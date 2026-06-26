import xml.etree.ElementTree as ET
from urllib.parse import urlparse

# Blogger Atom namespace
NS = {
    "atom": "http://www.w3.org/2005/Atom"
}

print("Reading feed.atom...")

# Load the Atom feed
tree = ET.parse("feed.atom")
root = tree.getroot()

# Find all entries
entries = root.findall("atom:entry", NS)

print(f"Found {len(entries)} entries.\n")

posts = []

for entry in entries:

    title = entry.findtext("atom:title", default="", namespaces=NS)
    published = entry.findtext("atom:published", default="", namespaces=NS)
    updated = entry.findtext("atom:updated", default="", namespaces=NS)
    content = entry.findtext("atom:content", default="", namespaces=NS)

    labels = []
    for category in entry.findall("atom:category", NS):
        term = category.get("term")
        if term:
            labels.append(term)

    posts.append({
        "title": title,
        "published": published,
        "updated": updated,
        "labels": labels,
        "content": content
    })

print(f"Extracted {len(posts)} posts.\n")

print("=" * 60)

for post in posts[:5]:
    print(f"Title       : {post['title']}")
    print(f"Published   : {post['published']}")
    print(f"Updated     : {post['updated']}")
    print(f"Labels      : {', '.join(post['labels'])}")
    print(f"Content Len : {len(post['content'])} characters")
    print("-" * 60)