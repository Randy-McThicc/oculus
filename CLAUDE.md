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
- [x] **Day 4 — Publish.** git basics, GitHub repo, GitHub Pages → first public URL.
- [x] **Day 5 — Automation.** GitHub Actions hourly cron → site updates itself 24/7.
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
- Day 4 DONE: site is LIVE. Repo: https://github.com/Randy-McThicc/oculus (public). Live URL:
  https://randy-mcthicc.github.io/oculus/ . Did: git init, repo-local identity (name "Boss",
  email = GitHub private noreply), .gitignore, first commit, `gh repo create --push`, enabled
  Pages from main /docs. Output folder renamed public/ -> docs/ (Pages deploy-from-branch only
  serves root or /docs). Concepts taught: git vs GitHub vs Pages, add/commit/push, branches,
  remotes/origin, .gitignore, private commit email, deploy-from-branch constraint.
- IMPORTANT: site does NOT yet auto-update. It only refreshes when we run `build.py` and
  `git add/commit/push` the new docs/index.html. Making it refresh itself hourly = Day 5.
- Day 5 DONE: site now auto-updates 24/7. Added `.github/workflows/build.yml` — hourly cron
  (`0 * * * *`) + manual `workflow_dispatch` button. Steps: checkout → setup-python 3.11 →
  pip install -r requirements.txt → python build.py → commit+push docs/index.html only if it
  changed (`git diff --staged --quiet` guard). Needs `permissions: contents: write` so the bot
  can push (common gotcha). Verified via manual run: bot committed "Auto-update headlines" and
  pushed with no laptop involved. Concepts taught: GitHub Actions (cloud robot + workflow file),
  .github/workflows magic path, YAML (indent=nesting, no tabs), cron 5-field syntax, uses: vs
  run:, fresh ephemeral runner, permissions, schedule is best-effort + disabled after 60d idle.
- Also trimmed feeds.json: removed The Verge AI and Hacker News (HN-dominance goal). Now 4
  feeds: OpenAI, Google DeepMind, Ars Technica, MIT Tech Review.
- WORKFLOW CHANGE for Boss: the bot now commits to main on its own. ALWAYS `git pull` before
  making/pushing local edits, or you'll hit "rejected (non-fast-forward)" conflicts.
- Minor: GH warns actions/checkout@v4 + setup-python@v5 use Node 20 (deprecated June 2026).
  Harmless now; bump action versions when convenient.
- GitHub Trending feed: deferred. No official RSS (web page only). Options when revisited:
  community RSS bridge (mshibanami/GitHubTrendingRSS, drop-in) OR GitHub API (JSON, needs new
  non-RSS code path in build.py — good Day 6 lesson).
- Next (Day 6+, optional): AI summaries via Claude API, keyword filters, more sources, agents,
  monetization.
- Tooling: Python 3.9.6, git, Homebrew, and `gh` 2.92.0 all installed; gh authed as
  Randy-McThicc. Run brew/gh in non-login shells via: eval "$(/opt/homebrew/bin/brew shellenv)".
