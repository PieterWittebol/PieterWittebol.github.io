---
name: new-content
description: Scaffold a new photography or woodworking content entry with correct frontmatter and file structure
---

Ask the user:
1. Content type: photography or woodworking?
2. Title
3. Date (YYYY-MM-DD)
4. Tags (comma-separated)

For **photography**, also ask:
- Image filename (e.g. `_3254135.jpg`) — the file should be placed next to the .md
- Location (optional)
- Camera (optional)

For **woodworking**, also ask:
- Short description (one sentence)

---

## Photography

Create `src/content/photography/<slug>.md` where `<slug>` is the title kebab-cased.

```markdown
---
title: "<title>"
date: <YYYY-MM-DD>
image: ./<image-filename>
tags: [<tags>]
location: "<location>"       # omit line if not provided
camera: "<camera>"           # omit line if not provided
draft: false
---
```

Note: `image` must be a relative path starting with `./` pointing to the image co-located in the same directory. Remind the user that the image file must be placed in the same directory as the `.md` file before running `pnpm build`, otherwise the build will fail with a missing asset error.

---

## Woodworking

Create `src/content/woodworking/<slug>/index.md` and remind the user to place images in `src/content/woodworking/<slug>/images/` with a `cover.jpg` as the cover image.

```markdown
---
title: "<title>"
description: "<description>"
date: <YYYY-MM-DD>
cover: ./images/cover.jpg
tags: [<tags>]
draft: true
---

Write your project post here.
```

Set `draft: true` by default so the post isn't published until the user is ready.
