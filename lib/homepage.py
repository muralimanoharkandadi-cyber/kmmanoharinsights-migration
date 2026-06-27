from pathlib import Path

OUTPUT_DIR = Path("output")
INDEX_TEMPLATE = Path("templates/index.html")


def render_homepage(articles):

    template = INDEX_TEMPLATE.read_text(encoding="utf-8")

    cards = []

    for article in articles:

        cards.append(f"""
<article class="post-card">

    <h2>
        <a href="{article['slug']}/">
            {article['title']}
        </a>
    </h2>

    <p class="post-summary">
        Read the complete article →
    </p>

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