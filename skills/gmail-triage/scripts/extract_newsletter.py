#!/usr/bin/env python3
"""Extract readable text from a gws gmail message JSON response.

Usage:
    # Pipe from gws directly:
    gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"full"}' | python extract_newsletter.py

    # Or from a saved file:
    python extract_newsletter.py < message.json

    # With a character limit (default 3000):
    python extract_newsletter.py --limit 5000 < message.json
"""

import sys
import json
import base64
import re
import html
import argparse


def find_part(payload, mime="text/plain"):
    """Recursively find a MIME part in the email payload."""
    if payload.get("mimeType") == mime and payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode(
            "utf-8", errors="replace"
        )
    for part in payload.get("parts", []):
        result = find_part(part, mime)
        if result:
            return result
    return None


def extract_text(data, limit=3000):
    """Extract readable text from a Gmail message JSON object."""
    # Try text/plain first
    text = find_part(data["payload"], "text/plain")
    if not text:
        # Fall back to HTML, strip tags
        h = find_part(data["payload"], "text/html")
        if h:
            text = re.sub(r"<[^>]+>", " ", h)
            text = html.unescape(text)
            text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] if text else "No content found"


def main():
    parser = argparse.ArgumentParser(description="Extract text from Gmail message JSON")
    parser.add_argument("--limit", type=int, default=3000, help="Max characters to output")
    args = parser.parse_args()

    raw = sys.stdin.read()
    # Strip any non-JSON prefix (e.g., "Using keyring backend: keyring")
    idx = raw.index("{")
    data = json.loads(raw[idx:])

    print(extract_text(data, args.limit))


if __name__ == "__main__":
    main()
