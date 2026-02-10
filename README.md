# wittebol.be

Personal website for [wittebol.be](https://wittebol.be) — a portfolio and blog built with Astro.

## Sections

- **About Me** — curriculum vitae with experience, education, skills, and languages
- **Photography** — photo gallery with PhotoSwipe lightbox viewer
- **Woodworking** — blog for project builds and workshop journal entries

## Tech Stack

- [Astro 5](https://astro.build) — static site generator
- [Svelte 5](https://svelte.dev) — interactive components (mobile nav)
- [Tailwind CSS 4](https://tailwindcss.com) — utility-first styling
- [PhotoSwipe 5](https://photoswipe.com) — image gallery lightbox
- [Sharp](https://sharp.pixelplumbing.com) — image optimization via `astro:assets`

## Project Structure

```
src/
├── components/         Reusable UI components
│   ├── Header.astro      Site header with navigation
│   ├── Footer.astro      Site footer
│   ├── Nav.svelte        Mobile hamburger menu
│   ├── PhotoCard.astro   Photo gallery thumbnail
│   ├── BlogCard.astro    Blog post card
│   └── SEO.astro         Meta/OG tags
├── content/            Markdown content collections
│   ├── about/            CV data and intro text
│   ├── photography/      Photo entries (markdown + co-located images)
│   └── woodworking/      Blog posts (markdown + co-located images)
├── content.config.ts   Collection schemas
├── layouts/
│   └── Layout.astro      Base HTML layout
├── pages/
│   ├── index.astro       Landing page
│   ├── about.astro       About Me / CV
│   ├── photography/      Photo gallery
│   └── woodworking/      Blog listing and post pages
└── styles/
    └── global.css        Tailwind theme and base styles
```

## Content Management

All content is managed via Markdown files in `src/content/`:

- **Photography**: one `.md` file per photo with frontmatter (title, date, location, camera, tags) and a co-located image
- **Woodworking**: one folder per post with `index.md` and an `images/` directory for inline photos
- **About**: a single `index.md` with structured CV data in YAML frontmatter and an intro paragraph as the body

## Commands

All commands are run from the project root:

| Command                | Action                                       |
| :--------------------- | :------------------------------------------- |
| `pnpm install`         | Install dependencies                         |
| `pnpm dev --host`      | Start dev server at `localhost:4321`          |
| `pnpm build`           | Build production site to `./dist/`           |
| `pnpm preview --host`  | Preview the production build locally         |
