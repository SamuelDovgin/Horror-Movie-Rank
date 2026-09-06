#!/usr/bin/env python3
"""Rebuild static chart points and the Markdown catalog from verified additions.

Run from any directory with Python 3. No network or third-party dependencies.
Existing chart entries retain their rating snapshots; ranks use the stated formula.
"""
import html
import json
import re
import unicodedata
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'september-2026-expansion'

class Points(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.points = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'button' and 'movie-point' in attrs.get('class', '').split():
            self.points.append(attrs)

def composite(imdb, rt):
    return str((Decimal(str(imdb)) * Decimal('4.75') + Decimal(str(rt)) * Decimal('.525')).quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

def slug(title):
    ascii_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode().lower()
    return re.sub('[^a-z0-9]+', '-', ascii_title).strip('-')

def build():
    path = ROOT / 'index.html'
    content = path.read_text()
    baseline = [p for p in Points(content).points if p.get('data-source') != SOURCE]
    fixes = {'Bring Her Back': 'tt32246771', 'Presence': 'tt28249919', 'Monkey Man': 'tt9214772'}
    points, ids = [], set()
    for p in baseline:
        if p['data-title'] in fixes:
            p['data-imdb-id'] = fixes[p['data-title']]
        identity = p['data-imdb-id']
        if identity in ids:
            continue
        ids.add(identity)
        points.append(p)
    additions = json.loads((ROOT / 'data/catalog-additions.json').read_text())
    for r in additions:
        assert r['imdbId'] not in ids, f"Duplicate IMDb ID: {r['title']}"
        ids.add(r['imdbId'])
        kind = {'Horror': 'horror', 'Thriller': 'thriller', 'Horror/Thriller': 'hybrid'}[r['type']]
        english = r['language'].lower().startswith('english')
        p = {'type': 'button', 'class': f"movie-point {kind} {r['leadbucket']} {'english' if english else 'nonenglish'} new-addition", 'aria-label': r['title'] + ' details'}
        values = {
            'title': r['title'], 'year': r['year'], 'imdb-id': r['imdbId'], 'imdb': r['imdb'],
            'rt': f"{r['rt']}%", 'rt-critic': f"{r['rt']}%", 'critic-pct': r['rt'],
            'critic-count': r.get('criticCount') or '', 'rt-url': r['rtUrl'],
            'audience-pct': r['audience'] if r['audience'] is not None else '',
            'rt-audience': f"{r['audience']}%" if r['audience'] is not None else '',
            'audience-count': r.get('audienceCount', ''), 'audience-type': r.get('audienceType', ''),
            'audience-source': 'Rotten Tomatoes scorecard, checked September 6, 2026',
            'rt-source': 'verified-september-2026', 'ratings-checked': '2026-09-06',
            'language': r['language'], 'english': 'yes' if english else 'no',
            'lead': r['lead'], 'leadbucket': r['leadbucket'], 'type': r['type'],
            'subgenre': r['subgenre'], 'source': SOURCE,
            'slug': f"{slug(r['title'])}-{r['year']}-{r['imdbId']}",
            'yearbucket': '2005-2010' if r['year'] <= 2010 else '2010s' if r['year'] < 2020 else '2020s'
        }
        p.update({'data-' + k: str(v) for k, v in values.items()})
        points.append(p)
    for p in points:
        p['data-score'] = composite(p['data-imdb'], p['data-critic-pct'])
    points.sort(key=lambda p: (-float(p['data-score']), -float(p['data-imdb']), p['data-title'].casefold(), p['data-imdb-id']))
    rendered = []
    for rank, p in enumerate(points, 1):
        p['data-rank'] = str(rank)
        x = 78 + float(p['data-imdb']) / 10 * 1200
        y = 704 - float(p['data-critic-pct']) / 100 * 632
        diameter = max(8.2, min(15.2, 8.2 + (float(p['data-score']) - 30) / 9))
        color = {'Horror': '#ff4f68', 'Thriller': '#55a7ff', 'Horror/Thriller': '#b77dff'}[p['data-type']]
        p['style'] = f'--x:{x:.1f}px;--y:{y:.1f}px;--d:{diameter:.1f}px;--hit:{max(26, diameter+14):.1f}px;--c:{color};--z:{10001-rank};'
        p.pop('data-y-critic', None)
        label = f'<span class="point-label">{html.escape(p["data-title"])}</span>' if rank <= 12 else ''
        attrs = ' '.join(f'{k}="{html.escape(v, quote=True)}"' for k, v in p.items())
        rendered.append(f'<button {attrs}>{label}</button>')
    start = re.search(r'<button\b[^>]*class="movie-point\b', content).start()
    end = content.index('<div class="empty-state"', start)
    content = content[:start] + '\n'.join(rendered) + '\n' + content[end:]
    count = len(points)
    content = re.sub(r'(?<=id="catalogCount">)[\d,]+', f'{count:,}', content)
    content = re.sub(r'(?<=id="stat-visible">)[\d,]+', str(count), content)
    content = re.sub(r'(?<=id="filterStatus">)Showing \d+ movies\.', f'Showing {count} movies.', content)
    content = re.sub(r'Explore and compare \d+ horror', f'Explore and compare {count} horror', content)
    path.write_text(content)
    counts = Counter(p['data-type'] for p in points)
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    lines = [
        '# Horror & Thriller Chart — Full Movie Data',
        f'**Total: {count:,} movies** | Horror: {counts["Horror"]} | Thriller: {counts["Thriller"]} | Horror/Thriller: {counts["Horror/Thriller"]}',
        '', f'September 6, 2026 expansion: **{len(additions)} additions**. Two duplicate aliases were removed from the original 661 entries, leaving 659 original films. Three incorrect original IMDb links were corrected.',
        '', 'Scope: horror and thriller films dated 2005–2026. New catalog years follow IMDb; RT release years and dates are preserved in the source data because festival and theatrical dates can differ. The earlier 2026 refresh retains its U.S. release-year convention.',
        '', 'New IMDb ratings come from the IMDb non-commercial ratings dataset; new RT critic and audience scores come from individual movie scorecards. Existing films retain their previous rating snapshots. Composite = 4.75 × IMDb + 0.525 × RT critics, rounded to one decimal. All ranks are rebuilt using that formula.',
        '', 'Metacritic additions are keyed by IMDb ID to distinguish unrelated films sharing a title and year. Unverified scores remain unavailable, never zero. Unclassified lead tags are explicit. Sources and exclusions are recorded in `data/catalog-audit.json`; accepted additions are in `data/catalog-additions.json`.',
        '', 'This is a broad catalog audit, not a claim that every horror/thriller ever released is covered. Films without the scores required by the default chart remain in the audit for follow-up.',
        '', '| Rank | Title | Year | IMDb | Critics RT | Composite | Type | Lead | Language | Added |',
        '|---:|---|---:|---:|---:|---:|---|---|---|---|'
    ]
    for p in points:
        title = f'[{cell(p["data-title"])}](https://www.imdb.com/title/{p["data-imdb-id"]}/)'
        vals = [p['data-rank'], title, p['data-year'], p['data-imdb'], p['data-rt-critic'], p['data-score'], p['data-type'], p['data-lead'], p['data-language'], 'September 2026' if p.get('data-source') == SOURCE else 'Earlier catalog']
        lines.append('| ' + ' | '.join(cell(v) if i != 1 else v for i, v in enumerate(vals)) + ' |')
    (ROOT / 'movies-data.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'total': count, 'additions': len(additions), 'genres': counts}, indent=2))

if __name__ == '__main__':
    build()
