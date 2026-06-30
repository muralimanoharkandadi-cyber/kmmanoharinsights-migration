from pathlib import Path

TEMPLATE = Path("templates/article_v2.html")
OUTPUT_DIR = Path("output")


def load_template():
    return TEMPLATE.read_text(encoding="utf-8")


def build_related(article, all_articles):
    labels = set(article.get("labels", []))

    related = []

    for other in all_articles:
        if other["slug"] == article["slug"]:
            continue

        score = len(labels.intersection(other.get("labels", [])))

        if score:
            related.append((score, other))

    related.sort(reverse=True, key=lambda x: x[0])

    if not related:
        return ""

    items = []

    for _, item in related[:5]:
        items.append(
            f'<li><a href="/{item["slug"]}/">{item["title"]}</a></li>'
        )

    return f"""
<section class="related">
<h2>Related Articles</h2>
<ul>
{''.join(items)}
</ul>
</section>
"""


def build_navigation(previous_article, next_article):

    prev_link = ""

    if previous_article:
        prev_link = (
            f'<a class="nav-card prev" '
            f'href="/{previous_article["slug"]}/">← '
            f'{previous_article["title"]}</a>'
        )

    next_link = ""

    if next_article:
        next_link = (
            f'<a class="nav-card next" '
            f'href="/{next_article["slug"]}/">'
            f'{next_article["title"]} →</a>'
        )

    return f"""
<nav class="article-navigation">
{prev_link}
<a class="nav-home" href="/">Home</a>
{next_link}
</nav>
"""


def render_html(article, previous_article, next_article, all_articles):

    html = load_template()

    hero = ""

    if article.get("image"):
        hero = (
            f'<figure class="hero">'
            f'<img src="{article["image"]}" '
            f'alt="{article["title"]}">'
            f'</figure>'
        )

    html = html.replace("{{TITLE}}", article["title"])
    html = html.replace(
        "{{DESCRIPTION}}",
        article.get("summary", article["title"])
    )
    html = html.replace(
        "{{AUTHOR}}",
        article.get("author", "KM Manohar")
    )
    html = html.replace(
        "{{DATE}}",
        article.get("published", "")[:10]
    )
    html = html.replace(
        "{{CANONICAL}}",
        f"https://www.kmmanoharinsights.com/{article['slug']}/"
    )
    html = html.replace("{{HERO}}", hero)
    html = html.replace("{{CONTENT}}", article["content"])
    html = html.replace(
        "{{NAVIGATION}}",
        build_navigation(previous_article, next_article)
    )
    html = html.replace(
        "{{RELATED}}",
        build_related(article, all_articles)
    )

    return html


def render_article(article, previous_article, next_article, all_articles):

    article_dir = OUTPUT_DIR / article["slug"]
    article_dir.mkdir(parents=True, exist_ok=True)

    output = article_dir / "index.html"

    output.write_text(
        render_html(
            article,
            previous_article,
            next_article,
            all_articles,
        ),
        encoding="utf-8",
    )

    return output