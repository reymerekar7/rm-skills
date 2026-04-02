# LinkedIn Asset Analyzer

Analyze LinkedIn carousels and infographics to understand why they performed. Focuses on visual design, format choices, and engagement mechanics — not copy critique.

## What It Does

- Examines any LinkedIn visual asset (carousel, infographic, single image)
- Runs a structured 4-lens analysis: Format & Layout, Visual Design, Engagement Mechanics, and Why It Worked
- Outputs specific, actionable insights — not generic "good design" feedback
- Works with image files (PNG, JPG, screenshots) and PDFs

## Prerequisites

- None — no API keys, no external dependencies
- Works with Claude's built-in image reading capabilities
- For PDF carousels, uses the `pdf` skill to extract slides

## Setup

Install the skill into your Claude Code project:

```bash
# From your project root
mkdir -p .claude/skills
cp -r linkedin-asset-analyzer .claude/skills/
```

No `.env` file or configuration needed.

## Usage

### Analyze an image

```
Analyze this carousel [drop image]
```

### Analyze a PDF carousel

```
Break down this carousel [drop PDF]
```

### Ask why something performed

```
Why did this infographic perform? [drop image]
```

Claude reads the asset, runs all 4 analysis lenses, and returns a structured breakdown with specific observations about what drove engagement.

## Analysis Framework

| Lens | What It Covers |
|------|---------------|
| **Format & Layout** | Asset type, slide count, layout pattern, information density, scannability |
| **Visual Design** | Cover strength, color palette, typography hierarchy, icons/imagery, whitespace, brand consistency |
| **Engagement Mechanics** | Save/share/comment triggers, CTA placement, algorithm fit |
| **Why It Worked** | 3-5 specific bullet points mapping elements to engagement drivers |

## Output

Returns a structured markdown analysis. No files are created — output is inline in the conversation.
