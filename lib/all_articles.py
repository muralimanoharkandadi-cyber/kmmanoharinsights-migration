from pathlib import Path

OUTPUT_DIR = Path("output")


def render_all_articles(articles):

    articles = sorted(
        articles,
        key=lambda x: x.get("published", ""),
        reverse=True,
    )

    folder = OUTPUT_DIR / "articles"
    folder.mkdir(parents=True, exist_ok=True)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="utf-8">

<title>All Articles | KM Manohar Insights</title>

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

<h2>All Articles</h2>

<p><strong>{len(articles)}</strong> Native Articles</p>

<div class="articles">
"""

    for article in articles:

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

    print(f"Generated All Articles page ({len(articles)} articles).")