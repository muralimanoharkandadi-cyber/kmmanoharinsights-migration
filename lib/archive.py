from pathlib import Path
from collections import defaultdict
from datetime import datetime

OUTPUT_DIR = Path("output")


def render_archive(articles):

    archive = defaultdict(list)

    for article in sorted(
        articles,
        key=lambda x: x.get("published", ""),
        reverse=True,
    ):

        published = article.get("published", "")

        try:
            dt = datetime.fromisoformat(
                published.replace("Z", "+00:00")
            )
        except Exception:
            continue

        archive[(dt.year, dt.strftime("%B"))].append(article)

    folder = OUTPUT_DIR / "archive"
    folder.mkdir(parents=True, exist_ok=True)

    html = """<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="utf-8">

<title>Archive | KM Manohar Insights</title>

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

Article Archive

</p>

</div>

</header>

<main class="container">

<h2>Archive</h2>
"""

    years = sorted(
        {year for year, month in archive.keys()},
        reverse=True,
    )

    for year in years:

        html += f"<h2>{year}</h2>"

        months = [
            m for y, m in archive.keys()
            if y == year
        ]

        seen = []

        for month in months:

            if month in seen:
                continue

            seen.append(month)

            html += f"<h3>{month}</h3>"

            html += '<div class="articles">'

            for article in archive[(year, month)]:

                html += f"""
<article class="post-card">

<h3>

<a href="/{article['slug']}/">

{article['title']}

</a>

</h3>

<div class="post-meta">

{article.get('published','')[:10]}

</div>

<p>

{article.get('summary','')}

</p>

<a class="read-more"
href="/{article['slug']}/">

Read More →

</a>

</article>
"""

            html += "</div>"

    html += """

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

    print("Archive generated.")