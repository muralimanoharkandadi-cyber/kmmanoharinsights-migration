import json


def generate_article_schema(article):
    """
    Generate Schema.org Article JSON-LD
    """

    schema = {
        "@context": "https://schema.org",
        "@type": "Article",

        "headline": article.get("title", ""),
        "description": article.get("summary", ""),

        "author": {
            "@type": "Person",
            "name": article.get("author", "KM Manohar")
        },

        "publisher": {
            "@type": "Organization",
            "name": "KM Manohar Insights",
            "logo": {
                "@type": "ImageObject",
                "url": "https://www.kmmanoharinsights.com/assets/images/logo.png"
            }
        },

        "datePublished": article.get("published", ""),
        "dateModified": article.get(
            "last_updated",
            article.get("updated", "")
        ),

        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": article.get("canonical_url", "")
        },

        "url": article.get("canonical_url", ""),

        "image": article.get(
            "hero_image",
            article.get("image", "")
        ),

        "keywords": article.get("labels", []),

        "wordCount": article.get("word_count", 0),

        "timeRequired": f"PT{article.get('reading_time', 1)}M",

        "inLanguage": "en"
    }

    return (
        '<script type="application/ld+json">'
        + json.dumps(schema, indent=2, ensure_ascii=False)
        + "</script>"
    )