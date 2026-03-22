# Visual Refresh — Refined Warm Elegance — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade wittebol.be with Lora body font, an amber/sand complementary accent palette, and scroll-triggered + hover animations — all while preserving the existing warm character.

**Architecture:** Typography is switched by changing `--font-sans` in the Tailwind theme and restricting Playwrite NZ to a `.font-display` utility class. Amber tokens are added as a new `--color-amber-*` scale. Scroll animations are driven by a single `IntersectionObserver` module (`reveal.ts`) that reads `data-reveal` attributes and is re-initialised on every `astro:page-load` event (supporting ClientRouter page transitions).

**Tech Stack:** Astro 5, Svelte 5, Tailwind CSS 4 (via Vite plugin, no config file), `@fontsource-variable/lora`, vanilla TypeScript.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `src/styles/global.css` | Modify | Font imports, theme tokens (amber scale + font-sans), `.font-display`, `.nav-link`, `.reveal` / `.reveal.is-visible` |
| `src/scripts/reveal.ts` | **Create** | IntersectionObserver scroll-reveal module |
| `src/layouts/Layout.astro` | Modify | Wire in `reveal.ts` script |
| `src/components/Header.astro` | Modify | Logo gets `.font-display`; desktop nav links get `.nav-link` sliding underline |
| `src/components/Footer.astro` | Modify | Brand span: `text-accent-700` → `text-amber-700` |
| `src/components/BlogCard.astro` | Modify | Tags: `bg-accent-50 text-accent-700` → `bg-amber-50 text-amber-700` |
| `src/pages/index.astro` | Modify | "Welcome to" tagline gets `.font-display`; section cards get amber hover |
| `src/pages/about.astro` | Modify | Section headings: remove page-load animations, add `data-reveal="left"`; experience entries get `data-reveal-group`; skill tags get amber |
| `src/pages/photography/index.astro` | Modify | `h1` gets `data-reveal="left"`; remove per-card animate wrappers; grid gets `data-reveal-group` |
| `src/pages/woodworking/index.astro` | Modify | Same as photography |
| `src/pages/woodworking/[slug].astro` | Modify | Tags: `bg-accent-50 text-accent-700` → `bg-amber-50 text-amber-700` |

---

## Task 1: Install Lora Font Package

**Files:**
- No file edits — package install only

- [ ] **Step 1: Install the package**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io
pnpm add @fontsource-variable/lora
```

Expected: package added to `dependencies` in `package.json`, no errors.

- [ ] **Step 2: Verify install**

```bash
ls node_modules/@fontsource-variable/lora
```

Expected: directory exists with font files inside.

---

## Task 2: Update Global CSS + Header (single commit — critical ordering)

> ⚠️ **These two files must change in the same commit.** Changing `--font-sans` without updating the Header logo will cause the logo to briefly render in Lora until the second commit lands. Always stage both files together.

**Files:**
- Modify: `src/styles/global.css`
- Modify: `src/components/Header.astro`

### global.css changes

- [ ] **Step 1: Open `src/styles/global.css` and make the following changes**

**a) Add the Lora import** directly after the Playwrite NZ import on line 1:

```css
@import "@fontsource-variable/playwrite-nz";
@import "@fontsource-variable/lora";
```

**b) Change `--font-sans`** in the `@theme` block (currently line 7):

```css
/* Before */
--font-sans: "Playwrite NZ", "Segoe UI", "Roboto", sans-serif;

/* After */
--font-sans: "Lora Variable", "Georgia", serif;
```

**c) Add the amber colour scale** to the `@theme` block, after the existing accent scale:

```css
/* Amber/sand complementary scale */
--color-amber-50:  #fffbeb;
--color-amber-100: #fef3c7;
--color-amber-200: #fde68a;
--color-amber-300: #fcd34d;
--color-amber-400: #fbbf24;
--color-amber-500: #f59e0b;
--color-amber-600: #d97706;
--color-amber-700: #b45309;
--color-amber-800: #92400e;
--color-amber-900: #78350f;
```

**d) Add `.font-display` utility and `.nav-link` styles** inside `@layer utilities` (after the existing delay helpers):

```css
.font-display {
  font-family: "Playwrite NZ Variable", cursive;
}

/* Sliding underline for desktop nav links */
.nav-link {
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-amber-400);
  transition: width 0.2s ease;
}

.nav-link:hover::after,
.nav-link.is-active::after {
  width: 100%;
}
```

**e) Add `.reveal` scroll styles** inside `@layer utilities`, after the `.nav-link` block:

```css
/* Scroll-triggered reveal */
.reveal {
  opacity: 0;
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.reveal[data-reveal="up"] {
  transform: translateY(20px);
}

.reveal[data-reveal="left"] {
  transform: translateX(-20px);
}

.reveal.is-visible {
  opacity: 1;
  transform: none;
}
```

### Header.astro changes

- [ ] **Step 2: Open `src/components/Header.astro` and make these changes**

**a) Add `font-display` to the logo span** (line 34). Change:

```astro
<span class="text-xl font-bold text-white group-hover:text-accent-200 transition-colors tracking-tight">
  Wittebol
</span>
```

To:

```astro
<span class="font-display text-xl font-bold text-white group-hover:text-accent-200 transition-colors tracking-tight">
  Wittebol
</span>
```

**b) Replace the desktop nav link classes** (lines 41–54). Change the entire `<nav>` block:

```astro
<!-- Desktop navigation -->
<nav class="hidden md:flex items-center gap-8" aria-label="Main navigation">
  {links.map(({ href, label }) => (
    <a
      href={href}
      data-astro-prefetch
      class:list={[
        'text-sm font-medium transition-colors',
        currentPath === href || (href !== '/' && currentPath.startsWith(href))
          ? 'text-white border-b-2 border-accent-300 pb-0.5'
          : 'text-accent-200 hover:text-white',
      ]}
    >
      {label}
    </a>
  ))}
</nav>
```

To:

```astro
<!-- Desktop navigation -->
<nav class="hidden md:flex items-center gap-8" aria-label="Main navigation">
  {links.map(({ href, label }) => (
    <a
      href={href}
      data-astro-prefetch
      class:list={[
        'nav-link text-sm font-medium transition-colors pb-0.5',
        currentPath === href || (href !== '/' && currentPath.startsWith(href))
          ? 'text-white is-active'
          : 'text-accent-200 hover:text-white',
      ]}
    >
      {label}
    </a>
  ))}
</nav>
```

- [ ] **Step 3: Audit all `font-sans` usages**

```bash
grep -r "font-sans" /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io/src/
```

Expected: only the `body` rule in `global.css` and possibly no other files. If any file uses `font-sans` to intentionally render in Playwrite NZ, add `font-display` to that element too.

- [ ] **Step 4: Verify build passes**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

Expected: build completes without errors.

- [ ] **Step 5: Commit both files together**

```bash
git add src/styles/global.css src/components/Header.astro
git commit -m "feat: switch body font to Lora, add amber palette, add nav underline, add reveal CSS"
```

---

## Task 3: Create the Scroll-Reveal Script

**Files:**
- Create: `src/scripts/reveal.ts`

- [ ] **Step 1: Create the file**

Create `src/scripts/reveal.ts` with this content:

```typescript
let observer: IntersectionObserver | null = null;

function setupReveal(): void {
  // Disconnect any previous observer
  if (observer) observer.disconnect();

  // Handle data-reveal-group: write data-reveal="up" + staggered delays onto each direct child
  document.querySelectorAll('[data-reveal-group]').forEach((group) => {
    Array.from(group.children).forEach((child, i) => {
      child.setAttribute('data-reveal', 'up');
      (child as HTMLElement).style.transitionDelay = `${i * 80}ms`;
    });
  });

  // Observe all [data-reveal] elements
  const elements = document.querySelectorAll<HTMLElement>('[data-reveal]');

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer?.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
  );

  elements.forEach((el) => {
    el.classList.add('reveal');
    observer!.observe(el);
  });
}

// Strip is-visible from the incoming document BEFORE the swap so cached pages
// (e.g. back-navigation) don't arrive with elements already in their visible state.
// This fires during the view-transition animation — while the outgoing page exits
// and the incoming page enters — so the new content starts hidden and reveals fresh.
document.addEventListener('astro:before-swap', (event) => {
  const incoming = (event as CustomEvent & { newDocument: Document }).newDocument;
  incoming.querySelectorAll('.is-visible').forEach((el) => el.classList.remove('is-visible'));
});

// Re-run on every page load (initial load + ClientRouter navigations)
document.addEventListener('astro:page-load', setupReveal);
```

- [ ] **Step 2: Verify the file exists**

```bash
cat /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io/src/scripts/reveal.ts
```

Expected: file prints the content above.

- [ ] **Step 3: Commit**

```bash
git add src/scripts/reveal.ts
git commit -m "feat: add IntersectionObserver scroll-reveal script"
```

---

## Task 4: Wire Reveal Script into Layout

**Files:**
- Modify: `src/layouts/Layout.astro`

- [ ] **Step 1: Add the script tag to `src/layouts/Layout.astro`**

The current `<body>` ends with `<Footer>` and then `</body>`. Add a `<script>` import just before `</body>`:

```astro
    <Footer transition:animate="none" />
    <script>
      import '../scripts/reveal.ts';
    </script>
  </body>
```

The full updated `Layout.astro` should look like:

```astro
---
import { ClientRouter } from 'astro:transitions';
import '../styles/global.css';
import SEO from '../components/SEO.astro';
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';

interface Props {
  title: string;
  description?: string;
  ogImage?: string;
  ogType?: 'website' | 'article';
}

const { title, description, ogImage, ogType } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="generator" content={Astro.generator} />
    <SEO title={title} description={description} ogImage={ogImage} ogType={ogType} />
    <ClientRouter />
  </head>
  <body class="min-h-screen flex flex-col">
    <Header transition:animate="none" />
    <main class="flex-1" transition:animate="slide">
      <slot />
    </main>
    <Footer transition:animate="none" />
    <script>
      import '../scripts/reveal.ts';
    </script>
  </body>
</html>
```

- [ ] **Step 2: Verify build passes**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add src/layouts/Layout.astro
git commit -m "feat: wire scroll-reveal script into layout"
```

---

## Task 5: Update Homepage (index.astro)

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1: Add `font-display` to the "Welcome to" tagline**

Line 10. Change:

```astro
<p class="text-sm font-medium tracking-widest uppercase text-gray-400 mb-4 animate-fade-in">
  Welcome to
</p>
```

To:

```astro
<p class="font-display text-sm font-medium tracking-widest uppercase text-gray-400 mb-4 animate-fade-in">
  Welcome to
</p>
```

- [ ] **Step 2: Update the three section cards with amber hover**

For each card `<a>` (About, Photography, Woodworking), add `hover:border-amber-200` to the `class` and change `group-hover:bg-accent-100` to `group-hover:bg-amber-50` on the icon container.

**About card** (line 30–43). Change:

```astro
<a
  href="/about"
  data-astro-prefetch
  class="group relative block p-8 rounded-2xl border border-gray-200 bg-white shadow-md hover:shadow-xl hover:border-gray-300 transition-all animate-scale-in delay-400"
>
  <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-accent-50 text-accent-700 group-hover:bg-accent-100 transition-colors">
```

To:

```astro
<a
  href="/about"
  data-astro-prefetch
  class="group relative block p-8 rounded-2xl border border-gray-200 bg-white shadow-md hover:shadow-xl hover:border-amber-200 transition-all animate-scale-in delay-400"
>
  <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-accent-50 text-accent-700 group-hover:bg-amber-50 transition-colors">
```

**Photography card** (line 49). Apply the same two class changes:
- `hover:border-gray-300` → `hover:border-amber-200`
- `group-hover:bg-accent-100` → `group-hover:bg-amber-50`

**Woodworking card** (line 69). Apply the same two class changes.

- [ ] **Step 3: Verify build**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: homepage — display font on tagline, amber card hovers"
```

---

## Task 6: Update Footer and BlogCard (amber accents)

**Files:**
- Modify: `src/components/Footer.astro`
- Modify: `src/components/BlogCard.astro`

- [ ] **Step 1: Update Footer brand text**

In `src/components/Footer.astro` line 8, change:

```astro
<span class="text-accent-700">wittebol</span>
```

To:

```astro
<span class="text-amber-700">wittebol</span>
```

- [ ] **Step 2: Update BlogCard tags**

In `src/components/BlogCard.astro` line 46, change:

```astro
<span class="px-2 py-0.5 text-xs bg-accent-50 text-accent-700 rounded-full">
```

To:

```astro
<span class="px-2 py-0.5 text-xs bg-amber-50 text-amber-700 rounded-full">
```

- [ ] **Step 3: Verify build**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

- [ ] **Step 4: Commit**

```bash
git add src/components/Footer.astro src/components/BlogCard.astro
git commit -m "feat: amber accent on footer brand text and blog card tags"
```

---

## Task 7: Update About Page

**Files:**
- Modify: `src/pages/about.astro`

Changes: remove existing page-load animations from section headings (they conflict with scroll-reveal), add `data-reveal="left"` to section headings, `data-reveal-group` to experience entries, amber skill tags.

- [ ] **Step 1: Update the Experience heading** (line 49)

Change:

```astro
<h2 class="text-xl font-bold text-gray-800 mb-6 border-b border-gray-200 pb-2 animate-slide-in-left">
  Experience
</h2>
```

To:

```astro
<h2 class="text-xl font-bold text-gray-800 mb-6 border-b border-gray-200 pb-2" data-reveal="left">
  Experience
</h2>
```

- [ ] **Step 2: Add `data-reveal-group` to the experience entries container** (line 52)

Change:

```astro
<div class="space-y-6">
  {experience.map(({ role, company, period, description, assignments }) => (
```

To:

```astro
<div class="space-y-6" data-reveal-group>
  {experience.map(({ role, company, period, description, assignments }) => (
```

- [ ] **Step 3: Update the Education heading** (line 76)

Change:

```astro
<h2 class="text-xl font-bold text-gray-800 mb-6 border-b border-gray-200 pb-2 animate-slide-in-left">
  Education
</h2>
```

To:

```astro
<h2 class="text-xl font-bold text-gray-800 mb-6 border-b border-gray-200 pb-2" data-reveal="left">
  Education
</h2>
```

- [ ] **Step 4: Add `data-reveal="left"` to the three sidebar section headings**

Certifications heading (line 94):

```astro
<h2 class="text-xl font-bold text-gray-800 mb-4 border-b border-gray-200 pb-2" data-reveal="left">
  Certifications
</h2>
```

Skills heading (line 106):

```astro
<h2 class="text-xl font-bold text-gray-800 mb-4 border-b border-gray-200 pb-2" data-reveal="left">
  Skills
</h2>
```

Languages heading (line 120):

```astro
<h2 class="text-xl font-bold text-gray-800 mb-4 border-b border-gray-200 pb-2" data-reveal="left">
  Languages
</h2>
```

- [ ] **Step 5: Update skill tags to amber** (line 111)

Change:

```astro
<span class="px-3 py-1 text-xs font-medium bg-accent-50 text-accent-800 rounded-full">
```

To:

```astro
<span class="px-3 py-1 text-xs font-medium bg-amber-50 text-amber-800 rounded-full">
```

- [ ] **Step 6: Verify build**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

- [ ] **Step 7: Commit**

```bash
git add src/pages/about.astro
git commit -m "feat: about page — scroll-reveal on section headings, amber skill tags"
```

---

## Task 8: Update Photography Page

**Files:**
- Modify: `src/pages/photography/index.astro`

Changes: `h1` gets scroll-reveal; replace per-card `animate-scale-in` wrappers with `data-reveal-group` on the grid.

- [ ] **Step 1: Update the `h1`** (line 28)

Change:

```astro
<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-10 animate-fade-in">
  Photography
</h1>
```

To:

```astro
<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-10" data-reveal="left">
  Photography
</h1>
```

- [ ] **Step 2: Replace per-card animate wrappers with `data-reveal-group` on the grid**

Change the grid and map (lines 33–49):

```astro
<div id="gallery" class="pswp-gallery grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
  {photosWithFull.map((photo, index) => (
    <div class="animate-scale-in" style={`animation-delay: ${index * 80}ms`}>
      <PhotoCard
        image={photo.data.image}
        title={photo.data.title}
        location={photo.data.location}
        camera={photo.data.camera}
        tags={photo.data.tags}
        fullSrc={photo.full.src}
        fullWidth={photo.full.width}
        fullHeight={photo.full.height}
        index={index}
      />
    </div>
  ))}
</div>
```

To:

```astro
<div id="gallery" class="pswp-gallery grid gap-4 sm:grid-cols-2 lg:grid-cols-3" data-reveal-group>
  {photosWithFull.map((photo, index) => (
    <PhotoCard
      image={photo.data.image}
      title={photo.data.title}
      location={photo.data.location}
      camera={photo.data.camera}
      tags={photo.data.tags}
      fullSrc={photo.full.src}
      fullWidth={photo.full.width}
      fullHeight={photo.full.height}
      index={index}
    />
  ))}
</div>
```

Note: `index` prop is still passed — PhotoCard uses it for `loading="eager"` on the first 6 images.

- [ ] **Step 3: Verify build**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

- [ ] **Step 4: Commit**

```bash
git add src/pages/photography/index.astro
git commit -m "feat: photography page — scroll-reveal on heading and photo grid"
```

---

## Task 9: Update Woodworking Pages

**Files:**
- Modify: `src/pages/woodworking/index.astro`
- Modify: `src/pages/woodworking/[slug].astro`

### woodworking/index.astro

- [ ] **Step 1: Update the `h1`** (line 13)

Change:

```astro
<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-10 animate-fade-in">
  Woodworking
</h1>
```

To:

```astro
<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-10" data-reveal="left">
  Woodworking
</h1>
```

- [ ] **Step 2: Replace per-card animate wrappers with `data-reveal-group` on the grid** (lines 18–29)

> ⚠️ The grid is inside a `{posts.length > 0 ? ( ... ) : ( ... )}` ternary. Replace **only the inner `<div>` and its children** — do NOT remove the surrounding conditional or the empty-state fallback branch.

Change only the inner `<div>` block (inside the truthy branch):

```astro
<div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
  {posts.map((post, index) => (
    <div class="animate-scale-in" style={`animation-delay: ${index * 100}ms`}>
      <BlogCard
        slug={post.id}
        title={post.data.title}
        description={post.data.description}
        date={post.data.date}
        cover={post.data.cover}
        tags={post.data.tags}
      />
    </div>
  ))}
</div>
```

To:

```astro
<div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3" data-reveal-group>
  {posts.map((post) => (
    <BlogCard
      slug={post.id}
      title={post.data.title}
      description={post.data.description}
      date={post.data.date}
      cover={post.data.cover}
      tags={post.data.tags}
    />
  ))}
</div>
```

The empty-state `<div class="text-center py-24 animate-fade-in">` branch stays unchanged.

### woodworking/[slug].astro

> **Note on spec line "Section headings: `data-reveal="left"`":** The `[slug].astro` page has no template-level `<h2>` section headings — all body headings are inside `<Content />` (rendered markdown prose) and are not accessible to the page template. The page-level `<h1>` title is above the fold and already has a page-load animation (`animate-slide-up`). There is nothing to add `data-reveal` to at the template level; this spec line is a no-op for this file.

- [ ] **Step 3: Update tags to amber** (line 56)

Change:

```astro
<span class="px-2.5 py-0.5 text-xs font-medium bg-accent-50 text-accent-700 rounded-full">
```

To:

```astro
<span class="px-2.5 py-0.5 text-xs font-medium bg-amber-50 text-amber-700 rounded-full">
```

- [ ] **Step 4: Verify build**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

- [ ] **Step 5: Commit**

```bash
git add src/pages/woodworking/index.astro src/pages/woodworking/\[slug\].astro
git commit -m "feat: woodworking pages — scroll-reveal on heading and grid, amber tags"
```

---

## Final Verification

- [ ] **Run a full production build**

```bash
cd /Users/pieterwittebol/Documents/Projects/PieterWittebol.github.io && pnpm build
```

Expected: exits 0, no TypeScript or Astro errors.

- [ ] **Start the dev server and smoke-test visually**

```bash
pnpm dev
```

Check each page:
1. **Homepage** — "Welcome to" renders in Playwrite NZ cursive; "wittebol.be" h1 renders in Lora; three cards have amber border on hover; nav links show amber sliding underline on hover/active.
2. **About** — Body text in Lora; section headings animate in from the left as you scroll; experience entries stagger in; skill tags are amber.
3. **Photography** — Page heading slides in from left; photos reveal staggered as you scroll down.
4. **Woodworking index** — Same as photography.
5. **Woodworking article** — Tags are amber.
6. **Footer** — "wittebol" span is amber-700.
7. **Navigate between pages** — Scroll reveals re-trigger on each navigation (don't stay visible from previous visit).
8. **Reduced motion** — Open DevTools > Rendering > Enable "Emulate CSS prefers-reduced-motion: reduce". All animations should be instantaneous.
