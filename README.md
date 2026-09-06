# Horror Movie Rank

An interactive horror and thriller ranking chart with 1,215 films from 2005–2026, expanded September 6, 2026.

## What the site includes

- Scatter plot with independently selectable X and Y axes: IMDb, Rotten Tomatoes critics, Rotten Tomatoes audience, or Metacritic
- Exact start and end year inputs, plus quick year presets
- Combinable title/subgenre/language search, genre, lead, language, and quality filters
- Dynamically recalculated composite ranks and a clickable ranked-results view
- Shareable filtered URLs
- Film detail cards with direct IMDb and Rotten Tomatoes links
- Metacritic critic scores matched by title and release year, with explicit unavailable/no-score states
- Optional Rotten Tomatoes CSV import for exact audience-score plotting
- Responsive, touch-friendly chart navigation

The composite score is `47.5% × IMDb (scaled to 100) + 52.5% × Tomatometer`. Ratings are snapshots and naturally change over time. The September 6 expansion adds **556 films**, removes two duplicate aliases, and corrects three existing IMDb links. All 1,215 chart points and their ranks are rebuilt consistently from that formula.

Use **September additions** above the chart to isolate the new movies. New films have verified IMDb dataset ratings and direct Rotten Tomatoes scorecard links; 329 also have verified Metacritic scores. Missing metric values are excluded only when that metric is selected as an axis. Lead tags that have not been reviewed are explicitly unclassified.

New entries use IMDb's film year; RT release dates are retained separately because festival and theatrical dates may differ. The earlier 2026 refresh retains its U.S. release-year convention. Coverage is broad, not exhaustive: unscored films, uncertain matches, and inaccessible source pages are recorded for follow-up rather than assigned invented ratings.

- `data/catalog-additions.json`: accepted films, rating snapshots, identities, cast/director evidence, and source links.
- `data/catalog-audit.json`: candidate-by-candidate results and exclusions.
- `data/discovery-sources.json`: genre guides checked during discovery.
- `data/metacritic-additions.json` and `.js`: new Metacritic matches keyed by IMDb ID.
- `movies-data.md`: the full chart catalog with recalculated ranks.
- `python3 scripts/build_catalog.py`: rebuild chart points and the Markdown catalog without network access or third-party dependencies.


Published with GitHub Pages at:
https://samueldovgin.github.io/Horror-Movie-Rank/
