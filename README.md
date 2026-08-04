# Horror Movie Rank

An interactive horror and thriller ranking chart with 661 films from 2005 through June 2026.

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

The composite score is `47.5% × IMDb (scaled to 100) + 52.5% × Tomatometer`. Ratings are snapshots and naturally change over time. The catalog contains 661 unique title/year entries; the Metacritic snapshot matched 608 critic scores, 16 pages without a published score, and 37 titles without a matching Metacritic page as of August 4, 2026. Missing values are excluded only when that metric is selected as an axis.

Published with GitHub Pages at:
https://samueldovgin.github.io/Horror-Movie-Rank/
