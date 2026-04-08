# Social Media Ban Tracker

An interactive hex-grid map tracking global social media restrictions for minors — built for marketers and media buyers.

**[Live site →](https://zwzw27.github.io/social-media-ban-tracker/)**

## What it shows

- **37 countries** across Americas, Europe, and Asia-Pacific
- **5-stage classification** from political intent to full enforcement with audits
- **Population-scaled hexes** with geographic positioning
- **Marketer-focused tooltips** with regulatory summaries and actionable implications
- **Auto-refreshing news** via Claude API with web search

## How to refresh news

1. Go to the **Actions** tab in this repo
2. Click **"Refresh News Data"** in the left sidebar
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait ~60 seconds — the action calls Claude API with web search, generates `news-data.json`, and commits it
5. The live site automatically picks up the new data on next page load

## Setup (one-time)

1. Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com)
2. In this repo, go to **Settings** → **Secrets and variables** → **Actions**
3. Add a new secret: `ANTHROPIC_API_KEY` = your key
4. Enable web search in your Anthropic Console organization settings

## Files

- `index.html` — The interactive map (rename from `social-media-bans-hex-map.html`)
- `refresh_news.py` — Python script that calls Claude API with web search
- `.github/workflows/refresh.yml` — GitHub Action (manual trigger)
- `news-data.json` — Auto-generated news data (created on first refresh)

## Tech

- D3-style SVG hex rendering (vanilla JS, no dependencies)
- Claude API with `web_search_20260209` tool for news
- GitHub Actions for CI
- GitHub Pages for hosting

## Data sources

Regulatory data compiled from government sources (eSafety Commissioner, Ofcom, EU DSA), Reuters, AP News, BBC, TechCrunch, and specialist trackers. News refreshed via Claude web search.

---

*The Current · April 2026*
