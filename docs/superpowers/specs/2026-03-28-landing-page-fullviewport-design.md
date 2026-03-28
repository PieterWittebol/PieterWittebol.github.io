# Landing Page Full-Viewport Redesign

**Date:** 2026-03-28
**Status:** Approved

## Goal

Eliminate scrolling on the landing page. The background photo should fill the entire visible area below the header, with the three navigation cards integrated into the image via a frosted glass treatment at the bottom of the viewport.

## Approach

Approach A: hero fills remaining viewport height. The header stays as-is (sticky, `h-16` / 4rem). The hero section is `h-[calc(100dvh-4rem)]` so it exactly fills the remaining viewport. No changes to `Layout.astro`.

## Layout Structure

```
<header>                  ← unchanged, h-16, sticky top-0
<section id="hero">       ← h-[calc(100dvh-4rem)], flex flex-col, bg image + overlay
  <div>                   ← flex-1, flex items-center justify-center
    title + tagline       ← centered vertically in upper area
  </div>
  <div>                   ← bottom cards row, pb-8 px-4 sm:px-6 lg:px-8
    grid of 3 cards       ← frosted glass
  </div>
</section>
```

The separate `<section>` containing the cards below the hero is removed entirely.

The hero uses `min-h-[calc(100dvh-4rem)]` (not `h-`) so that on mobile, stacked cards can grow the section naturally rather than clipping.

## Background & Overlay

- Background image applied via existing JS (`applyHeroBg`), no changes needed.
- Overlay gradient: `bg-gradient-to-b from-black/60 via-black/25 to-black/55`
  - Darker at top: ensures title/tagline text is legible.
  - Lighter in the middle: lets the photo breathe.
  - Darker at bottom: provides contrast behind the frosted cards.

## Title / Tagline Area

Unchanged content. Styling adjustments only:
- Wrapper: `flex-1 flex flex-col items-center justify-center text-center px-4`
- All existing animation classes (`animate-fade-in`, `animate-slide-up`, delay classes) retained.

## Frosted Glass Cards

Each card (`<a>` element) gets:
- `backdrop-blur-md bg-white/10 border border-white/20 rounded-2xl p-6`
- Hover: `hover:bg-white/20 hover:border-white/35 hover:shadow-xl`
- All text: `text-white` (title) and `text-white/70` (description)
- Icon wrapper: `bg-white/15` background, `text-white` icon color
- Icon hover: `group-hover:bg-white/25`
- Existing `animate-scale-in` and delay classes retained.

Card grid wrapper:
- `grid gap-4 grid-cols-1 sm:grid-cols-3 w-full max-w-6xl mx-auto pb-8`

## Responsive Behavior

- **Mobile (`< sm`):** Cards stack vertically (`grid-cols-1`). Because the hero uses `min-h`, stacked cards grow the section naturally — scroll only happens on very small screens.
- **`sm` and above:** All three cards sit in one row within the viewport height. No scroll.

## Files Changed

- `src/pages/index.astro` — only file modified. No changes to Layout, Header, or any component.

## Out of Scope

- Header transparency / overlay (Approach B) — deferred.
- Any changes to the photography, woodworking, or about pages.
