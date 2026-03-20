# Video Performance Analyzer

Analyze short-form videos (TikTok, Instagram Reels, YouTube Shorts) to extract transcripts, understand why they perform, and generate repurposing ideas.

## What It Does

- Extracts a full timestamped transcript from any video
- Scores the video across 6 performance dimensions (hook, progressive intrigue, credibility, framing, retention, CTA)
- Generates 4-8 actionable repurposing ideas per video

## Prerequisites

- **GEMINI_API_KEY** — Get one from [Google AI Studio](https://aistudio.google.com/apikey)
- Python 3.9+
- `pip install google-genai --break-system-packages`

## Usage

```bash
# Analyze a local video file
python scripts/analyze_video.py /path/to/video.mp4

# Analyze a YouTube video
python scripts/analyze_video.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Save output to file
python scripts/analyze_video.py /path/to/video.mp4 --output analysis.md
```

## API Key Setup

Add to `.env` at your project root:
```
GEMINI_API_KEY=your_key_here
```

Or set as an environment variable:
```bash
export GEMINI_API_KEY=your_key_here
```
