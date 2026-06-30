import math


def enrich_article(article):
    """
    Enriches an article dictionary with additional metadata.
    Safe to call multiple times.
    """

    text = article.get("content_text", "")

    words = len(text.split())

    article["word_count"] = words

    article["reading_time"] = max(1, math.ceil(words / 200))

    labels = article.get("labels", [])

    article["primary_category"] = labels[0] if labels else ""

    article["tags"] = labels

    article["hero_alt"] = article.get(
        "hero_alt",
        article.get("title", "")
    )

    article["hero_caption"] = article.get(
        "hero_caption",
        ""
    )

    slug = article.get("slug", "")

    article["canonical_url"] = (
        f"https://www.kmmanoharinsights.com/{slug}/"
    )

    article["breadcrumbs"] = [
        {
            "name": "Home",
            "url": "/",
        },
        {
            "name": article["primary_category"],
            "url": (
                f"/category/"
                f"{article['primary_category'].lower()}/"
            ) if article["primary_category"] else "/",
        },
        {
            "name": article.get("title", ""),
            "url": f"/{slug}/",
        },
    ]

    article["last_updated"] = article.get(
        "updated",
        article.get("published", "")
    )

    return article