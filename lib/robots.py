from pathlib import Path

OUTPUT_DIR = Path("output")
BASE_URL = "https://www.kmmanoharinsights.com"


def generate_robots():

    robots = f"""User-agent: *

Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""

    (OUTPUT_DIR / "robots.txt").write_text(
        robots,
        encoding="utf-8",
    )

    print("robots.txt generated.")