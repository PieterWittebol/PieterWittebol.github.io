# Photography Globe — Design Spec
_Date: 2026-03-28_

## Overview

Add an interactive 3D globe to the site at `/photography/map` that highlights countries where photos have been taken. Clicking a highlighted country navigates to `/photography?country=<name>`, which filters the gallery to that country. Country data is derived dynamically from the photography content collection — no manual maintenance required.

---

## 1. Schema & Data Layer

### `country` field
Add an optional `z.string()` field named `country` to the photography collection schema in `src/content.config.ts`. Each existing `.md` file in `src/content/photography/` gets a `country` frontmatter value (plain English name, e.g. `"South Africa"`).

Current countries and their photo counts:
| Country | Photos |
|---|---|
| South Africa | 4 |
| Namibia | 7 |
| Kenya | 3 |
| Oman | 1 |
| Sri Lanka | 1 |
| Sweden | 1 |

### Build-time data flow
In `src/pages/photography/map.astro`:
1. `getCollection('photography')` fetches all non-draft entries
2. Filter to entries with a `country` value
3. Build a `countryCounts: Record<string, number>` map (e.g. `{ "Namibia": 7, ... }`)
4. Pass to `PhotoGlobe` as a typed prop

### ISO lookup table
A static `COUNTRY_ISO: Record<string, string>` inside `PhotoGlobe.svelte` maps country names to ISO 3166-1 alpha-2 codes for use with GeoJSON polygon matching. **This table must be extended whenever a new country is added to the photography collection** — it is the one manual step required when adding photos from a new country.
```ts
const COUNTRY_ISO: Record<string, string> = {
  "South Africa": "ZA",
  "Namibia": "NA",
  "Kenya": "KE",
  "Oman": "OM",
  "Sri Lanka": "LK",
  "Sweden": "SE",
  // extend as new countries are added
};
```

---

## 2. Globe Component (`src/components/PhotoGlobe.svelte`)

### Library
`globe.gl` — WebGL/Three.js based, ~150KB gzipped. Installed via pnpm.

### GeoJSON
Fetched client-side from `https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson` (or equivalent). Each feature's `ISO_A2` property is matched against the lookup table to determine highlight state. The file is fetched from a third-party CDN at runtime; if unavailable, the globe renders without country polygons. Bundling locally is a future option if reliability becomes a concern.

### Props
```ts
export let countries: Record<string, number>; // { "Namibia": 7, ... }
```

### Theming (matches site palette)
| Element | Color |
|---|---|
| Background/space | transparent |
| Ocean | `#d4cfc8` |
| Land (non-visited) | `#e8e4de` |
| Highlighted country | `#b11d1d` (accent-700) |
| Highlighted country (hover) | `#f26e6e` (accent-400) |
| Polygon borders | `#c9c4bc` |

### Behaviour
- **Auto-rotation**: slow continuous rotation when idle; pauses on user interaction, resumes after 3 seconds
- **Drag**: user can freely rotate the globe with mouse/touch
- **Hover**: hovering a highlighted country shows a tooltip — `"Namibia — 7 photos"`; cursor changes to pointer
- **Click**: clicking a highlighted country navigates to `/photography?country=Namibia`
- **Non-visited countries**: not interactive (default cursor, no hover state)
- **SSR**: component uses `client:only="svelte"` — globe.gl requires a real DOM and `window`

---

## 3. Map Page (`src/pages/photography/map.astro`)

### Route
`/photography/map`

### Layout
Uses existing `Layout.astro` wrapper — consistent header, footer, page background.

### Page structure
```
<h1>Where I've Shot</h1>
<p>{countryCount} countries so far</p>   ← dynamic, derived from Object.keys(countryCounts).length
<div class="globe-container">            ← ~600px tall on desktop, responsive
  <PhotoGlobe countries={countryCounts} client:only="svelte" />
</div>
<p class="hint">Click a highlighted country to browse its photos</p>
```

### Discovery
A subtle "Map" link added near the top of `/photography/index.astro` so visitors can find the page.

---

## 4. Photography Page URL Filter (`src/pages/photography/index.astro`)

### URL parameter
`?country=Namibia` — plain English country name, case-insensitive matching against `photo.data.country`.

### Behaviour on load
On `astro:page-load`, the existing `initFilters` function is extended to:
1. Read `URLSearchParams` for a `country` param
2. If present, hide all photo entries where `photo.data.country` does not match (case-insensitive)
3. Render a dismissible pill above the gallery: `"Showing: Namibia ×"`

### Clearing the filter
Clicking × on the country pill:
1. Removes the `?country` param via `history.replaceState`
2. Shows all photos again
3. Removes the pill

### Graceful handling of missing `country`
Photos without a `country` value (i.e. `undefined`) are always shown when no country filter is active. When a country filter is active, photos with `undefined` country are hidden. The country pill is not rendered if no `?country` param is present.

### Coexistence with tag filter
Country filter and tag filter operate independently and additively — a photo must satisfy both to be visible. The country param is not surfaced as a button in the tag panel.

---

## 5. Files to Create / Modify

| Action | File |
|---|---|
| Modify | `src/content.config.ts` — add `country` field to photography schema |
| Modify | `src/content/photography/*.md` — add `country` frontmatter to all 17 files |
| Create | `src/components/PhotoGlobe.svelte` — globe.gl Svelte component |
| Create | `src/pages/photography/map.astro` — map page |
| Modify | `src/pages/photography/index.astro` — URL param filter + country pill + map link |
| Install | `globe.gl` via pnpm |
