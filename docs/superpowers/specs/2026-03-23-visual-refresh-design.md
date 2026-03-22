# Visual Refresh — Refined Warm Elegance

**Date:** 2026-03-23
**Status:** Approved

## Goal

Increase the general appeal of wittebol.be for all visitors by improving typography readability, adding a complementary amber accent, and introducing scroll-triggered animations — while preserving the warm, earthy character of the site.

## Typography

### Fonts

| Role | Font | Usage |
|------|------|-------|
| Display / accent | Playwrite NZ (existing) | Logo text in header, "Welcome to" hero tagline only |
| Body / prose | Lora (variable, Google Fonts) | All body text, headings, prose content |
| UI / utility | Inter (system fallback) | Nav links, labels, tags, metadata |

**Rationale:** Playwrite NZ is a cursive script — beautiful but low readability at body sizes. Moving it to display-only preserves personality while making the site accessible to users with dyslexia or visual impairments. Lora is a warm, editorial serif that harmonises with the earthy palette.

**Implementation:** Add `@fontsource-variable/lora` package. Add a `.font-display` utility class in global CSS that applies Playwrite NZ. Remove Playwrite NZ from the `--font-sans` theme variable; replace with Lora as primary, Inter as fallback.

## Color Palette

### Existing (unchanged)

- **Gray scale** (`--color-gray-50` → `--color-gray-950`): warm zinc tones, used for backgrounds, text, borders
- **Accent / burgundy scale** (`--color-accent-50` → `--color-accent-950`): deep red-burgundy, used for header background, active nav, links

### New — Amber/Sand scale

Added as `--color-amber-*` in the `@theme` block:

```
--color-amber-50:  #fffbeb
--color-amber-100: #fef3c7
--color-amber-200: #fde68a
--color-amber-300: #fcd34d
--color-amber-400: #fbbf24
--color-amber-500: #f59e0b
--color-amber-600: #d97706
--color-amber-700: #b45309
--color-amber-800: #92400e
--color-amber-900: #78350f
```

**Usage rules:**
- Skill/tag badges: `bg-amber-50 text-amber-800` (replaces current `bg-accent-50 text-accent-800`)
- Card hover border tint: `hover:border-amber-200`
- Nav sliding underline: amber-400
- Footer brand text "wittebol": `text-amber-700` (replaces `text-accent-700`)
- Section dividers / decorative accents: amber-200
- Never used as a background for large areas — complementary only

## Animations

### Page Load (existing, refined)

- Hero "Welcome to" tagline: `animate-fade-in` (unchanged)
- Hero `h1`: `animate-slide-up delay-100` (unchanged)
- Hero paragraph: `animate-slide-up delay-200` (unchanged)
- Homepage cards: `animate-scale-in` with staggered delays (unchanged)
- Page `h1` headings: `animate-slide-in-left` (unchanged)

### Scroll-triggered (new)

**Mechanism:** A small vanilla JS module (`src/scripts/reveal.ts`, ~30 lines) using `IntersectionObserver`. Applied once via a `<script>` tag in `Layout.astro`. Re-initialised on `astro:page-load` to support ClientRouter transitions.

**API:**
- `data-reveal="fade"` — opacity 0 → 1
- `data-reveal="up"` — opacity 0 + translateY(20px) → visible
- `data-reveal="left"` — opacity 0 + translateX(-20px) → visible
- `data-reveal-group` — parent attribute; auto-applies `data-reveal="up"` to each direct child with 80ms incremental delay

**CSS:** `.reveal` sets initial hidden state; `.reveal.is-visible` sets final visible state with a `transition: opacity 0.5s ease, transform 0.5s ease`.

**Reduced motion:** The existing `prefers-reduced-motion` reset in `global.css` already collapses all transition durations to 0.01ms — no additional work needed.

**Observer options:** `threshold: 0.12`, `rootMargin: "0px 0px -40px 0px"` — triggers slightly before element fully enters viewport for a natural feel.

### Hover Interactions (enhanced)

**Nav links (desktop):**
- Remove static `border-b-2 border-accent-300` active state
- Add CSS sliding underline via `::after` pseudo-element: `width: 0 → 100%` on hover, amber-400 color
- Active link: underline always visible (width: 100%, amber-400)

**Cards (homepage):**
- Keep existing `shadow-md → shadow-xl` on hover
- Add `hover:border-amber-200 transition-colors` for warm border shift

**Photo cards:**
- Existing scale + overlay fade kept unchanged — already polished

## Component-by-Component Changes

### `src/styles/global.css`
- Add `@import "@fontsource-variable/lora"`
- Change `--font-sans` to `"Lora Variable", "Georgia", serif`
- Add amber color scale to `@theme`
- Add `.font-display { font-family: "Playwrite NZ Variable", cursive; }` utility
- Add `.reveal` / `.reveal.is-visible` base styles

### `src/scripts/reveal.ts` (new file)
- IntersectionObserver logic
- Handles `data-reveal` and `data-reveal-group`
- Re-init on `astro:page-load`

### `src/layouts/Layout.astro`
- Import and inline the reveal script (or `<script src>`)

### `src/components/Header.astro`
- Logo span: add `font-display` class (Playwrite NZ)
- Nav links: replace active border with sliding underline via CSS class
- Active link: amber underline

### `src/pages/index.astro`
- Hero "Welcome to": add `font-display` class
- Section cards: add `hover:border-amber-200` on anchor elements
- Icon hover: change `group-hover:bg-accent-100` → `group-hover:bg-amber-50`

### `src/pages/photography/index.astro`
- `h1`: add `data-reveal="left"`
- Grid wrapper: add `data-reveal-group` (or per-item `data-reveal="up"` with index-based delay)

### `src/pages/woodworking/index.astro`
- Same treatment as photography

### `src/pages/woodworking/[slug].astro`
- Section headings: `data-reveal="left"`

### `src/pages/about.astro`
- Section headings (Experience, Education, Certifications, Skills, Languages): `data-reveal="left"`
- Experience entries wrapper: `data-reveal-group`
- Skill tags: `bg-amber-50 text-amber-800` (replaces accent)

### `src/components/Footer.astro`
- `text-accent-700` → `text-amber-700` on "wittebol" span

## Accessibility Notes

- All animation durations collapse to near-zero under `prefers-reduced-motion`
- Lora at body sizes meets WCAG AA contrast requirements against the #f5f2ed background
- Amber-800 on amber-50 badge combo: contrast ratio ~7:1 (AAA)
- No animation conveys information — purely decorative

## Out of Scope

- Dark mode
- New pages or content sections
- Layout restructuring
- JavaScript framework changes
