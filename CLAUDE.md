# AI Radar

A public, auto-updating website that shows the latest AI/tech news headlines.
This project doubles as a hands-on course for learning how Claude Code works.

## What it does (target design)
1. `build.py` reads `feeds.json` (a list of RSS news sources)
2. fetches + dedupes + sorts the latest stories
3. renders a static page to `docs/index.html` (GitHub Pages serves from /docs)
4. (later) published via GitHub Pages, refreshed hourly by a GitHub Actions cron

Key idea: **Claude Code is the builder, not the runner.** A scheduler runs the program 24/7 —
not a laptop.

## How to run (local)
```bash
pip3 install -r requirements.txt   # one time
python3 build.py                   # regenerates docs/index.html
open docs/index.html               # view in browser (macOS)
```

## Layout
- `feeds.json` — the news sources (safe for a human to edit; no coding needed)
- `build.py` — the fetch + render engine
- `templates/index.html.j2` — page template (added Day 3)
- `docs/` — generated output served to visitors (GitHub Pages source folder)
- `requirements.txt` — Python dependencies

## Conventions
- Beginner-friendly: explain changes; keep them small and surgical.
- Python 3.9 (installed). Dependencies: feedparser, jinja2.

## Roadmap & progress
Two goals at once: (1) learn how Claude Code works (~70%), (2) ship the real website at the end.
This checklist is the single source of truth — update it as we go.

- [x] **Day 1 — Scaffolding.** CLAUDE.md, feeds.json, requirements.txt; deps installed.
- [x] **Day 2 — `build.py` (fetch).** Read feeds, fetch RSS, dedupe, sort, print stories.
- [x] **Day 3 — Page.** `templates/index.html.j2` + `public/style.css`; render real HTML; view in browser.
- [ ] **Day 4 — Publish.** git basics, GitHub repo, GitHub Pages → first public URL.
- [ ] **Day 5 — Automation.** GitHub Actions hourly cron → site updates itself 24/7.
- [ ] **Day 6+ (optional).** AI summaries (Claude API), keyword filters, agents, monetization.

(Full detailed plan also saved at: ~/.claude/plans/hello-i-structured-beaver.md)

## Status
- Day 1 DONE: scaffolding created (this file, feeds.json, requirements.txt); deps installed
  (feedparser, jinja2) via `pip3 install --user`. Also did deep concept teaching (CC mental
  model, memory vs CLAUDE.md, JSON, dependencies/pip, context window).
- Boss has a rough (not complete) grasp of the Day 1 concepts — offer a 2-line recap before
  diving into a new day, and keep teaching beginner-level.
- Day 2 DONE: built `build.py` step-by-step (read feeds → fetch all → try/except skip failures
  → dedupe by link via a set → sort newest-first by published_parsed → trim to latest 30 →
  print with enumerate). Concepts taught: import, with open, for, f-strings, [0] indexing,
  try/except, set, sort key function, slicing, enumerate, RSS-vs-webpage, HTTP status codes
  (200/307/404). Removed the dead Anthropic feed (404; /news is JS HTML with no RSS). 6 working
  feeds now; ~1128 stories/run.
- Known follow-ups (NOT bugs): output is HN-heavy and not all AI-topical → keyword filter is a
  Day 6 item; some titles show HTML entities like &#8216; → clean during HTML render (Day 3).
- Boss wants to ADD SOURCES later: Reddit (has RSS — subreddit `.rss`) and X/Twitter (NO public
  RSS — needs API or a bridge; teach this tradeoff when we get there). Also reduce HN dominance.
- Day 3 DONE: `build.py` now renders the latest 30 stories into `templates/index.html.j2` via
  jinja2 and writes `public/index.html` (auto-creates `public/`). Added `public/style.css` in
  the "Matrix Terminal" theme (pure black bg, phosphor-green #33ff66 monospace, glow on title +
  link hover, CSS counter renders [01]/[02] numbering, <source> tags). Verified live in browser.
  Concepts taught: HTML structure/tags, CSS (selectors/properties, classes, ::before counters),
  Jinja2 templates ({{ }} insert vs {% %} action), separating structure/style/data, writing
  files in "w" mode, datetime timestamp.
- Style status: Boss is happy with font for now; LAYOUT tweaks deferred to later (not urgent).
- Next (Day 4): publish online — git basics, create GitHub repo, enable GitHub Pages → first
  public URL. NOTE: `gh` CLI not installed yet (may need to install or use the web UI).
- Tooling: Python 3.9.6 + git present; `gh` not installed yet.
