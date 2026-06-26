import os
import json
import re
import xml.etree.ElementTree as ET

ATOM = {
    "atom": "http://www.w3.org/2005/Atom"
}


def make_slug(title):
    """Convert title into an SEO-friendly slug."""
    slug = title.lower()
    slug = re.sub(r'&', ' and ', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip("-")


print("=" * 60)
print("KM STATIC SITE BUILDER")
print("=" * 60)

tree = ET.parse("feed.atom")
root = tree.getroot()

posts = []

for entry in root.findall("atom:entry", ATOM):

    title = entry.findtext("atom:title", default="", namespaces=ATOM)

    published = entry.findtext(
        "atom:published",
        default="",
        namespaces=ATOM
    )

    updated = entry.findtext(
        "atom:updated",
        default="",
        namespaces=ATOM
    )

    content = entry.findtext(
        "atom:content",
        default="",
        namespaces=ATOM
    )

    summary = entry.findtext(
        "atom:summary",
        default="",
        namespaces=ATOM
    )

    author = ""

    author_node = entry.find("atom:author", ATOM)

    if author_node is not None:
        author = author_node.findtext(
            "atom:name",
            default="",
            namespaces=ATOM
        )

    labels = []

    for cat in entry.findall("atom:category", ATOM):

        term = cat.attrib.get("term")

        if term:
            labels.append(term)

    blogger_url = ""

    for link in entry.findall("atom:link", ATOM):

        if link.attrib.get("rel") == "alternate":
            blogger_url = link.attrib.get("href", "")
            break

    image = ""

    m = re.search(
        r'<img[^>]+src="([^"]+)"',
        content,
        re.IGNORECASE
    )

    if m:
        image = m.group(1)

    posts.append({
        "title": title,
        "slug": make_slug(title),
        "published": published,
        "updated": updated,
        "author": author,
        "labels": labels,
        "url": blogger_url,
        "summary": summary,
        "image": image,
        "content": content
    })

posts.sort(
    key=lambda x: x["published"],
    reverse=True
)

os.makedirs("data", exist_ok=True)

with open(
    "data/posts.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        posts,
        f,
        ensure_ascii=False,
        indent=2
    )

print()
print(f"Articles Found : {len(posts)}")
print()
print("posts.json created successfully.")
print("Location: data/posts.json")
print()
print("Latest Articles:")
print()

for article in posts[:5]:
    print("•", article["title"])