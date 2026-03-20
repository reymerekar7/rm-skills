# rm-skills

AI agent skills for Claude Code — video analysis, X/Twitter scanning, Gmail triage, and tweet reading.

## Skills

| Skill | Description | API Key Required |
|-------|-------------|-----------------|
| [video-performance-analyzer](skills/video-performance-analyzer/) | Analyze short-form videos for transcript, performance scoring, and repurposing ideas | `GEMINI_API_KEY` |
| [x-scanner](skills/x-scanner/) | Scan X/Twitter for AI news from 25+ curated accounts via xAI Grok API | `XAI_API_KEY` |
| [gmail-triage](skills/gmail-triage/) | Triage Gmail inbox — flag important, summarize newsletters, clean up noise | Google Workspace CLI |
| [twitter-reader](skills/twitter-reader/) | Fetch tweet content by URL using Jina.ai reader API | `JINA_API_KEY` |

## Install

```bash
# List available skills
npx skills add reymerekar/rm-skills --list

# Install a specific skill
npx skills add reymerekar/rm-skills --skill video-performance-analyzer

# Install all skills
npx skills add reymerekar/rm-skills --all
```

## Setup

Each skill needs its own API key or tool. Add keys to a `.env` file at your project root:

```bash
# Video Performance Analyzer
GEMINI_API_KEY=your_gemini_key

# X Scanner
XAI_API_KEY=your_xai_key

# Twitter Reader
JINA_API_KEY=your_jina_key

# Gmail Triage — uses Google Workspace CLI instead of API key
# npm install -g @googleworkspace/cli && gws auth setup
```

## Per-Skill Details

### Video Performance Analyzer

Uses Google Gemini to extract transcripts and analyze short-form videos across 6 dimensions: hook strength, progressive intrigue, credibility signals, viewer-first framing, visual pattern interrupts, and CTA quality. Generates 4-8 repurposing ideas per video.

```bash
python scripts/analyze_video.py /path/to/video.mp4
python scripts/analyze_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Requires:** `pip install google-genai`

### X Scanner

Monitors AI-focused X/Twitter accounts using xAI's Grok API with native `x_search`. Flags breaking news, revenue data, contrarian takes, and viral content. Includes a cron-ready script for automated daily digests.

```bash
python scripts/scan_x.py --summary-only
python scripts/scan_x.py --hours 6
python scripts/scan_x.py --query "Claude Code update"
```

**Requires:** No Python packages (stdlib only)

### Gmail Triage

Read-only inbox triage using Google Workspace CLI. Categorizes emails into Action Required, Newsletter, and Low Priority. Summarizes newsletters by topic and marks noise as read.

**Requires:** `npm install -g @googleworkspace/cli`

### Twitter Reader

Fetches tweet content from any public X/Twitter URL using Jina.ai's reader API. Returns clean Markdown with author info, timestamps, and media descriptions.

```bash
python scripts/fetch_tweet.py https://x.com/user/status/123456
scripts/fetch_tweets.sh url1 url2 url3
```

**Requires:** No Python packages (uses curl)

## License

MIT
