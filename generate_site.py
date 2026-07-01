from pathlib import Path
import json

print("***** GENERATE_SITE.PY VERSION 6 *****")

from lib.parser import load_articles
from lib.renderer_v3 import render_article
from lib.homepage import render_homepage
import lib.homepage
print("Homepage module:", lib.homepage.__file__)

from lib.assets import copy_assets
from lib.categories import render_categories
from lib.category_index import render_category_index
from lib.archive import render_archive
from lib.all_articles import render_all_articles
from lib.sitemap import generate_sitemap
from lib.robots import generate_robots
from lib.rss import generate_rss
from lib.error404 import generate_404
from lib.link_converter import convert_links
from lib.article_metadata import enrich_article
from lib.validator import validate_site
from lib.clean_build import clean_build

clean_build()

OUTPUT_DIR = Path("output")


def build_search_index(articles):
    """
    Generates:
    - output/search-index.json
    - output/data/posts.json
    """

    search = []

    for article in articles:
        search.append(
            {
                "title": article["title"],
                "slug": article["slug"],
                "summary": article.get("summary", ""),
                "labels": article.get("labels", []),
                "published": article.get("published", ""),
                "image": article.get("image", ""),
                "author": article.get("author", ""),
            }
        )

    output = OUTPUT_DIR / "search-index.json"

    output.write_text(
        json.dumps(search, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    data_dir = OUTPUT_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    posts_file = data_dir / "posts.json"

    posts_file.write_text(
        json.dumps(
            {
                "count": len(search),
                "posts": search,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Search index generated.")
    print("posts.json generated.")


def main():

    print("=" * 70)
    print("KM MANOHAR INSIGHTS STATIC SITE GENERATOR")
    print("=" * 70)

    clean_build()

    copy_assets()

    articles = load_articles()

    print(f"\nLoaded {len(articles)} articles.\n")

    for index, article in enumerate(articles):

        previous_article = (
            articles[index - 1]
            if index > 0
            else None
        )

        next_article = (
            articles[index + 1]
            if index < len(articles) - 1
            else None
        )

        article = enrich_article(article)

        article["content"] = convert_links(article["content"])

        render_article(
            article,
            previous_article,
            next_article,
            articles,
        )

        print(f"{index + 1:03d}  {article['slug']}")

    print("\nGenerating homepage...")
    homepage = render_homepage(articles)

    print("Generating All Articles page...")
    render_all_articles(articles)

    print("Generating category pages...")
    render_categories(articles)

    print("Generating category index...")
    render_category_index(articles)

    print("Generating archive...")
    render_archive(articles)

    print("Generating sitemap...")
    generate_sitemap(articles)

    print("Generating robots.txt...")
    generate_robots()

    print("Generating RSS feed...")
    generate_rss(articles)

    print("Generating 404 page...")
    generate_404()

    print("Generating search index...")
    build_search_index(articles)

    print("Running validator...")
    validate_site(articles)

    print("\n" + "=" * 70)
    print("BUILD COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"Articles           : {len(articles)}")
    print(f"Homepage           : {homepage}")
    print("All Articles Page  : output/articles/index.html")
    print("Categories         : Generated")
    print("Category Index     : output/categories/index.html")
    print("Archive            : output/archive/index.html")
    print("Search Index       : Generated")
    print("RSS Feed           : Generated")
    print("Sitemap            : Generated")
    print("Validator          : PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()
