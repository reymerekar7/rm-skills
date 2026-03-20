#!/usr/bin/env python3
"""
X/Twitter Scanner — uses xAI's Grok API with x_search tool to pull
recent posts from AI creators and news accounts.

The Grok API has native X/Twitter search built in, so we don't need
separate Twitter API credentials. One xAI API key does everything.

Usage:
    python scan_x.py                         # default scan, all accounts
    python scan_x.py --hours 6               # last 6 hours
    python scan_x.py --handles karpathy sama # specific accounts only
    python scan_x.py --query "Claude update" # freeform X search

Output: JSON to stdout with Grok's summarized findings + raw response.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Default accounts to monitor
DEFAULT_HANDLES = [
    # AI Labs / Products
    "AnthropicAI",
    "OpenAI",
    "GoogleAI",
    "cursor_ai",
    "peraborgen",    # Perplexity AI
    # AI Practitioners / Researchers
    "karpathy",
    "AndrewYNg",
    "sama",
    "vasuman",       # Vasu — ex-Meta, founder of Varick Agents AI agency
    "OfficialLoganK", # Logan Kilpatrick — Google AI, ex-OpenAI DevRel
    "mattshumer_",   # Matt Shumer — CEO HyperWrite, AI agent builder
    # Builders / Solopreneurs
    "AlexFinn",      # Vibe coding, Creator Buddy, X growth
    "ErnestoSOFTWARE", # Ernesto Lopez, 21yo, 11 apps, $73k MRR, mobile app strategies
    "gregisenberg",
    "levelsio",
    "itsolelehmann", # Ole Lehmann — AI agents for non-technical people
    "PrajwalTomar_", # Prajwal Tomar — MVPs in 21 days, vibe coding
    "JosephKChoi",   # Joseph Choi — consumer apps, viral growth
    "trq212",        # Content creator
    # AI News / Commentary
    "AIHighlight",
    "TheRundownAI",
    "aakashg0",      # Aakash Gupta — AI, growth, product analysis
    "WesRoth",       # Wes Roth — AI commentary, automation, optimism
    "Scobleizer",    # Robert Scoble — tech/AI news aggregator
]

# Flagging criteria — posts matching these get marked [FLAGGED]
FLAG_CRITERIA = """
Mark a post as [FLAGGED] if it hits ANY of these:
- Breaking product launch or major feature drop (Claude, GPT, Gemini, Cursor, etc.)
- Real revenue/growth numbers shared publicly (MRR, ARR, user counts, conversion rates)
- Genuinely contrarian take that challenges mainstream AI narratives
- A workflow, system, or tool that fits "1 person + AI > 10 people"
- High engagement signal: viral post, >500 likes, or replies blowing up
- Anything directly relevant to: lean ops, solopreneurship, AI implementation, vibe coding, mobile apps
"""

XAI_API_URL = "https://api.x.ai/v1/responses"
XAI_MODEL = "grok-4-1-fast-reasoning"


def load_api_key():
    """Load xAI API key from .env file in repo root."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        env_path = current / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("XAI_API_KEY="):
                        token = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if token:
                            return token
        current = current.parent

    # Fallback to environment variable
    token = os.environ.get("XAI_API_KEY")
    if token:
        return token

    print("ERROR: XAI_API_KEY not found in .env or environment.", file=sys.stderr)
    print("Add XAI_API_KEY=your_key to your .env file.", file=sys.stderr)
    sys.exit(1)


def call_grok_x_search(api_key, prompt, from_date=None, to_date=None):
    """Call the xAI Grok API with x_search tool enabled."""
    payload = {
        "model": XAI_MODEL,
        "input": [
            {"role": "user", "content": prompt}
        ],
        "tools": [
            {"type": "x_search"}
        ],
    }

    # Add date filters if provided
    if from_date or to_date:
        tool_config = {"type": "x_search"}
        if from_date:
            tool_config["from_date"] = from_date
        if to_date:
            tool_config["to_date"] = to_date
        payload["tools"] = [tool_config]

    data = json.dumps(payload).encode("utf-8")
    req = Request(XAI_API_URL, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "curl/7.81.0")

    try:
        with urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"API error {e.code}: {error_body}", file=sys.stderr)
        if e.code == 429:
            print("Rate limited. Try again later.", file=sys.stderr)
        return None
    except URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return None


def extract_text_from_response(response):
    """Extract the text content from the Grok API response."""
    if not response:
        return ""

    # The responses API returns output as a list of items
    output = response.get("output", [])
    texts = []
    for item in output:
        if item.get("type") == "message":
            content = item.get("content", [])
            for block in content:
                if block.get("type") == "output_text":
                    texts.append(block.get("text", ""))
        # Also handle direct text field
        if "text" in item:
            texts.append(item["text"])

    # Fallback: check top-level fields
    if not texts:
        if "output_text" in response:
            texts.append(response["output_text"])
        # Handle chat completions format as fallback
        choices = response.get("choices", [])
        for choice in choices:
            msg = choice.get("message", {})
            if "content" in msg:
                texts.append(msg["content"])

    return "\n".join(texts)


def scan_accounts(handles, api_key, hours):
    """Scan accounts by asking Grok to search X for their recent posts."""
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=hours)
    from_date = since.strftime("%Y-%m-%d")
    to_date = now.strftime("%Y-%m-%d")

    handles_str = ", ".join(f"@{h}" for h in handles)

    prompt = f"""Search X/Twitter for the most recent and noteworthy posts from these accounts in the last {hours} hours: {handles_str}

Return exactly 10 top posts (or as many as exist if fewer than 10). Rank by relevance to someone building AI-powered products, creating short-form video content about AI implementation, and running lean operations. Prioritize: AI product launches, real revenue/growth data, vibe coding workflows, content creation tactics, and contrarian takes on AI narratives. Engagement is a secondary signal.

For each post, provide:
1. The account handle
2. A 1-2 sentence summary of the post
3. Engagement metrics if visible (likes, retweets, replies)
4. The post URL

{FLAG_CRITERIA}

Format your response like this:

[FLAGGED] @handle — summary of post (likes: X, retweets: Y) — url
@handle — summary of post (likes: X) — url

Put all [FLAGGED] posts at the top of the output, then the rest below.

If the monitored accounts have fewer than 10 posts in this window, fill remaining slots with the highest-engagement AI-related posts from the broader X feed. Label these backfilled posts with [DISCOVERY] instead of the account handle prefix so I know they came from outside my list.

Skip: retweets of old content, generic motivational posts, pure promo with no substance."""

    response = call_grok_x_search(api_key, prompt, from_date=from_date, to_date=to_date)
    summary = extract_text_from_response(response)

    return {
        "scan_time": now.isoformat(),
        "hours_back": hours,
        "accounts_queried": handles,
        "from_date": from_date,
        "to_date": to_date,
        "summary": summary,
        "raw_response": response,
    }


def search_topic(query, api_key, hours):
    """Search X for a specific topic or query."""
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=hours)
    from_date = since.strftime("%Y-%m-%d")
    to_date = now.strftime("%Y-%m-%d")

    prompt = f"""Search X/Twitter for the most recent and noteworthy posts about: {query}

Look at the last {hours} hours. Provide:
1. The most discussed angles and opinions
2. Key posts with author handles and URLs
3. Any breaking news or announcements
4. Engagement levels (likes, retweets) where visible

Focus on substantive posts with real information, not generic takes."""

    response = call_grok_x_search(api_key, prompt, from_date=from_date, to_date=to_date)
    summary = extract_text_from_response(response)

    return {
        "scan_time": now.isoformat(),
        "query": query,
        "hours_back": hours,
        "from_date": from_date,
        "to_date": to_date,
        "summary": summary,
        "raw_response": response,
    }


def main():
    parser = argparse.ArgumentParser(description="Scan X/Twitter via xAI Grok API")
    parser.add_argument("--hours", type=int, default=12, help="Hours to look back (default: 12)")
    parser.add_argument("--handles", nargs="+", default=None, help="Specific handles to scan")
    parser.add_argument("--query", type=str, default=None, help="Freeform search query instead of account scan")
    parser.add_argument("--summary-only", action="store_true", help="Print only the summary text, not full JSON")
    args = parser.parse_args()

    api_key = load_api_key()
    handles = args.handles or DEFAULT_HANDLES

    if args.query:
        result = search_topic(args.query, api_key, args.hours)
    else:
        result = scan_accounts(handles, api_key, args.hours)

    if args.summary_only:
        print(result.get("summary", "No results."))
    else:
        # Print without raw_response for cleaner output (it's large)
        clean_result = {k: v for k, v in result.items() if k != "raw_response"}
        print(json.dumps(clean_result, indent=2))


if __name__ == "__main__":
    main()
