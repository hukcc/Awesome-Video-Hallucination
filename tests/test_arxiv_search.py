"""Offline coverage for complete discovery and failure-safe state updates."""

import json
import sys
import unittest
from datetime import date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
from xml.sax.saxutils import escape

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import arxiv_search as search


def entry(number, published='2026-10-01T12:00:00Z'):
    return {
        'id': f'https://arxiv.org/abs/2610.{number:05d}v1',
        'published': published,
        'title': f'Video Hallucination Study {number}',
        'summary': 'A study of video hallucination.',
    }


def response(entries=(), start=0, total=None):
    total = len(entries) if total is None else total
    items = ''.join('<entry>' + ''.join(f'<{key}>{escape(value)}</{key}>'
                                      for key, value in item.items()) + '</entry>' for item in entries)
    body = (
        '<feed xmlns="http://www.w3.org/2005/Atom" '
        'xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
        f'<opensearch:totalResults>{total}</opensearch:totalResults>'
        f'<opensearch:startIndex>{start}</opensearch:startIndex>{items}</feed>'
    )
    return Mock(content=body.encode('utf-8'))


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.get = patch.object(search.requests, 'get').start()
        self.sleep = patch.object(search.time, 'sleep').start()
        self.addCleanup(patch.stopall)

    def test_more_than_100_results_are_not_truncated(self):
        self.get.side_effect = [response([entry(i) for i in range(100)], total=101),
                                response([entry(100)], start=100, total=101)]
        found = search.search_arxiv('all:video')
        self.assertEqual(len(found), 101)
        self.assertEqual(search.extract_arxiv_id(found[-1]), '2610.00100')
        self.assertEqual([call.kwargs['params']['start'] for call in self.get.call_args_list], [0, 100])
        for call in self.get.call_args_list:
            self.assertEqual(call.kwargs['params']['max_results'], 100)
            self.assertEqual(call.kwargs['params']['sortBy'], 'submittedDate')
            self.assertEqual(call.kwargs['params']['sortOrder'], 'descending')
            self.assertEqual(call.kwargs['timeout'], 30)
        self.sleep.assert_called_once_with(search.REQUEST_DELAY)

    def test_short_pages_continue_using_actual_result_count(self):
        self.get.side_effect = [response([entry(1)], total=2), response([entry(2)], start=1, total=2)]
        self.assertEqual(len(search.search_arxiv('all:video', page_size=100)), 2)
        self.assertEqual(self.get.call_args_list[-1].kwargs['params']['start'], 1)

    def test_cutoff_day_is_included_and_older_pages_stop_pagination(self):
        self.get.side_effect = [response([entry(1, '2026-09-02T00:00:00Z')], total=3),
                                response([entry(2, '2026-09-01T23:59:59Z')], start=1, total=3)]
        found = search.search_arxiv('all:video', page_size=1, cutoff=date(2026, 9, 2))
        self.assertEqual(len(found), 2)
        self.assertEqual(self.get.call_count, 2)

    def test_empty_search_is_a_success_without_an_extra_request(self):
        self.get.return_value = response()
        self.assertEqual(search.search_arxiv('all:video'), [])
        self.get.assert_called_once()
        self.sleep.assert_not_called()

    def test_invalid_page_sizes_do_not_make_requests(self):
        for size in (0, -1, 2001):
            with self.subTest(size=size), self.assertRaises(ValueError):
                search.search_arxiv('all:video', page_size=size)
        self.get.assert_not_called()

    def test_malformed_feed_and_http_200_api_errors_are_failures(self):
        bodies = [b'<feed>', b'<html><title>Service unavailable</title></html>',
                  b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/api/errors</id>'
                  b'<title>Error</title><summary>Invalid query</summary></entry></feed>']
        for body in bodies:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.get.return_value = Mock(content=body)
                search.search_arxiv('all:video')

    def test_inconsistent_pagination_is_not_mistaken_for_exhaustion(self):
        pages = [response([], total=5), response([entry(1)], start=1, total=2),
                 response([entry(1)], total=0), response([], total=-1), response([], total='unknown')]
        for page in pages:
            with self.subTest(body=page.content), self.assertRaises(ValueError):
                self.get.return_value = page
                search.search_arxiv('all:video')

    def test_repeated_results_fail_instead_of_looping_or_silently_skipping(self):
        for pages in ([response([entry(1), entry(1)], total=2)],
                      [response([entry(1)], total=2), response([entry(1)], start=1, total=2)]):
            with self.subTest(pages=len(pages)), self.assertRaisesRegex(ValueError, 'repeated paper IDs'):
                self.get.side_effect = pages
                search.search_arxiv('all:video')

    def test_entries_without_valid_identity_or_publication_date_fail(self):
        for item in ({**entry(1), 'id': 'error'}, {**entry(1), 'published': 'unknown'}):
            with self.subTest(item=item), self.assertRaises(ValueError):
                self.get.return_value = response([item])
                search.search_arxiv('all:video')

    def test_later_http_failure_does_not_return_partial_results(self):
        failed = response([entry(2)], start=1, total=2)
        failed.raise_for_status.side_effect = requests.HTTPError('503 unavailable')
        self.get.side_effect = [response([entry(1)], total=2), failed]
        with self.assertRaises(requests.HTTPError):
            search.search_arxiv('all:video')


class DiscoveryStateTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        self.readme = self.directory / 'README.md'
        self.known = self.directory / 'known_papers.json'
        self.output = self.directory / 'new_papers.md'
        self.gh_output = self.directory / 'github-output'
        self.readme.write_text('[Known paper](https://arxiv.org/abs/2610.00002)\n')
        self.known.write_text('{"arxiv_ids": ["2610.00003"]}\n')
        self.output.write_text('# New Papers\n\nExisting review decisions.\n')
        self.gh_output.write_text('previous=value\n')
        patch.multiple(search, README_PATH=str(self.readme), KNOWN_PAPERS_PATH=str(self.known),
                       OUTPUT_PATH=str(self.output), SEARCH_QUERIES=['first', 'second']).start()
        patch.dict(search.os.environ, GITHUB_OUTPUT=str(self.gh_output)).start()
        self.query = patch.object(search, 'search_arxiv').start()
        patch.object(search.time, 'sleep').start()
        clock = patch.object(search, 'datetime', wraps=datetime).start()
        clock.utcnow.return_value = datetime(2026, 11, 1, 22)
        patch('builtins.print').start()
        self.addCleanup(patch.stopall)

    def test_partial_or_total_failure_leaves_discovery_files_unchanged(self):
        originals = {path: path.read_bytes() for path in (self.readme, self.known, self.output, self.gh_output)}
        for results in ([ [entry(1)], requests.HTTPError('failed page') ],
                        [ requests.HTTPError('failed query'), requests.HTTPError('failed query') ]):
            with self.subTest(results=results):
                self.query.side_effect = results
                with self.assertRaisesRegex(RuntimeError, 'refusing to publish incomplete results'):
                    search.main()
                for path, original in originals.items():
                    self.assertEqual(path.read_bytes(), original)

    def test_complete_search_deduplicates_and_keeps_boundary_day_and_review_history(self):
        boundary = entry(1, '2026-09-02T00:00:00Z')
        old = entry(4, '2026-09-01T23:59:59Z')
        self.query.side_effect = [[boundary, entry(2), old], [boundary, entry(3)]]
        search.main()
        for call in self.query.call_args_list:
            self.assertEqual(call.kwargs['cutoff'], date(2026, 9, 2))
        output = self.output.read_text()
        self.assertIn('**1 new paper(s) found.**', output)
        self.assertEqual(output.count('### [Video Hallucination Study 1]'), 1)
        for number in (2, 3, 4):
            self.assertNotIn(f'### [Video Hallucination Study {number}]', output)
        self.assertIn('Existing review decisions.', output)
        self.assertEqual(json.loads(self.known.read_text())['arxiv_ids'],
                         [f'2610.{number:05d}' for number in range(1, 5)])
        self.assertIn('new_papers_count=1', self.gh_output.read_text())

    def test_complete_zero_result_search_keeps_existing_discovery_log(self):
        original = self.output.read_bytes()
        self.query.side_effect = [[], []]
        search.main()
        self.assertEqual(self.output.read_bytes(), original)
        self.assertIn('new_papers_count=0', self.gh_output.read_text())


if __name__ == '__main__':
    unittest.main()
