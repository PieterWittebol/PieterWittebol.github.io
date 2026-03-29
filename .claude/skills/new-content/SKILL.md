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
- Image file path — used both to run analysis and as the co-located asset
- Location (optional)
- Country (optional) — ISO country name (e.g. "Belgium", "South Africa"); enables globe filtering on /photography
- Camera (optional)
- Background? (optional, default false) — set to `true` if this photo should be eligible for the landing page hero rotation

For **woodworking**, also ask:
- Short description (one sentence)

---

## Photography — Auto-Analysis

When the user provides an image file path:

1. **Run the analysis script** to extract EXIF metadata:
   ```bash
   conda run -n website python3 .claude/skills/new-content/analyze_photo.py <image_path>
   ```
   This outputs JSON with `date`, `camera`, and `location` (if GPS is present).

2. **Read the image directly** using the Read tool to infer title, tags, and description — Claude Code is multimodal and analyzes the image itself.

Combine both sources as pre-filled defaults and present them to the user for confirmation:

```
Detected from photo:
  Date:     2023-03-25              (from EXIF)
  Camera:   Olympus OM-D E-M5 Mark II  (from EXIF)
  Location: South Africa            (from GPS)
  Title:    African Penguin         (Claude suggestion)
  Tags:     wildlife, south africa  (Claude suggestion)

Press Enter to accept each, or type a replacement.
```

If the script fails or a field is missing, fall back to asking the user.

### Dependencies

The script requires:
```bash
pip install Pillow
pip install geopy  # optional — enables GPS → location name
```

Dependencies are installed in the conda environment `website`.

---

## Photography — Output

Create `src/content/photography/<slug>.md` where `<slug>` is the title kebab-cased.

```markdown
---
title: "<title>"
date: <YYYY-MM-DD>
image: ./<image-filename>
tags: [<tags>]
location: "<location>"       # omit line if not provided
country: "<country>"         # omit line if not provided
camera: "<camera>"           # omit line if not provided
draft: false
background: false            # set true to include in landing page hero rotation
---
```

`image` must be a relative path starting with `./` — just the filename, not the full path. Remind the user that the image file must be placed in `src/content/photography/` before running `pnpm build`, otherwise the build will fail with a missing asset error.

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
