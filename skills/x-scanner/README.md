# X/Twitter Scanner

Scan X/Twitter for recent posts from a curated list of AI creators and news accounts using xAI's Grok API.

## What It Does

- Monitors 25+ AI-focused X/Twitter accounts for noteworthy posts
- Flags breaking news, revenue data, contrarian takes, and viral content
- Supports freeform topic search across all of X
- Outputs structured digests with engagement metrics and post URLs
- Includes a cron-ready script for automated daily scans

## Prerequisites

- **XAI_API_KEY** — Get one from [x.ai/api](https://x.ai/api)
- Python 3.9+ (no external packages needed — uses stdlib only)

## Usage

```bash
# Default scan — all accounts, last 12 hours
python scripts/scan_x.py

# Last 6 hours, summary only
python scripts/scan_x.py --hours 6 --summary-only

# Specific accounts
python scripts/scan_x.py --handles karpathy sama AnthropicAI

# Freeform topic search
python scripts/scan_x.py --query "Claude Code update"
```

## Automated Scanning

Use `scripts/scheduled_scan.sh` with cron for automated daily digests:

```bash
# Add to crontab — scan every 12 hours
0 8,20 * * * /path/to/skills/x-scanner/scripts/scheduled_scan.sh
```

## API Key Setup

Add to `.env` at your project root:
```
XAI_API_KEY=your_key_here
```
