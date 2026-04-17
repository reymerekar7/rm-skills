---
name: one-stack-newsletter-assets
description: >
  Generates visual assets for One Stack newsletter issues: thumbnails (1200×630 PNG)
  and Excalidraw diagrams. Reads brand context automatically from the brand book and
  thumbnail philosophy. Use when the user asks to create a newsletter thumbnail,
  build a diagram for an issue, or generate any One Stack visual asset.
compatibility: "Requires Python 3 + Pillow. Install: pip install Pillow"
---

# One Stack Newsletter Assets

Generates two types of assets for One Stack issues:
1. **Thumbnails** — 1200×630 PNG via Pillow, Signal Grid aesthetic
2. **Excalidraw diagrams** — `.excalidraw` JSON files via Python

Both are written directly into the issue folder and committed if requested.

---

## Context (always load first)

Before generating anything, read these files to absorb brand and style context:

```
/Users/reymerekar/Desktop/rm-agents/content/newsletter/branding/brand-book.md
/Users/reymerekar/Desktop/rm-agents/content/newsletter/branding/thumbnail-philosophy.md
```

Also read any existing assets in the issue folder to understand the current state:
```
/Users/reymerekar/Desktop/rm-agents/content/newsletter/issues/[issue-slug]/
```

Reference implementations to study before writing new code:
- Thumbnail: `content/newsletter/branding/build_thumbnail.py` (Map It issue)
- Excalidraw: `content/newsletter/issues/speed-of-control/build_excalidraw.py`

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| **Issue slug** | Yes | e.g. `speed-of-control`, `map-it-before-you-automate-it` |
| **Issue title** | Yes | Display title for the thumbnail |
| **Subtitle** | Yes | One-liner that goes below the accent line |
| **Concept / visual idea** | No | What should the abstract visualization represent? If not provided, derive from the title. |
| **Asset type** | No | `thumbnail`, `excalidraw`, or `both`. Default: `thumbnail`. |
| **Diagram specs** | If excalidraw | List of diagrams: name + type + content description |

---

## Workflow

### Step 1 — Plan the visualization

Before writing code, state the visual concept clearly:

**Thumbnail:**
- What is the LEFT-side abstract visualization? (network topology, spoke diagram, grid, flow, etc.)
- What colors and node arrangement match the issue concept?
- What is the title split? (usually 2 lines, ~52px Lora-BoldItalic cream)
- What is the subtitle? (~15px InstrumentSans-Regular blue)

**Excalidraw:**
- How many diagrams?
- What type is each? (node graph, decision tree, flow, comparison table)
- What brand colors map to which semantic meanings? (NAVY_MID boxes, BLUE strokes, GOLD for warnings/emphasis, CREAM for primary text)

State this plan. Ask for confirmation before proceeding if the concept is ambiguous.

---

### Step 2 — Thumbnail

Write a `build_thumbnail.py` in the issue folder. Follow these rules exactly:

**Canvas:** 1200×630px, `Image.new("RGBA", (W, H), NAVY)` then flatten to RGB for text.

**Brand palette:**
```python
NAVY     = (26, 39, 68)
NAVY_MID = (37, 58, 88)
CREAM    = (245, 240, 235)
BLUE     = (107, 163, 214)
GOLD     = (232, 201, 122)
```

**Fonts path:**
```python
FONTS = "/Users/reymerekar/.claude/plugins/marketplaces/anthropic-agent-skills/skills/canvas-design/canvas-fonts"
```

**Font usage:**
| Element | Font file | Size |
|---------|-----------|------|
| "One Stack" label | `Lora-Italic.ttf` | 18px BLUE |
| Title lines | `Lora-BoldItalic.ttf` | ~52px CREAM |
| Hub labels | `Lora-BoldItalic.ttf` | 16px NAVY |
| Subtitle | `InstrumentSans-Regular.ttf` | 15px BLUE |

**Layout split:** abstract visualization LEFT (roughly x=0–580), typography RIGHT (x=690+).

**Typography anchors (right side):**
```python
draw_flat.text((690, 38),  "One Stack",  fill=BLUE,  font=font_script)
draw_flat.line([(690, 62), (820, 62)],   fill=BLUE,  width=1)
# Title: two lines around y=210–280
draw_flat.line([(690, 348), (1130, 348)], fill=GOLD, width=1)   # or BLUE for neutral issues
draw_flat.text((690, 364), subtitle,     fill=BLUE,  font=font_sub)
```

**Text centering rule (critical):** Always use `textbbox` and subtract the offset:
```python
bbox = draw_flat.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw_flat.text((cx - bbox[0] - tw // 2, cy - bbox[1] - th // 2), text, fill=color, font=font)
```

**Signal Grid layers (always include):**
1. Dot grid substrate — 28px spacing, alpha fades from hub center outward
2. Main visualization — nodes, spokes, arcs, flow lines (concept-specific)
3. Micro-nodes — 6–8 small background nodes for depth
4. Hub or focal element — primary node with glow rings
5. Flatten RGBA → RGB, then draw text

**Output path:**
```python
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbnail-[issue-slug].png")
```

After writing the script, run it:
```bash
cd /Users/reymerekar/Desktop/rm-agents/content/newsletter/issues/[issue-slug] && python3 build_thumbnail.py
```

Then read the output PNG to verify it looks correct before finishing.

---

### Step 3 — Excalidraw diagrams

Write a `build_excalidraw.py` in the issue folder. Use the helper functions from the speed-of-control reference (`base_props`, `text_el`, `labeled_rect`, `arrow_el`, `line_el`, `wrap`). Copy them verbatim — they are stable and correct.

**Brand palette (Excalidraw uses hex strings):**
```python
NAVY_BG  = "#1A2744"
NAVY_MID = "#253a58"
CREAM    = "#F5F0EB"
BLUE     = "#6BA3D6"
GOLD     = "#E8C97A"
```

**Semantic color rules:**
- Question/decision boxes → NAVY_MID fill, BLUE stroke, CREAM text
- Warning/emphasis boxes → NAVY_MID fill, GOLD stroke, GOLD text
- Primary hub/you node → CREAM fill, NAVY_BG stroke, NAVY_BG text
- Arrows between steps → CREAM color
- Fix/action arrows → GOLD color
- Background rect → always `bg_rect("bg", -300, -300, 1500, [height])` in NAVY_BG

**Output:**
```python
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
# Write each diagram: json.dump(wrap(elements), f, indent=2)
```

Run after writing:
```bash
cd /Users/reymerekar/Desktop/rm-agents/content/newsletter/issues/[issue-slug] && python3 build_excalidraw.py
```

---

### Step 4 — Verify and commit

1. Read the generated PNG (thumbnail) to visually confirm it looks correct
2. Check Excalidraw files exist and are valid JSON
3. If user asks to commit: `git add` the issue folder files and commit with a short message

---

## Common Visual Patterns by Concept

| Issue concept | Suggested left-side visualization |
|---|---|
| Controller / hub-and-spoke | Spoke diagram with YOU hub, agent nodes at radius |
| Before/after | Left cluster (messy) → arrow → right cluster (clean) |
| Sequential flow | Vertical chain of nodes with arrows |
| Decision tree | Diamond root branching to boxes below |
| Comparison | Two symmetric clusters, different colors |
| Parallel processes | Horizontal lanes with nodes per lane |
| Single constraint / bottleneck | Wide graph funneling to a narrow node |

---

## Reference Files

- Brand book: `content/newsletter/branding/brand-book.md`
- Thumbnail philosophy: `content/newsletter/branding/thumbnail-philosophy.md`
- Prior thumbnail script: `content/newsletter/branding/build_thumbnail.py`
- Prior Excalidraw script: `content/newsletter/issues/speed-of-control/build_excalidraw.py`
- Prior thumbnail output: `content/newsletter/issues/map-it-before-you-automate-it/thumbnail-map-it.png`
- Speed of Control thumbnail: `content/newsletter/issues/speed-of-control/thumbnail-speed-of-control.png`
