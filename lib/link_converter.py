import re

BLOG_URL = "https://kmmanohar1602.blogspot.com"

def convert_links(html):
    if not html:
        return html

    pattern = re.compile(
        r'https://kmmanohar1602\.blogspot\.com/\d{4}/\d{2}/([^"]+?)\.html'
    )

    return pattern.sub(lambda m: f'/{m.group(1)}/', html)