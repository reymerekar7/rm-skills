---
name: linkedin-asset-analyzer
description: >
  Analyze LinkedIn carousels and infographics to understand why they performed.
  Focuses on visual design, format choices, and engagement mechanics — not copy.
  Use when a reference image or PDF is provided and you want to know what made it work.
  Supports image files (PNG, JPG, screenshots) and PDFs.
compatibility: "Works with image inputs (Read tool) and PDF inputs (pdf skill). No external MCPs required."
---

# LinkedIn Asset Analyzer

## Overview

One job: look at a LinkedIn carousel or infographic and explain why it performed. Visual and structural analysis only — not copy critique.

---

## When to Use

Trigger on:
- "analyze this carousel / infographic"
- "why did this perform"
- "break down this image"
- User drops an image or PDF of a LinkedIn asset without explanation

---

## Input Formats

**Images (PNG, JPG, screenshots):** Use the `Read` tool directly on the file path. If multiple slides are separate images, read all in parallel.

**PDFs:** Use the `pdf` skill to extract slides, then analyze.

---

## Analysis Framework

Run every asset through these 4 lenses.

---

### 1. FORMAT & LAYOUT

- **Asset type**: Single infographic / Multi-slide carousel / Table / Grid
- **Slide count** (carousel): Cover + body + CTA breakdown
- **Layout pattern**: Single column / Two-column / Grid / Timeline / Comparison table
- **Information density**: Dense / Balanced / Airy — how much per slide/section?
- **Scannability**: Can someone get the value in 5 seconds without reading every word?

---

### 2. VISUAL DESIGN

- **Cover strength**: What makes the cover slide stop-scroll? Bold text, color contrast, visual element, novelty?
- **Color palette**: Background + accent + highlight. Consistent? High contrast?
- **Typography hierarchy**: Is it immediately clear what to read first, second, third?
- **Icons / imagery**: None / Emoji / Custom icons / Illustrations. Do they add meaning or just decoration?
- **Whitespace**: Does the layout breathe or feel cluttered?
- **Brand consistency**: Does it look like a system or a one-off?

---

### 3. ENGAGEMENT MECHANICS

- **Save trigger**: Is there something worth bookmarking? Checklist / Cheat sheet / Reference table / Prompt list
- **Share trigger**: Would someone tag a colleague or repost this to their feed?
- **Comment trigger**: Does it invite a reaction, opinion, or follow-up question?
- **CTA placement**: Where is the follow/repost ask? Does it feel earned or bolted on?
- **Algorithm fit**: Carousel > infographic > single image. Does the format match the intent?

---

### 4. WHY IT WORKED

Synthesize the above into 3-5 bullet points explaining the performance. Be specific — not "good design" but *what specifically* about the design drove the result.

Format:
```
- [Specific element] → [Why it drove engagement/saves/shares]
```

---

## Output Format

```
## LinkedIn Asset Analysis

**Asset:** [filename or description]
**Creator:** [if visible]
**Format:** [infographic / carousel / single image]

---

### Format & Layout
[findings]

### Visual Design
[findings]

### Engagement Mechanics
[findings]

### Why It Worked
- [element] → [reason]
- ...
```
