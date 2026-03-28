# Photography Globe & Filter Controller Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the globe onto the main photography page and replace the split filter initializers with a single controller that dynamically updates the tag panel when a country is active.

**Architecture:** `PhotoGlobe.svelte` dispatches a `country-select` CustomEvent instead of navigating. A unified `initFilters()` in `index.astro` owns all filter state (`activeTags`, `activeCountry`) and responds to that event via `setCountry()`, which updates the pill, runs `applyFilters()`, and runs `updateCompatibleTags()`. The `/photography/map` subpage is deleted.

**Tech Stack:** Astro 5, Svelte 5, Tailwind CSS 4, TypeScript, globe.gl, PhotoSwipe 5. No test framework — verify with `pnpm build` and manual browser testing.

---

### Task 1: Delete the map subpage

**Files:**
- Delete: `src/pages/photography/map.astro`

- [ ] **Step 1: Delete the file**

```bash
rm src/pages/photography/map.astro
```

- [ ] **Step 2: Verify build still passes**

```bash
pnpm build
```

Expected: build succeeds. The `/photography/map` route no longer exists.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: remove photography map subpage"
```

---

### Task 2: Update PhotoGlobe.svelte — dispatch event instead of navigating

**Files:**
- Modify: `src/components/PhotoGlobe.svelte:101-107`

- [ ] **Step 1: Replace the `onPolygonClick` handler**

In `src/components/PhotoGlobe.svelte`, find:

```ts
.onPolygonClick((feat: any) => {
  const iso: string = feat?.properties?.ISO_A2 ?? '';
  const name = ISO_COUNTRY[iso];
  if (name && countries[name]) {
    window.location.href = `/photography?country=${encodeURIComponent(name)}`;
  }
});
```

Replace with:

```ts
.onPolygonClick((feat: any) => {
  const iso: string = feat?.properties?.ISO_A2 ?? '';
  const name = ISO_COUNTRY[iso];
  if (name && countries[name]) {
    container.dispatchEvent(new CustomEvent('country-select', {
      detail: { country: name },
      bubbles: true,
    }));
  }
});
```

- [ ] **Step 2: Verify build still passes**

```bash
pnpm build
```

Expected: build succeeds, no TypeScript errors.

- [ ] **Step 3: Commit**

```bash
git add src/components/PhotoGlobe.svelte
git commit -m "feat: dispatch country-select event instead of navigating"
```

---

### Task 3: Add globe to the photography index page

**Files:**
- Modify: `src/pages/photography/index.astro` (frontmatter and template)

- [ ] **Step 1: Add the PhotoGlobe import to the frontmatter**

In `src/pages/photography/index.astro`, find the existing imports at the top of the frontmatter:

```ts
import { getCollection } from 'astro:content';
import { getImage } from 'astro:assets';
import Layout from '../../layouts/Layout.astro';
import PhotoEntry from '../../components/PhotoEntry.astro';
```

Add the PhotoGlobe import:

```ts
import { getCollection } from 'astro:content';
import { getImage } from 'astro:assets';
import Layout from '../../layouts/Layout.astro';
import PhotoEntry from '../../components/PhotoEntry.astro';
import PhotoGlobe from '../../components/PhotoGlobe.svelte';
```

- [ ] **Step 2: Compute country counts in the frontmatter**

After the existing `const allTags = ...` line, add:

```ts
const countryCounts: Record<string, number> = {};
for (const photo of photosWithFull) {
  if (photo.data.country) {
    countryCounts[photo.data.country] = (countryCounts[photo.data.country] ?? 0) + 1;
  }
}
```

- [ ] **Step 3: Remove the "View map →" link and add the globe section**

Find the title row in the template:

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

Replace with:

```astro
<div class="flex items-baseline justify-between mb-10" data-reveal="left">
  <h1 class="text-3xl sm:text-4xl font-bold text-gray-900">
    Photography
  </h1>
</div>

<div class="relative w-full rounded-xl overflow-hidden h-[400px] sm:h-[560px] mb-4">
  <PhotoGlobe countries={countryCounts} client:only="svelte" />
</div>
<p class="mb-10 text-sm text-gray-400 text-center">Click a country to filter photos</p>
```

- [ ] **Step 4: Verify build passes and globe renders**

```bash
pnpm build && pnpm preview
```

Open `http://localhost:4321/photography` in a browser. Confirm the globe renders between the title and the tag filter panel.

- [ ] **Step 5: Commit**

```bash
git add src/pages/photography/index.astro
git commit -m "feat: embed globe on photography index page"
```

---

### Task 4: Rewrite the filter controller as a unified initFilters()

**Files:**
- Modify: `src/pages/photography/index.astro` (`<script>` block)

- [ ] **Step 1: Replace the entire `<script>` block**

Replace everything from `<script>` to `</script>` in `src/pages/photography/index.astro` with:

```ts
<script>
  import PhotoSwipeLightbox from 'photoswipe/lightbox';
  import PhotoSwipe from 'photoswipe';
  import 'photoswipe/style.css';

  let currentLightbox: InstanceType<typeof PhotoSwipeLightbox> | null = null;

  function initGallery() {
    if (currentLightbox) {
      currentLightbox.destroy();
      currentLightbox = null;
    }

    const gallery = document.querySelector('#gallery');
    if (!gallery) return;

    const captionHeight = 72;

    const lightbox = new PhotoSwipeLightbox({
      gallery: '#gallery',
      children: 'a',
      pswpModule: PhotoSwipe,
      paddingFn: () => ({ top: 0, bottom: captionHeight, left: 0, right: 0 }),
    });

    lightbox.on('uiRegister', () => {
      lightbox.pswp!.ui!.registerElement({
        name: 'caption',
        order: 9,
        isButton: false,
        appendTo: 'root',
        html: '',
        onInit: (el) => {
          el.style.cssText = `position:absolute;bottom:0;left:0;right:0;height:${captionHeight}px;padding:10px 24px;background:#111827;color:#fff;text-align:center;font-size:14px;line-height:1.5;pointer-events:none;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;`;
          lightbox.pswp!.on('change', () => {
            const slide = lightbox.pswp!.currSlide;
            const caption = slide?.data?.element?.getAttribute('data-caption') ?? '';
            el.innerHTML = caption;
          });
        },
      });
    });

    lightbox.init();
    currentLightbox = lightbox;
  }

  function initFilters() {
    const activeTags = new Set<string>();
    let activeCountry: string | null = null;

    const tagButtons = document.querySelectorAll<HTMLButtonElement>('[data-tag]');
    const wrappers = document.querySelectorAll<HTMLElement>('[data-entry-wrapper]');
    const toggleBtn = document.querySelector<HTMLButtonElement>('#filter-toggle');
    const clearBtn = document.querySelector<HTMLButtonElement>('#filter-clear');
    const panel = document.querySelector<HTMLElement>('#filter-panel');
    const countBadge = document.querySelector<HTMLElement>('#filter-count');
    const chevron = document.querySelector<SVGElement>('#filter-chevron');
    const pill = document.getElementById('country-pill');

    if (!toggleBtn || !panel) return;

    let panelOpen = false;

    function openPanel() {
      panel!.style.overflow = 'hidden';
      panel!.style.height = '0';
      panel!.style.opacity = '0';
      panel!.getBoundingClientRect();
      const naturalH = panel!.scrollHeight;
      panel!.style.transition = 'height 300ms ease, opacity 300ms ease';
      panel!.style.height = naturalH + 'px';
      panel!.style.opacity = '1';
      function onEnd(e: TransitionEvent) {
        if (e.propertyName !== 'height') return;
        panel!.removeEventListener('transitionend', onEnd);
        panel!.style.height = 'auto';
        panel!.style.overflow = '';
        panel!.style.transition = '';
      }
      panel!.addEventListener('transitionend', onEnd);
      chevron?.classList.add('rotate-180');
      toggleBtn!.setAttribute('aria-expanded', 'true');
      panelOpen = true;
    }

    function closePanel() {
      const h = panel!.offsetHeight;
      panel!.style.overflow = 'hidden';
      panel!.style.height = h + 'px';
      panel!.getBoundingClientRect();
      panel!.style.transition = 'height 300ms ease, opacity 300ms ease';
      panel!.style.height = '0';
      panel!.style.opacity = '0';
      function onEnd(e: TransitionEvent) {
        if (e.propertyName !== 'height') return;
        panel!.removeEventListener('transitionend', onEnd);
        panel!.style.transition = '';
      }
      panel!.addEventListener('transitionend', onEnd);
      chevron?.classList.remove('rotate-180');
      toggleBtn!.setAttribute('aria-expanded', 'false');
      panelOpen = false;
    }

    toggleBtn.addEventListener('click', () => {
      if (panelOpen) closePanel();
      else openPanel();
    });

    function updateBadge() {
      const count = activeTags.size;
      if (countBadge) {
        countBadge.textContent = String(count);
        if (count > 0) countBadge.classList.replace('hidden', 'inline-flex');
        else countBadge.classList.replace('inline-flex', 'hidden');
      }
      if (clearBtn) {
        if (count > 0) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
      }
    }

    function isMatch(wrapper: HTMLElement): boolean {
      if (activeCountry) {
        const wrapperCountry = (wrapper.dataset.country ?? '').toLowerCase();
        if (wrapperCountry !== activeCountry) return false;
      }
      if (activeTags.size === 0) return true;
      const tags = (wrapper.dataset.tags ?? '').split(',').filter(Boolean);
      return [...activeTags].every((t) => tags.includes(t));
    }

    function hide(wrapper: HTMLElement) {
      const h = wrapper.offsetHeight;
      wrapper.style.overflow = 'hidden';
      wrapper.style.height = h + 'px';
      wrapper.getBoundingClientRect();
      wrapper.style.transition = 'height 400ms ease, opacity 400ms ease';
      wrapper.style.height = '0';
      wrapper.style.opacity = '0';
      function onEnd(e: TransitionEvent) {
        if (e.propertyName !== 'height') return;
        wrapper.removeEventListener('transitionend', onEnd);
        wrapper.style.display = 'none';
        wrapper.style.transition = '';
      }
      wrapper.addEventListener('transitionend', onEnd);
    }

    function show(wrapper: HTMLElement) {
      wrapper.style.display = '';
      wrapper.style.overflow = 'hidden';
      wrapper.style.height = '0';
      wrapper.style.opacity = '0';
      wrapper.getBoundingClientRect();
      const naturalH = wrapper.scrollHeight;
      wrapper.style.transition = 'height 400ms ease, opacity 400ms ease';
      wrapper.style.height = naturalH + 'px';
      wrapper.style.opacity = '1';
      function onEnd(e: TransitionEvent) {
        if (e.propertyName !== 'height') return;
        wrapper.removeEventListener('transitionend', onEnd);
        wrapper.style.height = 'auto';
        wrapper.style.overflow = '';
        wrapper.style.transition = '';
      }
      wrapper.addEventListener('transitionend', onEnd);
    }

    function applyFilters() {
      wrappers.forEach((wrapper) => {
        if (isMatch(wrapper)) {
          if (wrapper.style.display === 'none') show(wrapper);
        } else {
          if (wrapper.style.display !== 'none') hide(wrapper);
        }
      });
    }

    function updateCompatibleTags() {
      const compatible = new Set<string>();
      wrappers.forEach((wrapper) => {
        if (isMatch(wrapper)) {
          (wrapper.dataset.tags ?? '').split(',').filter(Boolean).forEach((t) => compatible.add(t));
        }
      });
      panel!.querySelectorAll<HTMLElement>('[data-panel-tag]').forEach((btn) => {
        const tag = btn.dataset.tag!;
        if (activeTags.has(tag) || compatible.has(tag)) {
          btn.style.display = '';
        } else {
          btn.style.display = 'none';
        }
      });
    }

    function setTagActive(tag: string, active: boolean) {
      document.querySelectorAll<HTMLElement>(`[data-tag="${tag}"]`).forEach((el) => {
        if (active) el.classList.add('!bg-gray-900', '!text-white');
        else el.classList.remove('!bg-gray-900', '!text-white');
      });
    }

    function setCountry(country: string | null) {
      activeCountry = country ? country.toLowerCase() : null;

      if (!pill) return;

      if (activeCountry && country) {
        pill.classList.remove('hidden');
        pill.innerHTML = '';
        const span = document.createElement('span');
        span.className = 'inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-700';
        const label = document.createElement('span');
        label.textContent = 'Showing: ';
        const strong = document.createElement('strong');
        strong.textContent = country;
        const pillClearBtn = document.createElement('button');
        pillClearBtn.className = 'ml-1 text-gray-400 hover:text-gray-700 cursor-pointer leading-none';
        pillClearBtn.setAttribute('aria-label', 'Clear country filter');
        pillClearBtn.textContent = '×';
        pillClearBtn.addEventListener('click', () => setCountry(null));
        label.appendChild(strong);
        span.appendChild(label);
        span.appendChild(pillClearBtn);
        pill.appendChild(span);
      } else {
        pill.classList.add('hidden');
        pill.innerHTML = '';
      }

      applyFilters();
      updateCompatibleTags();
    }

    tagButtons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const tag = btn.dataset.tag!;
        if (activeTags.has(tag)) {
          activeTags.delete(tag);
          setTagActive(tag, false);
        } else {
          activeTags.add(tag);
          setTagActive(tag, true);
          if (!panelOpen) openPanel();
        }
        updateBadge();
        applyFilters();
        updateCompatibleTags();
      });
    });

    clearBtn?.addEventListener('click', () => {
      activeTags.forEach((tag) => setTagActive(tag, false));
      activeTags.clear();
      updateBadge();
      applyFilters();
      updateCompatibleTags();
    });

    document.addEventListener('country-select', (e: Event) => {
      const country = (e as CustomEvent<{ country: string }>).detail.country;
      setCountry(country);
      document.getElementById('gallery')?.scrollIntoView({ behavior: 'smooth' });
    });
  }

  document.addEventListener('astro:page-load', initGallery);
  document.addEventListener('astro:page-load', initFilters);
</script>
```

- [ ] **Step 2: Verify build passes**

```bash
pnpm build
```

Expected: build succeeds, no TypeScript errors.

- [ ] **Step 3: Manual verification in dev server**

```bash
pnpm dev
```

Open `http://localhost:4321/photography` and verify:

1. Globe renders between the title and the tag filter panel
2. Hovering a country with photos shows the tooltip
3. Clicking a country hides photos from other countries, scrolls to the gallery, shows the country pill, and updates the tag filter panel to show only that country's tags
4. Clicking "×" on the pill clears the country filter and resets the tag panel to all tags
5. Selecting a tag while a country is active further filters, and the tag panel hides incompatible tags
6. Clearing tags while a country is active resets the tag panel to only that country's tags

- [ ] **Step 4: Commit**

```bash
git add src/pages/photography/index.astro
git commit -m "feat: unified filter controller with setCountry and dynamic tag panel"
```
