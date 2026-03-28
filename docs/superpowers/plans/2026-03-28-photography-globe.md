# Photography Globe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an interactive 3D globe at `/photography/map` showing countries where photos were taken; clicking a country navigates to `/photography?country=<name>` to filter the gallery.

**Architecture:** globe.gl renders a WebGL globe in a `PhotoGlobe.svelte` component (`client:only`). Country data is derived at build time from the photography collection via a new `country` frontmatter field. The photography page gains a URL-param-driven country filter layered on top of its existing tag filter.

**Tech Stack:** globe.gl, Svelte 5, Astro 5, Tailwind CSS 4, pnpm

---

## File Map

| Action | File | Purpose |
|---|---|---|
| Install | — | `globe.gl` package |
| Modify | `src/content.config.ts` | Add optional `country` field to photography schema |
| Modify | `src/content/photography/*.md` (17 files) | Add `country` frontmatter |
| Modify | `src/components/PhotoEntry.astro` | Add `country` prop + `data-country` attribute on wrapper |
| Create | `src/components/PhotoGlobe.svelte` | globe.gl interactive globe component |
| Create | `src/pages/photography/map.astro` | `/photography/map` page |
| Modify | `src/pages/photography/index.astro` | Pass `country` to PhotoEntry, add Map link, URL-param country filter |

---

## Task 1: Install globe.gl

**Files:**
- Modify: `package.json` (via pnpm)

- [ ] **Step 1: Install the package**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io
pnpm add globe.gl
```

Expected: `dependencies` in `package.json` now includes `"globe.gl": "..."` with no errors.

- [ ] **Step 2: Commit**

```bash
git add package.json pnpm-lock.yaml
git commit -m "chore: add globe.gl dependency"
```

---

## Task 2: Add `country` field to photography schema

**Files:**
- Modify: `src/content.config.ts`

- [ ] **Step 1: Add the field**

In `src/content.config.ts`, update the photography schema to add `country` after `location`:

```ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const photography = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/photography' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.coerce.date(),
      image: image(),
      tags: z.array(z.string()).default([]),
      location: z.string().optional(),
      country: z.string().optional(),
      camera: z.string().optional(),
      draft: z.boolean().default(false),
      background: z.boolean().default(false),
    }),
});
```

Leave everything else in the file unchanged.

- [ ] **Step 2: Verify build still passes**

```bash
pnpm build
```

Expected: Build completes with no TypeScript or schema errors.

- [ ] **Step 3: Commit**

```bash
git add src/content.config.ts
git commit -m "feat: add country field to photography schema"
```

---

## Task 3: Add `country` frontmatter to all photo files

**Files:**
- Modify: all 17 files in `src/content/photography/`

For each file below, add `country: "..."` on the line immediately after `location:` (or after `camera:` if no `location` field is present). The value is the plain English country name.

- [ ] **Step 1: Update each file**

**`african-penguin.md`** — add `country: "South Africa"`
**`drakensberg-storm.md`** — add `country: "South Africa"`
**`greater-kudu.md`** — add `country: "South Africa"`
**`iridescent-beetle.md`** — add `country: "South Africa"`
**`desert-sunset-drive.md`** — add `country: "Namibia"`
**`european-roller.md`** — add `country: "Namibia"`
**`european-roller-portrait.md`** — add `country: "Namibia"`
**`oryx-of-garub.md`** — add `country: "Namibia"`
**`scarlet-dragonfly.md`** — add `country: "Namibia"`
**`sossusvlei-reflections.md`** — add `country: "Namibia"`
**`spotted-beetle.md`** — add `country: "Namibia"`
**`hands-on-the-basket.md`** — add `country: "Kenya"`
**`nairobi-national-park-kenya.md`** — add `country: "Kenya"`
**`rhino-mother-and-calf.md`** — add `country: "Kenya"`
**`grand-chandelier.md`** — add `country: "Oman"`
**`sri-lanka-jeep.md`** — add `country: "Sri Lanka"`
**`swedish-lake.md`** — add `country: "Sweden"`

Example — `african-penguin.md` before:
```yaml
---
title: "African Penguin"
date: 2023-03-25
image: ./_3254135.jpg
tags: ["wildlife", "south-africa"]
location: "South Africa"
camera: "Olympus OM-D E-M5 Mark II"
draft: false
background: true
---
```

After:
```yaml
---
title: "African Penguin"
date: 2023-03-25
image: ./_3254135.jpg
tags: ["wildlife", "south-africa"]
location: "South Africa"
country: "South Africa"
camera: "Olympus OM-D E-M5 Mark II"
draft: false
background: true
---
```

- [ ] **Step 2: Verify build still passes**

```bash
pnpm build
```

Expected: Build completes with no errors. All 17 photos still render.

- [ ] **Step 3: Commit**

```bash
git add src/content/photography/
git commit -m "feat: add country frontmatter to all photography entries"
```

---

## Task 4: Add `country` prop to PhotoEntry

**Files:**
- Modify: `src/components/PhotoEntry.astro`

The current wrapper div is:
```html
<div data-entry-wrapper data-tags={tags?.join(',') ?? ''} class="pb-24">
```

It needs a `data-country` attribute for the URL filter to query.

- [ ] **Step 1: Add `country` to the Props interface and destructure it**

Replace the Props interface and destructuring:

```astro
---
import { Image } from 'astro:assets';
import type { ImageMetadata } from 'astro';

interface Props {
  image: ImageMetadata;
  title: string;
  location?: string;
  country?: string;
  camera?: string;
  tags?: string[];
  fullSrc: string;
  fullWidth: number;
  fullHeight: number;
  index: number;
}

const { image, title, location, country, camera, tags, fullSrc, fullWidth, fullHeight, index } = Astro.props;
```

- [ ] **Step 2: Add `data-country` to the wrapper div**

Change:
```html
<div data-entry-wrapper data-tags={tags?.join(',') ?? ''} class="pb-24">
```

To:
```html
<div data-entry-wrapper data-tags={tags?.join(',') ?? ''} data-country={country ?? ''} class="pb-24">
```

- [ ] **Step 3: Verify build still passes**

```bash
pnpm build
```

Expected: Build succeeds. PhotoEntry still renders; `country` is optional so no existing call sites break.

- [ ] **Step 4: Commit**

```bash
git add src/components/PhotoEntry.astro
git commit -m "feat: add data-country attribute to PhotoEntry wrapper"
```

---

## Task 5: Create PhotoGlobe.svelte

**Files:**
- Create: `src/components/PhotoGlobe.svelte`

This is a Svelte 5 component. It must use `client:only="svelte"` from the parent page since globe.gl requires a real DOM.

- [ ] **Step 1: Create the file**

Create `src/components/PhotoGlobe.svelte` with the following content:

```svelte
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let { countries }: { countries: Record<string, number> } = $props();

  let container: HTMLDivElement;
  let globe: any;
  let rotationTimer: ReturnType<typeof setTimeout>;

  // Map from plain English country name → ISO 3166-1 alpha-2 code.
  // Extend this table when adding photos from a new country.
  const COUNTRY_ISO: Record<string, string> = {
    'South Africa': 'ZA',
    'Namibia': 'NA',
    'Kenya': 'KE',
    'Oman': 'OM',
    'Sri Lanka': 'LK',
    'Sweden': 'SE',
  };

  // Reverse: ISO code → country name
  const ISO_COUNTRY: Record<string, string> = Object.fromEntries(
    Object.entries(COUNTRY_ISO).map(([name, iso]) => [iso, name])
  );

  let hoveredISO: string | null = null;

  function isVisited(feat: any): boolean {
    const iso: string = feat?.properties?.ISO_A2 ?? '';
    const name = ISO_COUNTRY[iso];
    return !!(name && countries[name]);
  }

  function getCapColor(feat: any): string {
    const iso: string = feat?.properties?.ISO_A2 ?? '';
    const name = ISO_COUNTRY[iso];
    if (!name || !countries[name]) return '#e8e4de';
    return iso === hoveredISO ? '#f26e6e' : '#b11d1d';
  }

  function startRotation() {
    globe?.controls().then?.((c: any) => { c.autoRotate = true; });
    try {
      const controls = globe?.controls();
      if (controls) {
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.3;
      }
    } catch (_) {}
  }

  function stopRotation() {
    try {
      const controls = globe?.controls();
      if (controls) controls.autoRotate = false;
    } catch (_) {}
    clearTimeout(rotationTimer);
  }

  function scheduleRotationResume() {
    clearTimeout(rotationTimer);
    rotationTimer = setTimeout(startRotation, 3000);
  }

  function solidColorDataURL(color: string): string {
    const canvas = document.createElement('canvas');
    canvas.width = 2;
    canvas.height = 2;
    const ctx = canvas.getContext('2d')!;
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, 2, 2);
    return canvas.toDataURL();
  }

  onMount(async () => {
    const { default: Globe } = await import('globe.gl');

    const geoRes = await fetch(
      'https://raw.githubusercontent.com/vasturiano/react-globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson'
    );
    const geoData = await geoRes.json();

    globe = Globe()(container)
      .width(container.clientWidth)
      .height(container.clientHeight)
      .backgroundColor('rgba(0,0,0,0)')
      .showAtmosphere(false)
      .globeImageUrl(solidColorDataURL('#d4cfc8'))
      .polygonsData(geoData.features)
      .polygonCapColor(getCapColor)
      .polygonSideColor(() => '#c9c4bc')
      .polygonStrokeColor(() => '#c9c4bc')
      .polygonAltitude(0.006)
      .polygonLabel((feat: any) => {
        const iso: string = feat?.properties?.ISO_A2 ?? '';
        const name = ISO_COUNTRY[iso];
        if (!name || !countries[name]) return '';
        const count = countries[name];
        return `<div style="background:#27272a;color:#fafafa;padding:4px 10px;border-radius:4px;font-size:13px;font-family:serif;pointer-events:none">${name} — ${count} photo${count !== 1 ? 's' : ''}</div>`;
      })
      .onPolygonHover((feat: any) => {
        const iso: string = feat?.properties?.ISO_A2 ?? '';
        const name = ISO_COUNTRY[iso];
        hoveredISO = name && countries[name] ? iso : null;
        container.style.cursor = hoveredISO ? 'pointer' : 'default';
        globe.polygonCapColor(getCapColor);
      })
      .onPolygonClick((feat: any) => {
        const iso: string = feat?.properties?.ISO_A2 ?? '';
        const name = ISO_COUNTRY[iso];
        if (name && countries[name]) {
          window.location.href = `/photography?country=${encodeURIComponent(name)}`;
        }
      });

    // Enable auto-rotation
    const controls = globe.controls();
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.3;

    // Pause on user interaction, resume after 3s
    container.addEventListener('pointerdown', () => {
      stopRotation();
    });
    container.addEventListener('pointerup', scheduleRotationResume);

    // Resize observer
    const ro = new ResizeObserver(() => {
      if (container) {
        globe.width(container.clientWidth).height(container.clientHeight);
      }
    });
    ro.observe(container);

    return () => {
      ro.disconnect();
    };
  });

  onDestroy(() => {
    clearTimeout(rotationTimer);
  });
</script>

<div bind:this={container} class="w-full h-full"></div>
```

- [ ] **Step 2: Verify build passes**

```bash
pnpm build
```

Expected: Build succeeds. The component is `client:only` so it won't be SSR'd; no server-side errors expected.

- [ ] **Step 3: Commit**

```bash
git add src/components/PhotoGlobe.svelte
git commit -m "feat: add PhotoGlobe Svelte component using globe.gl"
```

---

## Task 6: Create the map page

**Files:**
- Create: `src/pages/photography/map.astro`

- [ ] **Step 1: Create the page**

Create `src/pages/photography/map.astro`:

```astro
---
import { getCollection } from 'astro:content';
import Layout from '../../layouts/Layout.astro';
import PhotoGlobe from '../../components/PhotoGlobe.svelte';

const photos = (await getCollection('photography')).filter(
  (p) => !p.data.draft && !!p.data.country
);

const countryCounts: Record<string, number> = {};
for (const photo of photos) {
  const c = photo.data.country!;
  countryCounts[c] = (countryCounts[c] ?? 0) + 1;
}

const countryCount = Object.keys(countryCounts).length;
---

<Layout
  title="Photography Map"
  description="A map of countries where Pieter Wittebol has taken photographs."
>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
    <h1
      class="text-3xl sm:text-4xl font-bold text-gray-900 mb-2"
      data-reveal="left"
    >
      Where I've Shot
    </h1>
    <p class="text-gray-500 mb-8">
      {countryCount} {countryCount === 1 ? 'country' : 'countries'} so far
    </p>

    <div class="relative w-full rounded-xl overflow-hidden" style="height: 560px;">
      <PhotoGlobe countries={countryCounts} client:only="svelte" />
    </div>

    <p class="mt-4 text-sm text-gray-400 text-center">
      Click a highlighted country to browse its photos
    </p>
  </div>
</Layout>
```

- [ ] **Step 2: Verify build passes and page route exists**

```bash
pnpm build
```

Expected: Build succeeds. `dist/photography/map/index.html` is generated.

- [ ] **Step 3: Commit**

```bash
git add src/pages/photography/map.astro
git commit -m "feat: add photography map page at /photography/map"
```

---

## Task 7: Wire up photography index — country prop, Map link, and URL filter

**Files:**
- Modify: `src/pages/photography/index.astro`

This task has three changes: (a) pass `country` prop to `PhotoEntry`, (b) add a Map link, (c) add the URL-param country filter + dismissible pill.

- [ ] **Step 1: Pass `country` to PhotoEntry**

In `src/pages/photography/index.astro`, find the `<PhotoEntry ... />` call inside the map and add the `country` prop:

```astro
<PhotoEntry
  image={photo.data.image}
  title={photo.data.title}
  location={photo.data.location}
  country={photo.data.country}
  camera={photo.data.camera}
  tags={photo.data.tags}
  fullSrc={photo.full.src}
  fullWidth={photo.full.width}
  fullHeight={photo.full.height}
  index={index}
/>
```

- [ ] **Step 2: Add Map link after the h1**

Find the `<h1>` element:
```astro
<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-10" data-reveal="left">
  Photography
</h1>
```

Replace it with:
```astro
<div class="flex items-baseline justify-between mb-10" data-reveal="left">
  <h1 class="text-3xl sm:text-4xl font-bold text-gray-900">
    Photography
  </h1>
  <a
    href="/photography/map"
    data-astro-prefetch
    class="text-sm text-gray-400 hover:text-gray-600 transition-colors"
  >
    View map →
  </a>
</div>
```

- [ ] **Step 3: Add a `country-pill` placeholder div above the gallery**

Find the gallery block:
```astro
{photosWithFull.length > 0 ? (
  <div id="gallery" class="pswp-gallery">
```

Add a div immediately before it:
```astro
<div id="country-pill" class="hidden mb-6"></div>

{photosWithFull.length > 0 ? (
  <div id="gallery" class="pswp-gallery">
```

- [ ] **Step 4: Add the `initCountryFilter` function to the `<script>` block**

At the bottom of the `<script>` block, just before the two `addEventListener` lines, add:

```ts
function initCountryFilter() {
  const params = new URLSearchParams(window.location.search);
  const country = params.get('country');
  const pill = document.getElementById('country-pill');
  const wrappers = document.querySelectorAll<HTMLElement>('[data-entry-wrapper]');

  if (!country || !pill) return;

  // Show pill
  pill.classList.remove('hidden');
  pill.innerHTML = `
    <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-700">
      Showing: <strong>${country}</strong>
      <button id="clear-country-filter" class="ml-1 text-gray-400 hover:text-gray-700 cursor-pointer leading-none" aria-label="Clear country filter">×</button>
    </span>
  `;

  document.getElementById('clear-country-filter')?.addEventListener('click', () => {
    history.replaceState(null, '', window.location.pathname);
    pill.classList.add('hidden');
    pill.innerHTML = '';
    wrappers.forEach((w) => {
      w.style.display = '';
    });
  });

  // Hide non-matching entries
  wrappers.forEach((wrapper) => {
    const wrapperCountry = wrapper.dataset.country ?? '';
    if (wrapperCountry.toLowerCase() !== country.toLowerCase()) {
      wrapper.style.display = 'none';
    }
  });
}
```

- [ ] **Step 5: Register `initCountryFilter` with `astro:page-load`**

Find the two existing event listener registrations at the bottom of the script:
```ts
document.addEventListener('astro:page-load', initGallery);
document.addEventListener('astro:page-load', initFilters);
```

Add a third:
```ts
document.addEventListener('astro:page-load', initGallery);
document.addEventListener('astro:page-load', initFilters);
document.addEventListener('astro:page-load', initCountryFilter);
```

- [ ] **Step 6: Verify build passes**

```bash
pnpm build
```

Expected: Build completes with no errors.

- [ ] **Step 7: Smoke test in dev server**

```bash
pnpm dev
```

Visit `http://localhost:4321/photography/map` — globe should render, 6 countries highlighted in burgundy.
Click a highlighted country (e.g. Namibia) — should navigate to `http://localhost:4321/photography?country=Namibia`.
On the photography page, a pill "Showing: Namibia ×" should appear and only Namibia photos should be visible.
Click × — all photos reappear, URL reverts to `/photography`.
Visit `http://localhost:4321/photography` (no param) — no pill, all photos shown, "View map →" link visible top-right.

- [ ] **Step 8: Commit**

```bash
git add src/pages/photography/index.astro
git commit -m "feat: wire country filter, map link, and URL param to photography page"
```
