# Landing Page Full-Viewport Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign `src/pages/index.astro` so the background photo fills the viewport below the header, with frosted glass navigation cards anchored to the bottom — no scrolling required.

**Architecture:** Single-file change. The hero section becomes a `min-h-[calc(100dvh-4rem)]` flex column. Title/tagline occupies the upper flex area; the three cards sit at the bottom with `backdrop-blur` frosted glass styling. The separate cards section below the hero is removed.

**Tech Stack:** Astro 5, Tailwind CSS 4, no JS changes required.

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `src/pages/index.astro` | Full page rewrite — hero height, layout, card styles |

---

### Task 1: Restructure hero section to fill viewport

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1: Start the dev server**

```bash
pnpm dev
```

Open `http://localhost:4321` in a browser. Confirm the current state: hero section with title, then scrolling down reveals the three white cards.

- [ ] **Step 2: Replace the hero `<section>` opening tag and overlay**

In `src/pages/index.astro`, replace:

```astro
  <!-- Hero -->
  <section id="hero" class="relative overflow-hidden bg-gray-900">
    <div class="absolute inset-0 bg-gradient-to-b from-black/55 to-black/65"></div>
    <div class="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-36 text-center">
      <p class="font-display text-sm font-medium tracking-widest uppercase text-white/60 mb-4 animate-fade-in">
        Welcome to
      </p>
      <h1 class="font-display text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 tracking-tight animate-slide-up delay-100">
        wittebol.be
      </h1>
      <p class="text-lg sm:text-xl text-white/70 max-w-xl mx-auto leading-relaxed animate-slide-up delay-200">
        A personal corner of the web where I share my professional background,
        photography, and woodworking projects.
      </p>
    </div>
  </section>
```

with:

```astro
  <!-- Hero -->
  <section id="hero" class="relative overflow-hidden bg-gray-900 min-h-[calc(100dvh-4rem)] flex flex-col">
    <div class="absolute inset-0 bg-gradient-to-b from-black/60 via-black/25 to-black/55"></div>

    <!-- Title / tagline -->
    <div class="relative flex-1 flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8">
      <p class="font-display text-sm font-medium tracking-widest uppercase text-white/60 mb-4 animate-fade-in">
        Welcome to
      </p>
      <h1 class="font-display text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 tracking-tight animate-slide-up delay-100">
        wittebol.be
      </h1>
      <p class="text-lg sm:text-xl text-white/70 max-w-xl mx-auto leading-relaxed animate-slide-up delay-200">
        A personal corner of the web where I share my professional background,
        photography, and woodworking projects.
      </p>
    </div>
  </section>
```

- [ ] **Step 3: Verify in browser**

The hero should now fill the full viewport height below the header. Title and tagline should be centered vertically. Background image (if a `background: true` photo exists) should cover the whole area. There are no cards yet.

---

### Task 2: Add frosted glass cards inside the hero

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1: Replace the separate cards section with a cards row inside the hero**

Remove the entire `<!-- Section cards -->` section:

```astro
  <!-- Section cards -->
  <section class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <!-- About -->
      <a
        href="/about"
        data-astro-prefetch
        class="group relative block p-8 rounded-2xl border border-gray-200 bg-white shadow-md hover:shadow-xl hover:border-amber-200 transition-all animate-scale-in delay-400"
      >
        <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-amber-50 text-amber-700 group-hover:bg-amber-100 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
          </svg>
        </div>
        <h2 class="text-lg font-bold text-gray-900 group-hover:text-amber-700 mb-2">
          About Me
        </h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          Who I am, what's my professional background, and what drives me.
        </p>
      </a>

      <!-- Photography -->
      <a
        href="/photography"
        data-astro-prefetch
        class="group relative block p-8 rounded-2xl border border-gray-200 bg-white shadow-md hover:shadow-xl hover:border-amber-200 transition-all animate-scale-in delay-500"
      >
        <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-amber-50 text-amber-700 group-hover:bg-amber-100 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Z" />
          </svg>
        </div>
        <h2 class="text-lg font-bold text-gray-900 group-hover:text-amber-700 mb-2">
          Photography
        </h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          A portfolio of moments captured through the lens.
        </p>
      </a>

      <!-- Woodworking -->
      <a
        href="/woodworking"
        data-astro-prefetch
        class="group relative block p-8 rounded-2xl border border-gray-200 bg-white shadow-md hover:shadow-xl hover:border-amber-200 transition-all animate-scale-in delay-600"
      >
        <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-amber-50 text-amber-700 group-hover:bg-amber-100 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.049.58.025 1.193-.14 1.743" />
          </svg>
        </div>
        <h2 class="text-lg font-bold text-gray-900 group-hover:text-amber-700 mb-2">
          Woodworking
        </h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          Project builds, tips, and reflections from the workshop.
        </p>
      </a>
    </div>
  </section>
```

And add the following **inside** the hero `<section>`, immediately after the closing `</div>` of the title area (before `</section>`):

```astro
    <!-- Frosted glass cards -->
    <div class="relative px-4 sm:px-6 lg:px-8 pb-8">
      <div class="grid gap-4 grid-cols-1 sm:grid-cols-3 max-w-6xl mx-auto">

        <!-- About -->
        <a
          href="/about"
          data-astro-prefetch
          class="group relative block p-6 rounded-2xl border border-white/20 bg-white/10 backdrop-blur-md hover:bg-white/20 hover:border-white/35 hover:shadow-xl transition-all animate-scale-in delay-400"
        >
          <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-white/15 text-white group-hover:bg-white/25 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
            </svg>
          </div>
          <h2 class="text-lg font-bold text-white mb-2">
            About Me
          </h2>
          <p class="text-white/70 text-sm leading-relaxed">
            Who I am, what's my professional background, and what drives me.
          </p>
        </a>

        <!-- Photography -->
        <a
          href="/photography"
          data-astro-prefetch
          class="group relative block p-6 rounded-2xl border border-white/20 bg-white/10 backdrop-blur-md hover:bg-white/20 hover:border-white/35 hover:shadow-xl transition-all animate-scale-in delay-500"
        >
          <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-white/15 text-white group-hover:bg-white/25 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Z" />
            </svg>
          </div>
          <h2 class="text-lg font-bold text-white mb-2">
            Photography
          </h2>
          <p class="text-white/70 text-sm leading-relaxed">
            A portfolio of moments captured through the lens.
          </p>
        </a>

        <!-- Woodworking -->
        <a
          href="/woodworking"
          data-astro-prefetch
          class="group relative block p-6 rounded-2xl border border-white/20 bg-white/10 backdrop-blur-md hover:bg-white/20 hover:border-white/35 hover:shadow-xl transition-all animate-scale-in delay-600"
        >
          <div class="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-white/15 text-white group-hover:bg-white/25 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.049.58.025 1.193-.14 1.743" />
            </svg>
          </div>
          <h2 class="text-lg font-bold text-white mb-2">
            Woodworking
          </h2>
          <p class="text-white/70 text-sm leading-relaxed">
            Project builds, tips, and reflections from the workshop.
          </p>
        </a>

      </div>
    </div>
```

- [ ] **Step 2: Verify in browser**

At `http://localhost:4321`, confirm:
- No scrollbar visible on desktop (viewport fills completely)
- Background photo covers the full hero area
- Title/tagline is vertically centered in the upper portion
- Three frosted glass cards are visible at the bottom of the viewport
- Cards have translucent blur effect over the background photo
- Hovering a card darkens it slightly and adds a shadow
- Clicking each card navigates to the correct page

Resize to mobile width (< 640px): cards should stack vertically and scroll is acceptable if they overflow.

- [ ] **Step 3: Run production build to confirm no build errors**

```bash
pnpm build
```

Expected: build completes with no errors. Ignore image optimization warnings if any.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: full-viewport hero with frosted glass cards on landing page"
```
