from pathlib import Path

BASE_TEMPLATE = Path("templates/base.html")
OUTPUT_DIR = Path("output")


def load_base_template():
    return BASE_TEMPLATE.read_text(encoding="utf-8")


def build_related(article, all_articles):
    labels = set(article.get("labels", []))

    if not labels:
        return ""

    related = []

    for other in all_articles:
        if other["slug"] == article["slug"]:
            continue

        score = len(labels.intersection(other.get("labels", [])))
        if score:
            related.append((score, other))

    related.sort(key=lambda x: x[0], reverse=True)

    if not related:
        return ""

    html = """
<section class="related-articles">
<h2>Related Articles</h2>
<ul>
"""

    for _, item in related[:5]:
        html += f"""
<li>
<a href="/{item['slug']}/">{item['title']}</a>
</li>
"""

    html += """
</ul>
</section>
"""

    return html


def render_html(article, previous_article, next_article, all_articles):

    html = load_base_template()

    navigation = '<div class="article-nav">'

    if previous_article:
        navigation += f'<a class="nav-button" href="/{previous_article["slug"]}/">⬅ Previous</a>'
    else:
        navigation += "<span></span>"

    navigation += '<a class="nav-button" href="/">🏠 Home</a>'

    if next_article:
        navigation += f'<a class="nav-button" href="/{next_article["slug"]}/">Next ➡</a>'
    else:
        navigation += "<span></span>"

    navigation += "</div>"

    related = build_related(article, all_articles)

    hero = ""
    if article.get("image"):
        hero = f"""
<div class="hero-image">
    <img src="{article['image']}" alt="{article['title']}">
</div>
"""

    content = hero + article["content"] + navigation + related

    html = html.replace("{{TITLE}}", article["title"])
    html = html.replace("{{AUTHOR}}", article.get("author", "KM Manohar"))
    html = html.replace("{{PUBLISHED}}", article.get("published", "")[:10])
    html = html.replace("{{DESCRIPTION}}", article.get("summary", article["title"]))
    html = html.replace(
        "{{CANONICAL}}",
        f"https://www.kmmanoharinsights.com/{article['slug']}/"
    )
    html = html.replace("{{CONTENT}}", content)

    return html


def save_article(article, previous_article, next_article, all_articles):

    article_dir = OUTPUT_DIR / article["slug"]
    article_dir.mkdir(parents=True, exist_ok=True)

    html = render_html(
        article,
        previous_article,
        next_article,
        all_articles,
    )

    output_file = article_dir / "index.html"

    output_file.write_text(
        html,
        encoding="utf-8",
    )

    return output_file


def render_article(article, previous_article, next_article, all_articles):
    return save_article(
        article,
        previous_article,
        next_article,
        all_articles,
    )