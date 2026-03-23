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
- Camera (optional)

For **woodworking**, also ask:
- Short description (one sentence)

---

## Photography — Auto-Analysis

When the user provides an image file path, **run the analysis script first** before asking for title, tags, location, or camera:

```bash
python3 .claude/skills/new-content/analyze_photo.py <image_path>
```

The script outputs JSON. Use its values as pre-filled defaults. Present them to the user for confirmation:

```
Detected from photo:
  Date:     2023-03-25         (from EXIF)
  Camera:   Olympus OM-D E-M5 Mark II  (from EXIF)
  Location: South Africa       (from GPS)
  Title:    African Penguin    (Claude suggestion)
  Tags:     wildlife, south africa  (Claude suggestion)

Press Enter to accept each, or type a replacement.
```

If the script fails or a field is missing, fall back to asking the user.

### Dependencies

The script requires:
```bash
pip install Pillow anthropic   # required
pip install geopy              # optional — enables GPS → location name
```

Dependencies are installed in the conda environment `website`. Run the script via:
```bash
conda run -n website python3 .claude/skills/new-content/analyze_photo.py <image_path>
```

The script needs `ANTHROPIC_API_KEY` for vision inference. **Claude Code authenticates via OAuth (macOS Keychain), not a plain API key**, so the script's Claude step will fail in this environment. When it does, **skip the script's vision step and use the Read tool directly** — Claude Code is multimodal and can analyze the image itself. EXIF fields (date, camera) will still come from the script; title, tags, and location come from Claude's own analysis.

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
camera: "<camera>"           # omit line if not provided
draft: false
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
