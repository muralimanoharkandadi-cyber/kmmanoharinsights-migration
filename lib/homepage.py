from pathlib import Path

OUTPUT_DIR = Path("output")
INDEX_TEMPLATE = Path("templates/index.html")

HOMEPAGE_LIMIT = 20


def build_card(article):
    image = article.get("image", "")
    title = article.get("title", "Untitled")
    summary = article.get("summary", "Read the complete article.")
    published = article.get("published", "")[:10]
    slug = article["slug"]

    return f"""
<article class="post-card">

    <a href="{slug}/">
        <img src="{image}" alt="{title}" class="post-image">
    </a>

    <div class="post-content">

        <div class="post-meta">
            {published}
        </div>

        <h2>
            <a href="{slug}/">
                {title}
            </a>
        </h2>

        <p class="post-summary">
            {summary}
        </p>

        <a class="read-more" href="{slug}/">
            Read More →
        </a>

    </div>

</article>
"""


def render_homepage(articles):

    template = INDEX_TEMPLATE.read_text(encoding="utf-8")

    latest = sorted(
        articles,
        key=lambda x: x.get("published", ""),
        reverse=True
    )[:HOMEPAGE_LIMIT]

    cards = "\n".join(build_card(article) for article in latest)

    print("PLACEHOLDER FOUND:", "{{ARTICLES}}" in template)
    print("CARDS:", len(cards))

    html = template.replace("{{ARTICLES}}", cards)

    print("PLACEHOLDER AFTER REPLACE:", "{{ARTICLES}}" in html)

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "index.html"

    output_file.write_text(
        html,
        encoding="utf-8"
    )

    print(f"Homepage generated: {output_file}")

    return output_file