from PIL import Image, ImageDraw, ImageFont

FONTSIZE = 10
FONT = ImageFont.truetype('/usr/share/fonts/noto/NotoSerif-Bold.ttf', FONTSIZE)

BLOCK_WIDTH = 4
BLOCK_HEIGHT = 20
GAP_WIDTH = 2
GAP_HEIGHT = 2
HEIGHT = 50*BLOCK_HEIGHT
LEAF_MARGIN = 5

def textbox_size(message, offset, size):
    draw = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0, 0, 0, 0)))
    offset_x, offset_y = offset
    size_x, size_y = size
    _, _, width, height = draw.textbbox(
        (0, 0),
        message,
        font=FONT,
    )
    return width, height

def draw_text(draw, message, offset, size):
    offset_x, offset_y = offset
    size_x, size_y = size
    width, height = textbox_size(message, offset, size)

    draw.text(
        (
            offset_x + (size_x - width) / 2,
            offset_y + (size_y - height) / 2,
        ),
        text=message,
        fill=(0, 0, 0),
        font=FONT,
    )

def draw_leaf_text(im, draw, message, offset, size):
    offset_x, offset_y = offset
    size_x, size_y = size
    width, height = textbox_size(message, offset, size)

    img_text = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(img_text)
    draw_text.text(
        (0, 0),
        text=message,
        fill=(255, 255, 255),
        font=FONT,
    )
    img_text = img_text.rotate(-90, expand=True)
    im.alpha_composite(
        img_text,
        (
            offset_x + (size_x - height) // 2,
            offset_y + BLOCK_HEIGHT + LEAF_MARGIN,
        ),
    )


def draw_node(im, draw, node, x1, y1):
    # print(node, x1, y1)

    y2 = y1 + BLOCK_HEIGHT

    # draw children
    child_offset = x1
    for child in node.get_children():
        child_offset += draw_node(im, draw, child, child_offset, y2)

    width = node.get_count() * BLOCK_WIDTH
    x2 = x1 + width

    # draw self
    draw.rectangle(
        (x1, y1, x2-GAP_WIDTH, y2-GAP_HEIGHT),
        fill=node.get_colour(),
    )
    if node.children:
        draw_text(
            draw,
            node.get_name(),
            (x1, y1),
            (width, BLOCK_HEIGHT)
        )
    else:
        draw_leaf_text(
            im,
            draw,
            node.get_name(),
            (x1, y1),
            (width, BLOCK_HEIGHT)
        )

    return width


def plot(tree):
    width = tree.root.get_count() * BLOCK_WIDTH
    im = Image.new("RGBA", (width, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(im)

    # draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    draw_node(im, draw, tree.root, 0, 0)

    im = im.rotate(90, expand=True)
    im.save("tree_of_life.png")
