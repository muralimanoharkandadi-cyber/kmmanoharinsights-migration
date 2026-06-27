from pathlib import Path

OUTPUT_DIR = Path("output")


def generate_404():

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>404 - Page Not Found</title>
<link rel="stylesheet" href="/assets/css/style.css">
</head>

<body>

<div class="container">

<h1>404</h1>

<h2>Page Not Found</h2>

<p>
The page you're looking for doesn't exist or has been moved.
</p>

<p>
<a href="/">← Return to Homepage</a>
</p>

</div>

</body>
</html>
"""

    (OUTPUT_DIR / "404.html").write_text(
        html,
        encoding="utf-8",
    )

    print("404 page generated.")