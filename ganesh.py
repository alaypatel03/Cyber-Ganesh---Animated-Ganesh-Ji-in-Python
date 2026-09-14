import turtle
import random
import math

from PIL import Image, ImageOps, ImageEnhance, ImageFilter


# ============================================================
#                  SETTINGS
# ============================================================

IMAGE_FILE = "ganesh.png"

IMAGE_WIDTH = 180
IMAGE_HEIGHT = 220

# 1 = maximum detail
# 2 = recommended
# 3 = faster
STEP = 2

OM_SIZE = 7

# Animation
BATCH_SIZE = 45
ANIMATION_DELAY = 5

# Pixel difference required to consider it part of the idol
THRESHOLD = 35


# ============================================================
#                  LOAD IMAGE
# ============================================================

try:

    original = Image.open(IMAGE_FILE)

except FileNotFoundError:

    print("\nERROR: ganesh.png not found!")
    print("Make sure ganesh.png is beside this Python file.")
    input("\nPress ENTER to exit...")
    exit()


# ============================================================
#                  PROCESS IMAGE
# ============================================================

# ------------------------------------------------------------
# If PNG has transparency
# ------------------------------------------------------------

if original.mode == "RGBA":

    alpha = original.getchannel("A")

    gray = ImageOps.grayscale(original)

    # Transparent area becomes white
    white = Image.new(
        "L",
        original.size,
        255
    )

    img = Image.composite(
        gray,
        white,
        alpha
    )

    has_transparency = True

else:

    img = ImageOps.grayscale(original)

    has_transparency = False


# ------------------------------------------------------------
# Resize while maintaining aspect ratio
# ------------------------------------------------------------

img.thumbnail(
    (IMAGE_WIDTH, IMAGE_HEIGHT),
    Image.Resampling.LANCZOS
)


# ------------------------------------------------------------
# Create white canvas
# ------------------------------------------------------------

canvas = Image.new(
    "L",
    (IMAGE_WIDTH, IMAGE_HEIGHT),
    255
)

offset_x = (
    IMAGE_WIDTH - img.width
) // 2

offset_y = (
    IMAGE_HEIGHT - img.height
) // 2

canvas.paste(
    img,
    (offset_x, offset_y)
)

img = canvas


# ============================================================
#                  ENHANCE DETAILS
# ============================================================

img = ImageEnhance.Contrast(img).enhance(2.5)

img = ImageEnhance.Sharpness(img).enhance(3)

img = img.filter(
    ImageFilter.SHARPEN
)


# ============================================================
#              FIND BACKGROUND BRIGHTNESS
# ============================================================

pixels = img.load()

# Take corners as background reference
corners = [
    pixels[0, 0],
    pixels[IMAGE_WIDTH - 1, 0],
    pixels[0, IMAGE_HEIGHT - 1],
    pixels[IMAGE_WIDTH - 1, IMAGE_HEIGHT - 1]
]

background = sum(corners) / len(corners)


# ============================================================
#                  CREATE OM POINTS
# ============================================================

points = []


for y in range(
    0,
    IMAGE_HEIGHT,
    STEP
):

    for x in range(
        0,
        IMAGE_WIDTH,
        STEP
    ):

        value = pixels[x, y]

        difference = abs(
            value - background
        )

        # ----------------------------------------------------
        # Detect the actual Ganeshji
        # ----------------------------------------------------

        if difference > THRESHOLD:

            # Stronger details get larger Om
            if difference > 120:
                size = 8

            elif difference > 80:
                size = 7

            else:
                size = 6

            points.append(
                (
                    x,
                    y,
                    difference,
                    size
                )
            )


# ============================================================
#                  REMOVE NOISE
# ============================================================

# If there are too many points, keep the strongest details.
MAX_POINTS = 12000

if len(points) > MAX_POINTS:

    points.sort(
        key=lambda p: p[2],
        reverse=True
    )

    points = points[:MAX_POINTS]


# ============================================================
#              ORGANIZE FOR ANIMATION
# ============================================================

# We don't simply randomly scatter everything.
#
# The animation moves from top to bottom, making it look
# like the Ganeshji is being typed/drawn.

points.sort(
    key=lambda p: (
        p[1],
        p[0]
    )
)


# Add slight randomness inside nearby areas
random.seed(10)

for i in range(
    0,
    len(points),
    100
):

    section = points[
        i:i + 100
    ]

    random.shuffle(section)

    points[i:i + 100] = section


# ============================================================
#                  TURTLE WINDOW
# ============================================================

screen = turtle.Screen()

screen.setup(
    width=1000,
    height=900
)

screen.bgcolor(
    "#050505"
)

screen.title(
    "ॐ  GANESHJI  ॐ"
)

screen.tracer(
    False
)


# ============================================================
#                  TURTLE
# ============================================================

pen = turtle.Turtle()

pen.hideturtle()
pen.penup()
pen.speed(0)


# ============================================================
#                  OM FONT
# ============================================================

# Windows:
FONT = "Nirmala UI"

# If ॐ does not appear correctly,
# change it to:
#
# FONT = "Arial Unicode MS"


# ============================================================
#             CONVERT IMAGE → TURTLE
# ============================================================

def turtle_x(x):

    return (
        x - IMAGE_WIDTH / 2
    ) * 4.8


def turtle_y(y):

    return (
        IMAGE_HEIGHT / 2 - y
    ) * 3.7


# ============================================================
#                  DRAW OM
# ============================================================

def draw_om(x, y, difference, size):

    tx = turtle_x(x)
    ty = turtle_y(y)

    pen.goto(
        tx,
        ty
    )

    # Create shading using different whites
    if difference > 120:

        pen.color("#FFFFFF")

    elif difference > 80:

        pen.color("#DDDDDD")

    else:

        pen.color("#AAAAAA")


    pen.write(
        "ॐ",
        align="center",
        font=(
            FONT,
            size,
            "bold"
        )
    )


# ============================================================
#                  ANIMATION
# ============================================================

print()
print("======================================")
print("       ॐ GANESHJI ॐ")
print("======================================")
print()
print("Image loaded successfully.")
print("Creating Ganeshji from ॐ symbols...")
print()
print("Total ॐ symbols:", len(points))
print()


def animate(index):

    end = min(
        index + BATCH_SIZE,
        len(points)
    )

    # Draw next batch
    for i in range(
        index,
        end
    ):

        x, y, difference, size = points[i]

        draw_om(
            x,
            y,
            difference,
            size
        )


    screen.update()


    # Continue animation
    if end < len(points):

        screen.ontimer(
            lambda: animate(end),
            ANIMATION_DELAY
        )

    else:

        finished()


# ============================================================
#                  FINISHED
# ============================================================

def finished():

    # Final large Om
    pen.goto(
        0,
        -385
    )

    pen.color(
        "#FFD700"
    )

    pen.write(
        "",
        align="center",
        font=(
            FONT,
            28,
            "bold"
        )
    )

    screen.update()

    print()
    print("======================================")
    print("          GANESHJI COMPLETE")
    print("======================================")
    print()
    print("Created entirely using ॐ")
    print()


# ============================================================
#                  START
# ============================================================

animate(0)

screen.mainloop()