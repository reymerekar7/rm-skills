---
name: x-scanner
description: >
  Scan X/Twitter for recent posts from a curated list of AI creators and news accounts
  using xAI's Grok API with the x_search tool. Use this skill whenever the user asks to:
  check what's happening on AI Twitter, scan X for news, pull recent tweets from creators,
  get an AI news digest, find trending AI topics, or generate content ideas from X. Also
  trigger when the scheduled ai-news-scan task runs. This skill requires an xAI API key.
---

# X/Twitter Scanner

## What This Does

Uses xAI's Grok API with the built-in `x_search` tool to scan X/Twitter for recent posts
from AI-focused accounts. Grok has native access to X data, so one API call handles search,
filtering, and summarization. No separate Twitter API credentials needed.

## Setup

The script reads the xAI API key from the `.env` file in your project root.

Expected `.env` entry:
```
XAI_API_KEY=your_xai_api_key_here
```

Get an API key from https://x.ai/api.

## How It Works

The script calls `https://api.x.ai/v1/responses` with the `x_search` tool enabled.
Grok searches X in real-time and returns a summarized digest of what the specified
accounts have been posting. This is much simpler than the Twitter API v2 approach —
no user ID lookups, no pagination, no OAuth.

## Accounts to Monitor

These are the default accounts baked into the script. Edit the `DEFAULT_HANDLES` list
in `scan_x.py` to change them.

**AI Labs / Products:**
- @AnthropicAI — Claude updates, product launches
- @OpenAI — GPT updates, industry moves
- @GoogleAI — Gemini, DeepMind, research
- @cursor_ai — Cursor editor updates, agentic coding
- @peraborgen — Perplexity AI

**AI Practitioners / Researchers:**
- @karpathy — deep LLM insights, tutorials
- @AndrewYNg — practical AI, education
- @sama — OpenAI CEO, industry direction
- @vasuman — Vasu, ex-Meta, founder of Varick Agents AI agency
- @OfficialLoganK — Logan Kilpatrick, Google AI, ex-OpenAI DevRel
- @mattshumer_ — Matt Shumer, CEO HyperWrite, AI agent builder

**Builders / Solopreneurs:**
- @AlexFinn — vibe coding, Creator Buddy, X growth strategies
- @ErnestoSOFTWARE — Ernesto Lopez, 21yo, 11 apps, $73k MRR, mobile app tactics
- @gregisenberg — startup ideas, community-led growth
- @levelsio — building in public, one-person companies
- @itsolelehmann — Ole Lehmann, AI agents for non-technical people
- @PrajwalTomar_ — Prajwal Tomar, MVPs in 21 days, vibe coding
- @JosephKChoi — Joseph Choi, consumer apps, viral growth
- @trq212 — content creator

**AI News / Commentary:**
- @AIHighlight — daily AI tools and prompts
- @TheRundownAI — daily AI news digest
- @aakashg0 — Aakash Gupta, AI/growth/product analysis
- @WesRoth — Wes Roth, AI commentary, automation, optimism
- @Scobleizer — Robert Scoble, tech/AI news aggregator

## Flagging System

Posts are marked `[FLAGGED]` and surfaced at the top of the output when they hit:
- Breaking product launch or major feature drop
- Real revenue/growth numbers shared publicly
- Genuinely contrarian take on AI narratives
- Workflow or system that fits "1 person + AI > 10 people"
- High engagement: viral post, >500 likes, or replies blowing up
- Directly relevant to: lean ops, solopreneurship, AI implementation, vibe coding, mobile apps

## How to Use

### Quick scan (default — last 12 hours)
```bash
python <skill-directory>/scripts/scan_x.py
```

### Custom time window
```bash
python <skill-directory>/scripts/scan_x.py --hours 6
```

### Specific accounts only
```bash
python <skill-directory>/scripts/scan_x.py --handles karpathy sama AnthropicAI
```

### Freeform X search
```bash
python <skill-directory>/scripts/scan_x.py --query "Claude Code update"
```

### Summary only (no JSON wrapper)
```bash
python <skill-directory>/scripts/scan_x.py --summary-only
```

Output is JSON to stdout with a `summary` field containing Grok's digest.

### Filtering What Matters

Not every tweet is content-worthy. Prioritize:
- Product launches and feature announcements
- Data, stats, or research worth breaking down
- Hot takes you can respond to or riff on
- Trends connecting to "1 person + AI > 10 people"
- Anything contrarian or surprising

Skip: retweets of old news, generic motivational AI tweets, pure promotional content.

## Default Workflow

1. Run `scan_x.py` to pull recent posts via xAI Grok API
2. If the script fails (key expired, rate limited), fall back to Tavily search with queries like "AI news today", "Claude update", "OpenAI announcement"
3. Summarize top 5-8 stories (1-2 sentences each, with source link)
4. Present digest to the user
5. **STOP here.** Do NOT generate content ideas or push to Notion unless the user explicitly asks.

## Content Ideas + Notion Push (only when explicitly asked)

When the user asks to generate content ideas or push to Notion:
- Map interesting tweets to content pillars:
  - AI Implementation Reality (35%)
  - Behind the Scenes (25%)
  - Industry Hot Takes (25%)
  - Democratizing Expertise (15%)
- For each idea, create a Notion page in the content calendar:
  - data_source_id: `<your-notion-database-id>`
  - Status: "Backlog"
  - Content Format: based on best platform fit
  - Funnel Stage: "TOFU"
  - Include source tweet links in the Notes section
