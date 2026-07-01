from pathlib import Path
from collections import defaultdict
import re

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


def render_category_index(articles):

    categories = defaultdict(int)

    for article in articles:

        for label in article.get("labels", []):

            label = normalize(label)

            if label in IGNORE_LABELS:
                continue

            categories[label] += 1

    generated = sum(
        1 for category in categories
        if categories[category] >= 2
    )

    OUTPUT_DIR.mkdir(exist_ok=True)

    folder = OUTPUT_DIR / "categories"
    folder.mkdir(parents=True, exist_ok=True)

    html = f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="utf-8">

<title>Categories | KM Manohar Insights</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="stylesheet" href="/assets/css/style.css">

</head>

<body>

<header>

<div class="container">

<h1>
<a href="/">KM Manohar Insights</a>
</h1>

<p class="tagline">
Browse by Topic
</p>

</div>

</header>

<main class="container">

<h2>Categories</h2>

<p>
<strong>{generated}</strong> Categories
</p>

<div class="articles">
"""

    for category in sorted(categories):

        count = categories[category]

        if count < 2:
            continue

        slug = slugify(category)

        html += f"""
<article class="post-card">

<h2>
<a href="/categories/{slug}/">
{category}
</a>
</h2>

<p>{count} Articles</p>

<a class="read-more" href="/categories/{slug}/">
Browse →
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

    print(f"Generated Category Index ({generated} categories).")