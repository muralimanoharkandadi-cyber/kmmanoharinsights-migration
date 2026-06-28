from pathlib import Path
import re
from collections import defaultdict

OUTPUT_DIR = Path("output")

IGNORE_LABELS = {
    "Focus Keywords",
    "Meta Description",
    "Draft",
    "Uncategorized",
}


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60]


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

        if len(posts) < 2:
            continue

        folder = base / slugify(label)
        folder.mkdir(parents=True, exist_ok=True)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="utf-8">

<title>{label} | KM Manohar Insights</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="stylesheet" href="/assets/css/style.css">

</head>

<body>

<header>
<div class="container">

<h1><a href="/">KM Manohar Insights</a></h1>

<p class="tagline">
Science • Technology • AI • Space • Quantum • Biotechnology
</p>

</div>
</header>

<main class="container">

<h2>{label}</h2>

<p>{len(posts)} Articles</p>

<div class="articles">
"""

        for article in posts:

            image = article.get("image", "")
            summary = article.get("summary", "")
            published = article.get("published", "")[:10]

            html += f"""
<article class="post-card">

<a href="/{article['slug']}/">
<img src="{image}" class="post-image" alt="{article['title']}">
</a>

<h3>
<a href="/{article['slug']}/">
{article['title']}
</a>
</h3>

<div class="post-meta">
📅 {published}
</div>

<p class="post-summary">
{summary}
</p>

<a class="read-more" href="/{article['slug']}/">
Read More →
</a>

</article>
"""

        html += """
</div>

</main>

<footer>

<div class="container">

© 2026 KM Manohar Insights

</div>

</footer>

</body>

</html>
"""

        (folder / "index.html").write_text(
            html,
            encoding="utf-8",
        )

        generated += 1

    print("=" * 60)
    print(f"Generated {generated} category pages.")
    print("=" * 60)