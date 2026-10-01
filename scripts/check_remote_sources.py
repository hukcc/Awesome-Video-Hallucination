#!/usr/bin/env python3
"""Report remote link, arXiv revision, and withdrawal signals without editing the catalog."""

import argparse
import json
import re
import subprocess
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from check_catalog import Document

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.links = []
        self.title = []
        self.text = []
        self.in_title = False
        self.context = []
        self.record_text = []
        self.dateline = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property', ''))] = attrs.get('content', '')
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.context.append((tag, set(attrs.get('class', '').split())))

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        for index in range(len(self.context) - 1, -1, -1):
            if self.context[index][0] == tag:
                del self.context[index:]
                break

    def handle_data(self, value):
        self.text.append(value)
        if self.in_title:
            self.title.append(value)
        if any((tag == 'blockquote' and 'abstract' in classes) or
               (tag == 'td' and 'comments' in classes) or
               (tag == 'span' and 'error' in classes) for tag, classes in self.context):
            self.record_text.append(value)
        if any('dateline' in classes for _, classes in self.context):
            self.dateline.append(value)


def canonical_url(url):
    parsed = urlsplit(url)
    return urlunsplit(parsed._replace(fragment=''))


def collect_urls(data, metadata, readme):
    owners = defaultdict(set)
    for entry in data['entries']:
        for kind, url in [('paper', entry['paper_url']), *entry['resources'].items()]:
            if url:
                owners[canonical_url(url)].add(f'{entry["name"]}: {kind}')
    for key, detail in metadata['papers'].items():
        owners[canonical_url(detail['source_url'])].add(f'{key}: reviewed source')
        if detail.get('scope_review'):
            owners[canonical_url(detail['scope_review']['source_url'])].add(f'{key}: relevance evidence')
    doc = Document()
    doc.feed(readme)
    badges = [url for url in doc.links if urlsplit(url).hostname == 'img.shields.io']
    badges += re.findall(r'!\[[^\]]*\]\((https://[^)]+)\)', readme)
    for url in badges:
        owners[canonical_url(url)].add('README badge')
    return {url: sorted(labels) for url, labels in sorted(owners.items())}


def request(url, timeout):
    # Do not send credentials; redirects must remain HTTPS. curl verifies TLS by default.
    result = subprocess.run([
        'curl', '--silent', '--show-error', '--location', '--max-redirs', '5',
        '--proto', '=https', '--proto-redir', '=https', '--compressed',
        '--connect-timeout', '10', '--max-time', str(timeout), '--max-filesize', '5000000',
        '--user-agent', 'VideoHallucinationCatalog/1.0 (public-source audit)',
        '--write-out', '\nSOURCE_CHECK:%{http_code}\t%{url_effective}\t%{content_type}', url,
    ], capture_output=True)
    body, _, footer = result.stdout.rpartition(b'\nSOURCE_CHECK:')
    fields = footer.decode(errors='replace').split('\t')
    return {
        'status': int(fields[0]) if fields and fields[0].isdigit() else 0,
        'final_url': fields[1] if len(fields) > 1 else url,
        'content_type': fields[2] if len(fields) > 2 else '',
        'body': body.decode(errors='replace'),
        'error': result.stderr.decode(errors='replace').strip(),
        'exit_code': result.returncode,
    }


def classify(response):
    status = response['status']
    if response.get('exit_code') or status == 0:
        return 'unverified', response.get('error') or 'Transport failed or response incomplete.'
    if status in (401, 403, 429):
        return 'restricted', f'HTTP {status}; access or rate limit, not proof of removal.'
    if status in (404, 410):
        return 'missing', f'HTTP {status}; manually confirm before changing the link.'
    if not 200 <= status < 300:
        return 'unverified', f'HTTP {status}; retry before making an editorial decision.'
    page = Page()
    page.feed(response['body'])
    title = ' '.join(page.title).strip()
    if re.search(r'not found|page unavailable|^error\b|access denied|just a moment|^sign in|^log in', title, re.I):
        return 'review', f'Possible error, challenge, or login page: {title[:160]}'
    if '/login' in urlsplit(response['final_url']).path or '/signin' in urlsplit(response['final_url']).path:
        return 'review', 'Redirected to a login page.'
    if urlsplit(response['final_url']).hostname == 'img.shields.io':
        if '<svg' not in response['body'] or re.search(r'(?:invalid|inaccessible|not found)', ' '.join(page.text), re.I):
            return 'review', 'Badge payload is missing or reports an upstream error.'
    return 'reachable', 'HTTP success; reachability does not establish scientific correctness.'


def arxiv_signals(paper_id, reviewed_url, response):
    result = {'paper_id': paper_id, 'reviewed_url': reviewed_url, 'latest_version': None,
              'reviewed_version': None, 'withdrawal_signal': None, 'status': 'unverified'}
    reviewed = re.search(r'v(\d+)$', reviewed_url)
    if reviewed:
        result['reviewed_version'] = int(reviewed.group(1))
    if classify(response)[0] != 'reachable':
        return result
    page = Page()
    page.feed(response['body'])
    identity = page.meta.get('citation_arxiv_id', '')
    if not re.fullmatch(re.escape(paper_id) + r'(?:v\d+)?', identity):
        return result
    versions = [int(m.group(1)) for href in page.links
                if (m := re.search(r'/abs/' + re.escape(paper_id) + r'v(\d+)(?:$|[?#])', href))]
    versions += [int(m.group(1)) for m in re.finditer(re.escape(paper_id) + r'v(\d+)', identity)]
    versions += [int(v) for v in re.findall(r'\bv(\d+)\b', ' '.join(page.dateline))]
    if versions:
        result['latest_version'] = max(versions)
    # arXiv can retain the old abstract and put withdrawal only in a separate error banner.
    text = ' '.join([page.meta.get('citation_title', ''), page.meta.get('citation_abstract', ''), *page.record_text])
    plain = ' '.join(unescape(text).split())
    result['withdrawal_signal'] = bool(
        re.search(r'\bwithdrawn\b', page.meta.get('citation_title', ''), re.I) or
        re.search(r'\b(?:this (?:paper|article|submission|work) (?:has been|is|was) withdrawn|withdrawn by|withdrawal notice|authors are withdrawing)\b|^\s*\[?withdrawn\b', plain, re.I))
    if result['withdrawal_signal']:
        result['status'] = 'withdrawal-review'
    elif result['latest_version'] is None or result['reviewed_version'] is None:
        result['status'] = 'unverified'
    elif result['latest_version'] > result['reviewed_version']:
        result['status'] = 'new-version'
    elif result['latest_version'] < result['reviewed_version']:
        result['status'] = 'unverified'
    else:
        result['status'] = 'current'
    return result


def report_markdown(report):
    lines = ['# Remote Source Audit', '', f'Checked: {report["checked_at"]}', '',
             'Read-only checks. HTTP success is not proof of identity or relevance. Access restrictions and network failures '
             'remain unverified. No paper, link, or reviewed version is changed automatically.', '',
             '## Link Summary', '', ', '.join(f'{k}: {v}' for k, v in sorted(Counter(x['result'] for x in report['links']).items())), '',
             '## Links Requiring Review', '', '| Link | Result | Observation |', '| --- | --- | --- |']
    issues = [r for r in report['links'] if r['result'] != 'reachable']
    for row in issues:
        note = row['note'].replace('|', '\\|').replace('\n', ' ')
        lines.append(f'| [Source]({row["url"]}) | {row["result"]} | {note} |')
    if not issues:
        lines.append('| None | - | All requested URLs returned successful responses. |')
    lines += ['', '## arXiv Records Requiring Review', '',
              '| Paper | Reviewed | Latest observed | Result |', '| --- | --- | --- | --- |']
    for row in report['arxiv']:
        if row['status'] != 'current':
            lines.append(f'| [{row["paper_id"]}](https://arxiv.org/abs/{row["paper_id"]}) | {row["reviewed_version"] or "Unknown"} | {row["latest_version"] or "Unknown"} | {row["status"]} |')
    if all(r['status'] == 'current' for r in report['arxiv']):
        lines.append('| None | - | - | All observed versions match reviewed versions. |')
    lines += ['', 'Withdrawal detection is a conservative text signal, not a retraction database. Publisher-only '
              'records are checked for reachability; their version/retraction status requires manual publisher review. '
              'A changed arXiv version must be read before updating pinned evidence.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('reports/remote-sources'))
    parser.add_argument('--timeout', type=int, default=25)
    parser.add_argument('--delay', type=float, default=1.0)
    args = parser.parse_args()
    if args.timeout <= 0 or args.delay < 0:
        parser.error('Timeout must be positive and delay must be nonnegative.')
    data = json.loads((ROOT / 'data/papers.json').read_text())
    metadata = json.loads((ROOT / 'data/paper_details.json').read_text())
    urls = collect_urls(data, metadata, (ROOT / 'README.md').read_text())
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'links': [], 'arxiv': []}
    responses = {}
    for index, (url, owners) in enumerate(urls.items(), 1):
        response = request(url, args.timeout)
        if response['status'] in (0, 429, 500, 502, 503, 504) or response['exit_code']:
            time.sleep(max(args.delay, 3))
            response = request(url, args.timeout)
        result, note = classify(response)
        responses[url] = response
        report['links'].append({'url': url, 'owners': owners, 'status': response['status'],
                                'final_url': response['final_url'], 'result': result, 'note': note})
        print(f'{index}/{len(urls)} {result}: {url}', flush=True)
        time.sleep(args.delay)
    for key, detail in metadata['papers'].items():
        if re.fullmatch(r'\d{4}\.\d{4,5}', key):
            report['arxiv'].append(arxiv_signals(key, detail['source_url'], responses['https://arxiv.org/abs/' + key]))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    (args.output / 'report.md').write_text(report_markdown(report))
    print(f'Report saved to {args.output}. Review flags do not fail the run or change catalog data.')


if __name__ == '__main__':
    main()
