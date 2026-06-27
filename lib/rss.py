from pathlib import Path

OUTPUT_DIR = Path("output")
BASE_URL = "https://www.kmmanoharinsights.com"


def generate_rss(articles):

    rss = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '<channel>',
        '<title>KM Manohar Insights</title>',
        f'<link>{BASE_URL}</link>',
        '<description>Science • Technology • AI • Space • Quantum • Biotechnology</description>',
    ]

    for article in articles[:50]:

        rss.extend([
            "<item>",
            f"<title>{article['title']}</title>",
            f"<link>{BASE_URL}/{article['slug']}/</link>",
            f"<description>{article.get('summary', '')}</description>",
            "</item>",
        ])

    rss.extend([
        "</channel>",
        "</rss>",
    ])

    (OUTPUT_DIR / "rss.xml").write_text(
        "\n".join(rss),
        encoding="utf-8",
    )

    print("RSS feed generated.")