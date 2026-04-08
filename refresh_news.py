#!/usr/bin/env python3
"""
Refresh news data for the Social Media Ban Tracker.
Calls Claude API with web search to get the latest headline per country.
Outputs news-data.json for the HTML map to consume.

Usage:
    ANTHROPIC_API_KEY=sk-... python refresh_news.py

Or triggered via GitHub Actions (see .github/workflows/refresh.yml)
"""

import os
import json
import sys
from anthropic import Anthropic

# Countries to track — only those with stage > 0 (active regulatory activity)
COUNTRIES = {
    "US": "United States social media minors ban KOSA COPPA regulation",
    "BR": "Brazil social media minors Digital Statute children",
    "NO": "Norway social media ban minors under 15",
    "FI": "Finland social media minors age restriction",
    "DK": "Denmark social media ban children under 15",
    "UK": "United Kingdom Online Safety Act social media minors ban",
    "DE": "Germany social media ban minors under 14",
    "CZ": "Czechia social media minors restriction",
    "FR": "France social media ban minors under 15",
    "AT": "Austria social media ban minors under 14",
    "SI": "Slovenia social media ban minors",
    "IT": "Italy social media minors parental consent influencer",
    "ES": "Spain social media ban minors under 16 executive liability",
    "PT": "Portugal social media ban minors Digital Mobile Key",
    "GR": "Greece social media ban minors Kids Wallet",
    "CN": "China social media minors time limit youth mode",
    "PK": "Pakistan social media ban minors",
    "MY": "Malaysia social media ban under 16 Online Safety Act",
    "ID": "Indonesia social media ban minors under 16",
    "AU": "Australia social media ban under 16 eSafety enforcement",
    "NZ": "New Zealand social media ban minors",
}


def refresh_news():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    # Build the prompt — ask Claude to search for each country and return structured JSON
    country_list = "\n".join(
        f"- {code}: {query}" for code, query in COUNTRIES.items()
    )

    prompt = f"""I need you to search the web for the latest news on social media bans/restrictions for minors in each of these countries. For each country, find the single most recent and relevant development.

Countries to search:
{country_list}

For each country, return:
1. A one-sentence headline summary of the latest development (written for a marketing/advertising industry audience — focus on what matters for media buyers and brand marketers)
2. The source name
3. The approximate date

CRITICAL: You must search the web for current information. Do not rely on training data.

Return ONLY valid JSON in this exact format, with no other text before or after:
{{
  "updated": "YYYY-MM-DD",
  "countries": {{
    "US": {{
      "headline": "One sentence headline relevant to marketers",
      "source": "Source Name",
      "date": "Month YYYY"
    }},
    ... (all countries)
  }}
}}

If you cannot find recent news for a country, use:
{{"headline": "No recent developments", "source": "", "date": ""}}
"""

    print("Calling Claude API with web search enabled...")
    print(f"Searching for {len(COUNTRIES)} countries...")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        tools=[{"type": "web_search_20260209", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract text from response (may contain multiple content blocks)
    text_parts = []
    for block in message.content:
        if hasattr(block, "text"):
            text_parts.append(block.text)

    full_text = "\n".join(text_parts)

    # Parse JSON from response — strip any markdown fencing
    clean = full_text.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1]  # remove first line
    if clean.endswith("```"):
        clean = clean.rsplit("```", 1)[0]
    clean = clean.strip()
    if clean.startswith("json"):
        clean = clean[4:].strip()

    try:
        data = json.loads(clean)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON from Claude response: {e}")
        print(f"Raw response:\n{full_text[:2000]}")
        sys.exit(1)

    # Write output
    output_path = os.path.join(os.path.dirname(__file__), "news-data.json")
    # If running in GitHub Actions, write to repo root
    if os.environ.get("GITHUB_WORKSPACE"):
        output_path = os.path.join(os.environ["GITHUB_WORKSPACE"], "news-data.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Wrote news-data.json with {len(data.get('countries', {}))} countries")
    print(f"  Updated: {data.get('updated', 'unknown')}")

    # Print summary
    for code, info in data.get("countries", {}).items():
        headline = info.get("headline", "—")
        print(f"  {code}: {headline[:80]}{'...' if len(headline) > 80 else ''}")


if __name__ == "__main__":
    refresh_news()
