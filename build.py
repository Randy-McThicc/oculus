import json
import os
import time
from datetime import datetime

import feedparser
from jinja2 import Environment, FileSystemLoader

# Read the list of news sources from feeds.json
with open("feeds.json") as f:
    data = json.load(f)

feeds = data["feeds"]

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
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "published_parsed": entry.get("published_parsed"),
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

# Sort newest-first; stories with no date fall back to the very oldest possible
def story_date(story):
    return story["published_parsed"] or time.gmtime(0)

unique.sort(key=story_date, reverse=True)

# Keep only the latest 30
latest = unique[:30]
print(f"Keeping the latest {len(latest)} stories")

# Render the stories into the HTML template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html.j2")

html = template.render(
    stories=latest,
    count=len(latest),
    feed_count=len(feeds),
    updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
)

# Write the finished page to public/index.html
os.makedirs("public", exist_ok=True)
with open("public/index.html", "w") as f:
    f.write(html)

print("Wrote public/index.html")
