import argparse
import os
import time

from PIL import Image, ImageDraw, ImageFont



def indent(img_width, h, text, text_width,  img_draw, font,color):
    w = img_width
    while 1:
        if w > 40:
            img_draw.text((w, h), text, font=font, fill=color)
        else:
            break
        w = w - text_width - 20


def no_indent(w, h, text, text_width, img_width, img_draw, font,  color):
    while 1:
        if w + text_width + 10 < img_width - 40:
            img_draw.text((w, h), text, font=font, fill=color)
        else:
            break
        w = w + text_width + 20


def image_add_text(file, text, color='white'):
    p = file.rindex(".")
    ext = file[p:]
    font = ImageFont.truetype('./arial.ttf', 40)
    img = Image.open(file).convert('RGBA')
    text_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    img_draw = ImageDraw.Draw(text_img)
    img_width, img_height = img.size
    text_width, text_height = font.getsize(text)
    rows = img_height // text_height + 1

    white = (255, 255, 255, 60)
    blue = (0, 0, 255, 60)
    red = (255, 0, 0, 60)
    orange = (255, 156, 0, 60)
    yellow = (255, 255, 0, 60)
    green = (0, 255, 0, 60)
    black = (0, 0, 0, 60)
    colors = {'white': white, 'blue': blue, 'red': red, 'orange': orange, 'yellow': yellow, 'green': green, 'black':black}

    h = 0
    for r in range(1, rows):
        if h < img_height:
            if r % 2 == 0:
                indent(img_width, h, text, text_width, img_draw,font, colors[color])
            else:
                no_indent(0, h, text, text_width, img_width, img_draw, font, colors[color])
        h = h + text_height

    new_img = Image.alpha_composite(img, text_img).convert('RGB')
    # new_img.show()
    filename = str(int(time.time())) + ext
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/image_watermark")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    new_img.save(os.path.join(dir_path,filename))
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--color", type=str, default='white', choices=['white', 'blue', 'red', 'orange', 'yellow', 'green', 'black'], help="chocie one color [white, blue, red, orange, yellow, green, black] ")
    args = parser.parse_args()
    try:
        if os.path.exists(args.file):
             image_add_text(args.file, args.text, args.color)
    except Exception as err:
        print(err)
