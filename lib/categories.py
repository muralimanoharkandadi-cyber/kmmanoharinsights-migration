from pathlib import Path
import re
from collections import defaultdict

OUTPUT_DIR = Path("output")

# Ignore labels that should not become public category pages
IGNORE_LABELS = {
    "Focus Keywords",
    "Meta Description",
    "Draft",
    "Uncategorized",
}


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:60]   # Limit folder names to 60 characters


def normalize(label):
    return " ".join(label.split()).title()


def render_categories(articles):

    categories = defaultdict(list)

    for article in articles:

        for label in article.get("labels", []):

            label = normalize(label)

            if label in IGNORE_LABELS:
                continue

            categories[label].append(article)

    base = OUTPUT_DIR / "categories"
    base.mkdir(parents=True, exist_ok=True)

    generated = 0

    for label, posts in sorted(categories.items()):

        # Skip very small categories
        if len(posts) < 2:
            continue

        folder = base / slugify(label)
        folder.mkdir(parents=True, exist_ok=True)

        html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>{label} | KM Manohar Insights</title>

<link rel="stylesheet" href="/assets/css/style.css">

</head>

<body>

<header>

<div class="container">

<h1>
<a href="/">KM Manohar Insights</a>
</h1>

</div>

</header>

<main class="container">

<h2>{label}</h2>

<p>{len(posts)} Articles</p>
"""

        for article in posts:

            html += f"""
<article class="post-card">

<h3>

<a href="/{article['slug']}/">

{article['title']}

</a>

</h3>

<p>{article.get('summary','')}</p>

</article>
"""

        html += """

</main>

</body>

</html>
"""

        (folder / "index.html").write_text(
            html,
            encoding="utf-8",
        )

        generated += 1

    print("=" * 60)
    print(f"Generated {generated} quality category pages.")
    print("=" * 60)