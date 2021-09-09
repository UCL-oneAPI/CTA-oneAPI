from pathlib import Path


def add_images(report_root):
    image_path = Path.joinpath(Path(report_root), 'images')
    html = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sub Images</title>
    </head>
    <body>
    """
    for image in image_path.glob("*.jpg"):
        name = str(image.name)
        html += """
        <img src="images/%s" width="600" height="450" />
        """ % name

    html += """
    </body>
    </html>
    """
    return html
