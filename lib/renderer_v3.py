from pathlib import Path

BASE_TEMPLATE = Path("templates/article_v3.html")
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
<li><a href="/{item['slug']}/">{item['title']}</a></li>
"""

    html += """
</ul>
</section>
"""

    return html


def build_navigation(previous_article, next_article):
    html = '<div class="article-nav">'

    if previous_article:
        html += (
            f'<a class="nav-button" '
            f'href="/{previous_article["slug"]}/">⬅ Previous</a>'
        )
    else:
        html += "<span></span>"

    html += '<a class="nav-button" href="/">🏠 Home</a>'

    if next_article:
        html += (
            f'<a class="nav-button" '
            f'href="/{next_article["slug"]}/">Next ➡</a>'
        )
    else:
        html += "<span></span>"

    html += "</div>"

    return html


def build_hero(article):
    if not article.get("image"):
        return ""

    return f"""
<div class="hero-image">
    <img src="{article['image']}" alt="{article['title']}" loading="lazy">
</div>
"""


def render_html(article, previous_article, next_article, all_articles):

    html = load_base_template()

    published = article.get("published", "")[:10]
    summary = article.get("summary", article["title"])
    author = article.get("author", "KM Manohar")
    canonical = f"https://www.kmmanoharinsights.com/{article['slug']}/"

    content = article.get("content", "")

    word_count = len(content.split())
    reading_time = max(1, round(word_count / 220))

    html = html.replace("{{TITLE}}", article["title"])
    html = html.replace("{{DESCRIPTION}}", summary)
    html = html.replace("{{AUTHOR}}", author)
    html = html.replace("{{PUBLISHED}}", published)
    html = html.replace("{{DATE}}", published)
    html = html.replace("{{WORD_COUNT}}", str(word_count))
    html = html.replace("{{READING_TIME}}", str(reading_time))
    html = html.replace("{{CANONICAL}}", canonical)

    html = html.replace("{{HERO}}", build_hero(article))
    html = html.replace("{{CONTENT}}", content)
    html = html.replace(
        "{{NAVIGATION}}",
        build_navigation(previous_article, next_article),
    )
    html = html.replace(
        "{{RELATED}}",
        build_related(article, all_articles),
    )

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