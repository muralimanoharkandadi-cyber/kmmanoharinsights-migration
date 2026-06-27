from pathlib import Path

OUTPUT_DIR = Path("output")
BASE_URL = "https://www.kmmanoharinsights.com"


def generate_sitemap(articles):

    urls = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    # Homepage
    urls.extend([
        "<url>",
        f"<loc>{BASE_URL}/</loc>",
        "</url>"
    ])

    # Articles
    for article in articles:
        urls.extend([
            "<url>",
            f"<loc>{BASE_URL}/{article['slug']}/</loc>",
            "</url>"
        ])

    urls.append("</urlset>")

    (OUTPUT_DIR / "sitemap.xml").write_text(
        "\n".join(urls),
        encoding="utf-8"
    )

    print("Sitemap generated.")