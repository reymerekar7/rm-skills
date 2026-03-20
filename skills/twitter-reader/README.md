# Twitter Reader

Fetch Twitter/X post content by URL using Jina.ai's reader API. No Twitter API credentials or JavaScript needed.

## What It Does

- Fetches full tweet content (text, images, thread replies) from any public X/Twitter URL
- Returns clean Markdown with author, timestamp, and media descriptions
- Supports single and batch fetching

## Prerequisites

- **JINA_API_KEY** — Get one from [jina.ai](https://jina.ai/) (free tier available)
- curl (pre-installed on macOS/Linux)
- Python 3.9+ (for the Python script; bash script works without Python)

## Usage

```bash
# Single tweet (Python)
python scripts/fetch_tweet.py https://x.com/user/status/123456

# Single tweet (curl)
curl "https://r.jina.ai/https://x.com/user/status/123456" \
  -H "Authorization: Bearer $JINA_API_KEY"

# Batch fetch (bash)
scripts/fetch_tweets.sh \
  "https://x.com/user/status/123" \
  "https://x.com/user/status/456"

# Save to file
python scripts/fetch_tweet.py https://x.com/user/status/123456 output.md
```

## API Key Setup

Set as an environment variable:
```bash
export JINA_API_KEY=your_key_here
```

Or add to `.env` at your project root (auto-loaded by the bash script):
```
JINA_API_KEY=your_key_here
```
