"""Offline fixtures for remote status interpretation and relevance-report consistency."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_remote_sources import arxiv_signals, canonical_url, classify, collect_urls, report_markdown
from generate_relevance_review import render


def response(body='', status=200, url='https://arxiv.org/abs/1234.56789', exit_code=0):
    return {'body': body, 'status': status, 'final_url': url, 'exit_code': exit_code, 'error': ''}


def arxiv(version=2, abstract='Video hallucination research.', comments=''):
    return (f'<meta name="citation_arxiv_id" content="1234.56789v{version}">'
            f'<meta name="citation_title" content="Video research">'
            f'<a href="/abs/1234.56789v{version}">Version</a>'
            f'<blockquote class="abstract">{abstract}</blockquote>'
            f'<td class="tablecell comments">{comments}</td>')


class SourceTests(unittest.TestCase):
    def test_statuses_distinguish_missing_from_restricted_and_transient(self):
        for status, expected in [(200, 'reachable'), (404, 'missing'), (410, 'missing'),
                                 (401, 'restricted'), (403, 'restricted'), (429, 'restricted'),
                                 (0, 'unverified'), (503, 'unverified')]:
            self.assertEqual(classify(response(status=status))[0], expected)
        self.assertEqual(classify(response(exit_code=28))[0], 'unverified')

    def test_successful_login_challenge_and_error_pages_are_not_verified(self):
        for title in ['404 Not Found', 'Just a moment...', 'Sign in to continue', 'Access denied']:
            self.assertEqual(classify(response(f'<title>{title}</title>'))[0], 'review')
        self.assertEqual(classify(response(url='https://example.org/login'))[0], 'review')
        self.assertEqual(classify(response('<title>A real project</title>'))[0], 'reachable')

    def test_badge_payload_is_inspected(self):
        url = 'https://img.shields.io/badge/test'
        self.assertEqual(classify(response('<svg><text>Code</text></svg>', url=url))[0], 'reachable')
        self.assertEqual(classify(response('<svg><text>repo not found</text></svg>', url=url))[0], 'review')
        self.assertEqual(classify(response('not an image', url=url))[0], 'review')

    def test_versions_require_matching_identity_and_parse_multi_digit_versions(self):
        result = arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response(arxiv(12)))
        self.assertEqual(result['status'], 'new-version')
        self.assertEqual(result['latest_version'], 12)
        current = arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response(arxiv(2)))
        self.assertEqual(current['status'], 'current')
        wrong = arxiv_signals('9999.00000', 'https://arxiv.org/abs/9999.00000v1', response(arxiv(12)))
        self.assertEqual(wrong['status'], 'unverified')
        unknown = arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response('<title>Success</title>'))
        self.assertEqual(unknown['status'], 'unverified')

    def test_withdrawal_signals_use_record_text_not_cited_work(self):
        for body in [arxiv(abstract='This paper has been\nwithdrawn by the authors.'),
                     arxiv(comments='This article was withdrawn due to an error.')]:
            result = arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response(body))
            self.assertEqual(result['status'], 'withdrawal-review')
        body = arxiv(abstract='We compare with a withdrawn baseline.') + '<div>Related paper: This paper is withdrawn.</div>'
        self.assertEqual(arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response(body))['status'], 'current')
        title_notice = arxiv().replace('content="Video research"', 'content="Video research (withdrawn)"')
        self.assertEqual(arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response(title_notice))['status'], 'withdrawal-review')

    def test_restricted_and_inconsistent_versions_remain_unknown(self):
        restricted = arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response(status=403))
        self.assertEqual(restricted['status'], 'unverified')
        self.assertIsNone(restricted['withdrawal_signal'])
        older = arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v2', response(arxiv(1)))
        self.assertEqual(older['status'], 'unverified')

    def test_arxiv_withdrawal_banner_with_unchanged_abstract(self):
        body = ('<meta name="citation_arxiv_id" content="1234.56789">'
                '<span class="error">This paper has been withdrawn by Author</span>'
                '<div class="dateline">[Submitted on 9 May (v1), last revised 15 Aug (this version, v2)]</div>'
                '<blockquote class="abstract">Original video research abstract.</blockquote>'
                '<td class="comments mathjax"><em>The authors are withdrawing this manuscript due to errors.</em></td>')
        record = arxiv_signals('1234.56789', 'https://arxiv.org/abs/1234.56789v1', response(body))
        self.assertEqual(record['status'], 'withdrawal-review')
        self.assertEqual(record['latest_version'], 2)

    def test_catalog_collection_deduplicates_fragments_but_preserves_owners(self):
        data = {'entries': [{'name': 'A', 'paper_url': 'https://example.org/p', 'resources': {'code': 'https://example.org/c#top'}},
                            {'name': 'B', 'paper_url': 'https://example.org/p', 'resources': {'code': 'https://example.org/c#bottom'}}]}
        details = {'papers': {'id': {'source_url': 'https://example.org/pv1', 'scope_review': {'source_url': 'https://example.org/html/pv1'}}}}
        urls = collect_urls(data, details, '![Badge](https://img.shields.io/badge/code) ![Awesome](https://awesome.re/badge.svg)')
        self.assertEqual(len(urls), 6)
        self.assertEqual(len(urls['https://example.org/c']), 2)
        self.assertEqual(canonical_url('https://example.org/c?q=1#top'), 'https://example.org/c?q=1')

    def test_report_has_explicit_limits_and_actionable_flags(self):
        report = {'checked_at': '2026-10-01', 'links': [{'url': 'https://example.org/p', 'result': 'restricted', 'note': 'HTTP 403'}],
                  'arxiv': [{'paper_id': '1234.56789', 'reviewed_version': 1, 'latest_version': 2, 'status': 'new-version'}]}
        text = report_markdown(report)
        self.assertIn('not proof of identity or relevance', text)
        self.assertIn('new-version', text)
        self.assertIn('HTTP 403', text)

    def test_relevance_report_is_current_and_preserves_every_contribution(self):
        data = json.loads((ROOT / 'data/papers.json').read_text())
        metadata = json.loads((ROOT / 'data/paper_details.json').read_text())
        text = render(data, metadata)
        self.assertEqual(text, (ROOT / 'docs/RELEVANCE_REVIEW.md').read_text())
        for entry in data['entries']:
            self.assertEqual(text.count('../README.md#paper-' + entry['id'] + ')'), 1)
        self.assertIn('not a full-text audit of every paper', text)
        self.assertIn('pending decisions', text)


if __name__ == '__main__':
    unittest.main()
