from pathlib import Path
import json
print("***** GENERATE_SITE.PY VERSION 2 *****")

from lib.parser import load_articles
from lib.renderer import render_article
from lib.homepage import render_homepage
from lib.assets import copy_assets
from lib.categories import render_categories
from lib.sitemap import generate_sitemap
from lib.robots import generate_robots
from lib.rss import generate_rss
from lib.error404 import generate_404

OUTPUT_DIR = Path("output")


def build_search_index(articles):
    """
    Generates output/search-index.json
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
            }
        )

    output = OUTPUT_DIR / "search-index.json"

    output.write_text(
        json.dumps(search, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Search index generated.")


def main():

    print("KM Manohar Insights Generator")

    copy_assets()

    articles = load_articles()

    print(f"Generating {len(articles)} articles...\n")

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

        render_article(
            article,
            previous_article,
            next_article,
            articles,
        )

        print(f"{index + 1:03d}  {article['slug']}")

    homepage = render_homepage(articles)
    
    render_categories(articles)
    
    print("Calling generate_sitemap...")
    
    generate_sitemap(articles)
    
    generate_robots()
    
    generate_rss(articles)
    
    generate_404()

    build_search_index(articles)

    print("\nFinished.")
    print(f"Generated {len(articles)} articles.")
    print(f"Homepage: {homepage}")


if __name__ == "__main__":
    main()