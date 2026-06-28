from pathlib import Path

OUTPUT_DIR = Path("output")
INDEX_TEMPLATE = Path("templates/index.html")


def render_homepage(articles):

    template = INDEX_TEMPLATE.read_text(encoding="utf-8")

    cards = []

    for article in articles:

        image = article.get("image", "")

        summary = article.get("summary", "Read the complete article.")

        published = article.get("published", "")[:10]

        cards.append(f"""
<article class="post-card">

    <a href="{article['slug']}/">
        <img src="{image}" alt="{article['title']}" class="post-image">
    </a>

    <h2>
        <a href="{article['slug']}/">
            {article['title']}
        </a>
    </h2>

    <div class="post-meta">
        📅 {published}
    </div>

    <p class="post-summary">
        {summary}
    </p>

    <a class="read-more" href="{article['slug']}/">
        Read More →
    </a>

</article>
""")

    html = template.replace(
        "{{ARTICLES}}",
        "\n".join(cards)
    )

    output_file = OUTPUT_DIR / "index.html"

    output_file.write_text(
        html,
        encoding="utf-8"
    )

    return output_file