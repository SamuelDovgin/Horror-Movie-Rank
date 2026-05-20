# Mobile-Friendly Updates

Summary of responsive improvements made to the Horror Movie Rank app (`index.html`). **No filtering, chart data, popup content, CSV import, or score-mode behavior was changed** — only layout, touch targets, and presentation on small screens.

## Viewport & page shell

- Added `viewport-fit=cover` so notched phones respect safe areas.
- Added `env(safe-area-inset-*)` padding on `.wrap` for left/right/bottom insets.
- Set `overflow-x: hidden` on `body` and `-webkit-text-size-adjust: 100%` on `html` to prevent accidental horizontal page scroll and text zoom quirks on iOS.

## Stats header

- At **≤850px**: stats grid uses `minmax(0, 1fr)` (avoids overflow), tighter gaps, slightly smaller type, `word-break` on stat values (e.g. lead counts).
- At **≤480px**: stat numbers scale down slightly for narrow phones.

## Legend & intro

- Reduced legend gap and font size on tablets/phones.
- Title (`h1`) uses a slightly smaller clamp range on narrow viewports.

## Filter bar

- Filter and clear buttons: **44px min height**, `touch-action: manipulation`, no gray tap flash.
- **≤850px**: filter groups align with labels; status line no longer indented by desktop label width.
- **≤480px**: each filter group stacks vertically; labels full-width; clear button full-width; filter pills centered for easier tapping.

## RT import panel

- Already stacked on small screens; **Choose CSV** is now full-width with 44px min height for touch.

## Chart area

- `overscroll-behavior: contain` and `scroll-behavior: smooth` on `.chart-scroll` for nicer panning without pulling the whole page.
- **≤850px**: sticky hint text (“Swipe to explore chart →”) inside the scroll area; at **≤600px** copy updates to “Swipe chart · tap dots for details”.
- Chart dimensions (1320×820) unchanged — horizontal scroll preserved.

## Movie popup

- **≤850px**: popup width uses `100vw - 24px`; stat grid **2 columns** instead of 3.
- **≤600px**: popup becomes a **fixed bottom sheet** (centered, safe-area aware, max-height ~58vh, scrollable body) so details stay on screen while exploring the chart.
- Close button: **44×44px** touch target.
- **JavaScript**: On viewports ≤600px, absolute `left`/`top` positioning is skipped (sheet layout). On 601–850px, after opening near a dot, the chart auto-scrolls so the popup stays visible in the scroll viewport.

## Footer note

- Slightly smaller type on narrow screens for readability without crowding the chart.

## Files touched

| File | Change |
|------|--------|
| `index.html` | CSS media queries, safe areas, touch targets, chart hint, popup sheet; small `showPopup` positioning branch |

## Testing

### Automated smoke test (375×812 viewport)

Run locally:

```bash
python3 -m http.server 8765
# Visit http://localhost:8765/index.html
```

Verified on **2026-05-20**:

| Check | Result |
|-------|--------|
| Page loads without JS errors | Pass (console clean aside from browser tooling warnings) |
| Horror filter | Pass — count updates to “219 of 633” |
| Tap movie dot (Hereditary) | Pass — popup opens with title, stats, badges |
| Mobile bottom sheet (≤600px) | Pass — popup fixed at bottom, 2-column stat grid |
| Escape closes popup | Pass |
| Audience RT button | Pass — still disabled until CSV import |

### Manual checks (recommended)

1. DevTools device mode: iPhone SE (375px), iPhone 14 (390px), iPad (768px).
2. Chart horizontal pan + swipe hint visible on narrow screens.
3. CSV import file picker on a real phone.
