# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pnpm dev          # Start dev server at localhost:4321
pnpm build        # Build production site to ./dist/
pnpm preview      # Preview production build locally
```

Package manager is **pnpm**. There are no test commands.

## Architecture

This is a personal portfolio/blog site built with **Astro 5**, **Svelte 5**, and **Tailwind CSS 4**. It deploys automatically to GitHub Pages (https://wittebol.be) on push to `master` via GitHub Actions.

### Content Collections

Content lives in `src/content/` as Markdown files. Schemas are defined in `src/content.config.ts`:

- **photography** — individual `.md` files per photo with co-located images; frontmatter includes `title`, `date`, `image`, `alt`, `tags`
- **woodworking** — each project is a folder with `index.md` and an `images/` subdirectory; frontmatter includes `title`, `date`, `description`, `coverImage`, `tags`
- **about** — single `index.md` for the CV/about page

### Pages & Routing

`src/pages/` maps directly to routes. Pages fetch content via Astro's `getCollection()` API and pass it to components.

### Components

`src/components/` contains reusable Astro and Svelte components. Svelte is used for interactive elements (e.g., PhotoSwipe gallery). Static layout/UI pieces are Astro components.

### Styling

Tailwind CSS 4 is configured via the Vite plugin (no `tailwind.config.js`). Global styles and theme customizations are in `src/styles/`. The `@tailwindcss/typography` plugin styles Markdown-rendered content.

### Image Handling

Sharp handles image optimization at build time. PhotoSwipe 5 provides the lightbox gallery for the photography section.
