# Photography Globe & Filter Controller — Design Spec

**Date:** 2026-03-28

## Problem

The interactive globe lives on a separate `/photography/map` subpage, requiring navigation away from the photo grid to browse by country. Clicking a country causes a full page reload to `/photography?country=X`.

On the photography page itself, two separate initializers — `initFilters()` and `initCountryFilter()` — share state via module-level variables (`activeCountry`, `reapplyTagFilter`). When a country is active, the tag filter panel does not update to show only the tags present on photos from that country.

## Goal

- Embed the globe on the main photography page, between the title and the tag filter panel.
- Clicking a country applies the country filter inline and scrolls to the photos — no navigation.
- The tag filter panel updates dynamically to show only tags present on photos from the active country.
- Delete the `/photography/map` subpage.
- Remove shared module-level variables by merging filter init functions into one controller.

## Files changed

| File | Change |
|---|---|
| `src/pages/photography/map.astro` | Deleted |
| `src/components/PhotoGlobe.svelte` | Replace navigation with `CustomEvent` dispatch |
| `src/pages/photography/index.astro` | Add globe, unified filter controller, remove map link |

## `PhotoGlobe.svelte`

Replace `onPolygonClick` handler:

**Before:**
```ts
window.location.href = `/photography?country=${encodeURIComponent(name)}`;
```

**After:**
```ts
container.dispatchEvent(new CustomEvent('country-select', {
  detail: { country: name },
  bubbles: true,
}));
```

No other changes to the component.

## `index.astro` — layout

Remove the "View map →" link from the title row. Insert the globe section between the title row and the tag filters:

```html
<div class="relative w-full rounded-xl overflow-hidden h-[400px] sm:h-[560px] mb-4">
  <PhotoGlobe countries={countryCounts} client:only="svelte" />
</div>
<p class="mb-10 text-sm text-gray-400 text-center">Click a country to filter photos</p>
```

Country counts are computed in the frontmatter (same logic as the deleted `map.astro`):

```ts
const countryCounts: Record<string, number> = {};
for (const photo of photos) {
  if (photo.data.country) {
    countryCounts[photo.data.country] = (countryCounts[photo.data.country] ?? 0) + 1;
  }
}
```

## `index.astro` — filter controller

Replace `initFilters()` and `initCountryFilter()` with a single `initFilters()` function.

### State (all local to `initFilters`)

| Variable | Type | Description |
|---|---|---|
| `activeTags` | `Set<string>` | Currently selected tag filters |
| `activeCountry` | `string \| null` | Currently active country; `null` means no filter |
| `panelOpen` | `boolean` | Whether the tag filter panel is expanded |

The module-level `activeCountry` and `reapplyTagFilter` variables are deleted.

### Key inner functions

**`isMatch(wrapper)`** — unchanged. Checks both `activeCountry` and `activeTags`.

**`applyFilters()`** — unchanged. Shows/hides photo wrappers based on `isMatch`.

**`updateCompatibleTags()`** — unchanged. Shows/hides tag buttons in the panel based on which tags appear on currently-matching photos.

**`setCountry(country: string | null)`** — new. Handles all country transitions:
1. Set `activeCountry` to the normalised (lowercased) value or `null`
2. Update the country pill (show with label + clear button, or hide and clear)
3. Call `applyFilters()`
4. Call `updateCompatibleTags()`

### Event listener

`initFilters` listens for `country-select` on the document:

```ts
document.addEventListener('country-select', (e: Event) => {
  const country = (e as CustomEvent<{ country: string }>).detail.country;
  setCountry(country);
  document.getElementById('gallery')?.scrollIntoView({ behavior: 'smooth' });
});
```

### Initialisation

On `astro:page-load`:
1. `initGallery()` — unchanged
2. `initFilters()` — unified function; sets up tag toggle, clear, panel open/close, and `country-select` listener

`initCountryFilter()` is removed. No URL param reading.

## Behaviour

| Scenario | Result |
|---|---|
| Click a country on the globe | Country filter applied, tag panel shows only that country's tags, page scrolls to gallery |
| Click country pill "×" | Country filter cleared, all photos shown, tag panel resets to all tags |
| Select a tag while country is active | Only tags compatible with both the country and active tags remain visible |
| Clear tags while country is active | Tag panel resets to tags compatible with the country only |
| Visit `/photography/map` | 404 (page deleted) |

## Out of scope

- URL param deep-linking (`?country=X`) — no longer produced by anything
- Collapsing or hiding the globe when a country is active
