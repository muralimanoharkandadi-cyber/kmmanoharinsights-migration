import os
import xml.etree.ElementTree as ET

# Blogger Atom namespace
NS = {
    "atom": "http://www.w3.org/2005/Atom"
}

print("Reading feed.atom...")

# Read the Atom feed
tree = ET.parse("feed.atom")
root = tree.getroot()

entries = root.findall("atom:entry", NS)

print(f"Found {len(entries)} entries.")

first_post = None

# Find the first entry with both title and content
for entry in entries:

    title = entry.findtext("atom:title", default="", namespaces=NS)
    content = entry.findtext("atom:content", default="", namespaces=NS)

    if title.strip() and content.strip():
        first_post = {
            "title": title,
            "content": content
        }
        break

if first_post is None:
    print("No valid post found.")
    raise SystemExit

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{first_post['title']}</title>

<style>
body {{
    max-width:900px;
    margin:auto;
    padding:40px;
    font-family:Arial, Helvetica, sans-serif;
    line-height:1.8;
}}

img {{
    max-width:100%;
    height:auto;
}}

h1 {{
    color:#0B4EA2;
}}
</style>

</head>

<body>

<h1>{first_post['title']}</h1>

{first_post['content']}

</body>
</html>
"""

output_file = os.path.join("output", "article-test.html")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print()
print("SUCCESS!")
print("Created:")
print(output_file)