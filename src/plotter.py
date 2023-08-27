from PIL import Image, ImageDraw, ImageFont

FONTSIZE = 20
FONT = ImageFont.truetype('/usr/share/fonts/noto/NotoSerif-Bold.ttf', FONTSIZE)

BLOCK_WIDTH = 18*6
BLOCK_HEIGHT = 35
GAP_WIDTH = 3
GAP_HEIGHT = 3
HEIGHT = 25*BLOCK_HEIGHT

def draw_text(draw, message, offset, size):
    offset_x, offset_y = offset
    size_x, size_y = size
    _, _, width, height = draw.textbbox(
        (0, 0),
        message,
        font=FONT,
    )

    draw.text(
        (
            offset_x + (size_x - width) / 2,
            offset_y + (size_y - height) / 2,
        ),
        text=message,
        fill=(0, 0, 0),
        font=FONT,
    )


def draw_node(draw, node, x1, y1):
    # print(node, x1, y1)

    y2 = y1 + BLOCK_HEIGHT

    # draw children
    child_offset = x1
    for child in node.get_children():
        child_offset += draw_node(draw, child, child_offset, y2)

    width = node.get_count() * BLOCK_WIDTH
    x2 = x1 + width

    # draw self
    draw.rectangle(
        (x1, y1, x2-GAP_WIDTH, y2-GAP_HEIGHT),
        fill=node.get_colour(),
    )
    draw_text(
        draw,
        node.get_name(),
        (x1, y1),
        (width, BLOCK_HEIGHT)
    )

    return width


def plot(tree):
    width = tree.root.get_count() * BLOCK_WIDTH
    im = Image.new('RGB', (width, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    # draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    draw_node(draw, tree.root, 0, 0)

    im.save("tree_of_life.png")
