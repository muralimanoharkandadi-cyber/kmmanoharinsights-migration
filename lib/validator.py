from pathlib import Path

OUTPUT_DIR = Path("output")


def validate_site(articles):

    report = []

    total = len(articles)

    report.append(("Articles Parsed", total))

    rendered = 0

    for article in articles:

        page = OUTPUT_DIR / article["slug"] / "index.html"

        if page.exists():
            rendered += 1

    report.append(("Articles Rendered", rendered))

    homepage = (OUTPUT_DIR / "index.html").exists()
    report.append(("Homepage", homepage))

    all_articles = (
        OUTPUT_DIR / "articles" / "index.html"
    ).exists()

    report.append(("All Articles", all_articles))

    category_index = (
        OUTPUT_DIR / "categories" / "index.html"
    ).exists()

    report.append(("Category Index", category_index))

    archive = (
        OUTPUT_DIR / "archive" / "index.html"
    ).exists()

    report.append(("Archive", archive))

    sitemap = (
        OUTPUT_DIR / "sitemap.xml"
    ).exists()

    report.append(("Sitemap", sitemap))

    rss = (
        OUTPUT_DIR / "rss.xml"
    ).exists()

    report.append(("RSS", rss))

    robots = (
        OUTPUT_DIR / "robots.txt"
    ).exists()

    report.append(("robots.txt", robots))

    page404 = (
        OUTPUT_DIR / "404.html"
    ).exists()

    report.append(("404 Page", page404))

    search = (
        OUTPUT_DIR / "search-index.json"
    ).exists()

    report.append(("Search Index", search))

    print()
    print("=" * 70)
    print("PROJECT A VALIDATION")
    print("=" * 70)

    for item, value in report:

        if isinstance(value, bool):

            status = "PASS" if value else "FAIL"

            print(f"{item:<25} {status}")

        else:

            print(f"{item:<25} {value}")

    if rendered == total:

        print()
        print("RESULT : SITE VALIDATION PASSED")

    else:

        print()
        print("RESULT : SITE VALIDATION FAILED")

    print("=" * 70)