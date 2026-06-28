from pathlib import Path
from xml.sax.saxutils import escape

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
        '<language>en-us</language>',
    ]

    for article in articles[:50]:

        title = escape(article["title"])
        summary = escape(article.get("summary", ""))
        link = f"{BASE_URL}/{article['slug']}/"
        pubdate = article.get("published", "")

        rss.extend([
            "<item>",
            f"<title>{title}</title>",
            f"<link>{link}</link>",
            f"<guid>{link}</guid>",
            f"<description>{summary}</description>",
            f"<pubDate>{pubdate}</pubDate>",
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