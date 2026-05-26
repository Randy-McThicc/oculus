import calendar
import html
import json
import os
import re
import time
from datetime import datetime

import feedparser
from jinja2 import Environment, FileSystemLoader

# Read the list of news sources from feeds.json
with open("feeds.json") as f:
    data = json.load(f)

feeds = data["feeds"]

# Keywords used to keep general feeds on-topic. We match WHOLE words only (via \b word
# boundaries) so short terms like "ai" don't falsely match inside words like "claims" or "fail".
keywords = [k.lower() for k in data.get("keywords", [])]
keyword_pattern = (
    re.compile(r"\b(" + "|".join(re.escape(k) for k in keywords) + r")\b")
    if keywords else None
)

print(f"Loaded {len(feeds)} feeds:")
for feed in feeds:
    print(f"  - {feed['name']}: {feed['url']}")

# Fetch every feed, collect all stories into one list, skip any that fail
all_stories = []

for feed in feeds:
    print(f"Fetching: {feed['name']} ...")
    try:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries:
            all_stories.append({
                "source": feed["name"],
                "title": html.unescape(entry.title),  # decode &#8216; etc. into real characters
                "summary": entry.get("summary", ""),
                "link": entry.link,
                "published": entry.get("published", ""),
                "published_parsed": entry.get("published_parsed"),
                "always_keep": feed.get("always_keep", False),
            })
        print(f"  got {len(parsed.entries)} stories")
    except Exception as e:
        print(f"  SKIPPED {feed['name']} (error: {e})")

print(f"\nTotal stories collected: {len(all_stories)}")

# Remove duplicate stories (same link appearing in more than one feed)
unique = []
seen_links = set()
for story in all_stories:
    if story["link"] not in seen_links:
        seen_links.add(story["link"])
        unique.append(story)

print(f"After removing duplicates: {len(unique)}")

# Keep stories on-topic: trusted feeds (always_keep) pass through; everything else must
# mention at least one keyword in its title or summary.
def is_relevant(story):
    if story["always_keep"] or keyword_pattern is None:
        return True
    text = (story["title"] + " " + story["summary"]).lower()
    return bool(keyword_pattern.search(text))

relevant = [s for s in unique if is_relevant(s)]
print(f"After keyword filter: {len(relevant)}")

# Sort newest-first; stories with no date fall back to the very oldest possible
def story_date(story):
    return story["published_parsed"] or time.gmtime(0)

relevant.sort(key=story_date, reverse=True)

# Keep only the latest 30
latest = relevant[:30]
print(f"Keeping the latest {len(latest)} stories")

# Turn each story's publish time into a friendly "3h ago" label
def relative_age(story):
    pp = story["published_parsed"]
    if not pp:
        return ""
    seconds = time.time() - calendar.timegm(pp)  # timegm reads the UTC struct_time
    if seconds < 60:
        return "just now"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)}m ago"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)}h ago"
    return f"{int(hours / 24)}d ago"

for story in latest:
    story["age"] = relative_age(story)

# Render the stories into the HTML template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html.j2")

html = template.render(
    stories=latest,
    count=len(latest),
    feed_count=len(feeds),
    updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
)

# Write the finished page to docs/index.html (GitHub Pages serves from /docs)
os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w") as f:
    f.write(html)

print("Wrote docs/index.html")
