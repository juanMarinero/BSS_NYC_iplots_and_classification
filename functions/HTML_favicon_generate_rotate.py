#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :
from IPython.display import display, HTML
from PIL import Image, ImageFont, ImageDraw
import math
import io
import base64


def add_diagonal_text(text, fontsize, backgroundcolor, textcolor, angle, font):
    # Create the image using PIL
    font = ImageFont.truetype(font, fontsize)
    width, height = font.getsize(text)

    # Create an image to hold the text
    text_image = Image.new("RGBA", (width, height), color=backgroundcolor)
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0, 0), text, font=font, fill=textcolor)

    # Rotate the text image by the specified angle
    rotated_text_image = text_image.rotate(angle, expand=True)

    return rotated_text_image


def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def HTML_favicon_generate_rotate(
    text,
    fontsize=22,
    backgroundcolor="purple",
    textcolor="white",
    angle=-35,
    font="/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf",
):
    diagonal_image = add_diagonal_text(
        text, fontsize, backgroundcolor, textcolor, angle, font
    )
    favicon_base64 = image_to_base64(diagonal_image)

    favicon_url = f"data:image/png;base64,{favicon_base64}"

    display(
        HTML(f'<link rel="shortcut icon" type="image/x-icon" href="{favicon_url}">')
    )
