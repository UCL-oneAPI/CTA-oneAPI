from pathlib import Path


def add_images():
    cwd = Path.cwd()
    image_path = Path.joinpath(cwd, 'images')
    html  = """
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


# with open('subgraphs.html', 'w') as f:
#     f.write(add_images())
