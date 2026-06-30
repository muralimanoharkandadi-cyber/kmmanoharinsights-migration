from bs4 import BeautifulSoup, Comment

CHATGPT_ATTRS = [
    "data-message-author-role",
    "data-message-model-slug",
    "data-message-id",
    "data-turn",
    "data-turn-id",
    "data-testid",
]


def clean_content(html: str) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    # Remove <!--more-->
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if "more" in comment.lower():
            comment.extract()

    # Remove ChatGPT wrapper elements
    for tag in soup.find_all(True):
        if any(attr in tag.attrs for attr in CHATGPT_ATTRS):
            tag.decompose()

    # Remove unwanted attributes
    for tag in soup.find_all(True):
        tag.attrs = {
            k: v
            for k, v in tag.attrs.items()
            if k in ("href", "src", "alt", "title")
        }

    # Remove empty paragraphs
    for p in soup.find_all("p"):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()

    # Normalize heading hierarchy
    for h in soup.find_all(["h1"]):
        h.name = "h2"

    # Remove duplicate consecutive headings
    previous = None
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(" ", strip=True)

        if previous == text:
            tag.decompose()
            continue

        previous = text

    # Lazy-load images
    for img in soup.find_all("img"):
        img["loading"] = "lazy"
        img["decoding"] = "async"

    return str(soup)