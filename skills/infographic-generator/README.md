# Infographic Generator

Build polished infographic PNGs from any topic. Research a subject, design a multi-section HTML layout, and export to PNG via Playwright. Bring your own brand book and reference images, or use the built-in default design system.

## What It Does

- Researches a topic (via Tavily) or works from content you provide
- Builds a clean, structured HTML infographic (4-section portrait or square)
- Accepts **brand context** (pasted inline, dropped as a file, or described) to match your colors, fonts, and identity
- Accepts **reference images** to match a layout style you like
- Exports to a full-resolution PNG via Playwright screenshot

Works for any platform: LinkedIn, blog posts, newsletters, slide decks, or print.

## Prerequisites

- **Node.js** (for Playwright)
- No API key required

## Setup

Install Playwright once:

```bash
cd /tmp && npm install playwright
```

That's it. No `.env` file needed.

## Usage

### Basic — topic only

```
Create an infographic about the 4 habits of high-performing founders
```

Claude will research the topic and build a 4-section portrait infographic using the built-in design system.

### With brand context

Pass your brand information however is convenient — paste it inline, drop a file, or just describe it:

```
Create an infographic about AI agents. My brand colors are #1A2744 and #6BA3D6, font is Inter, logo initial is "R".
```

```
Create an infographic about AI agents. [paste or attach brand-book.md]
```

Claude extracts what it needs (colors, fonts, logo, tone) from whatever you provide and applies it to the infographic.

### With a reference image

```
Create an infographic about AI agents. Match the style of this image: [drop image]
```

Claude analyzes the reference image's layout structure, section arrangement, and visual hierarchy — then rebuilds it with your content.

### With both

```
Create an infographic about AI agents. My brand: [paste brand context]. Match this layout: [drop image]
```

Brand context controls colors + fonts. Reference image controls layout structure.

## Output

PNG saved to `./output/infographic-[topic].png` — 1080×1350px (portrait) or 1200×1200px (square).

Output files are gitignored by default.

## Passing Brand Context

Brand context can come from anywhere — there's no required format or file location. Claude reads what you provide and extracts what it needs. Examples of what to include:

```
Colors: primary #1A2744, accent #6BA3D6, background #EFF4F0
Fonts: Inter for headings and body
Logo: monogram "A", white on #6BA3D6 background
Tone: direct, specific, no jargon
```

You can paste this inline, drop a file, or write it in a few sentences. Anything not specified falls back to the built-in defaults.

## Customization

| Thing to change | How |
|---|---|
| Footer name/initial | Tell Claude "use [name] in the footer" |
| Output directory | Tell Claude "save output to ./assets/" |
| Canvas size | Ask for "square" (1200×1200) instead of portrait (default 1080×1350) |
| Number of sections | Ask for 3 sections if content is sparse |
