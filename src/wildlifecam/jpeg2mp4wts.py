import sys
import os

import numpy as np
from PIL import Image, ImageFont, ImageDraw
import cv2


def main(file_template, start=0, end=100000):

    font = ImageFont.truetype("Menlo.ttc", 32)
    capture = cv2.VideoCapture(0)
    out = cv2.VideoWriter(
        "out.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 20.0, (1640, 1232)
    )

    print(f"Processing images {start} to {end} inclusive")

    for j in range(start, end + 1):
        filename = file_template % j
        print(filename)

        if not os.path.exists(filename):
            break
        image = Image.open(filename)
        timestamp = image._getexif()[36867]
        day, time = timestamp.split()
        day = day.replace(":", "/")
        time = time[:5]
        draw = ImageDraw.Draw(image)
        draw.text((16, 16), f"{time}", (0xFF, 0xFF, 0xFF), font=font)
        # this inverts RGB but we don't care because monochrome
        out.write(np.asarray(image))

    out.release()
    capture.release()


if __name__ == "__main__":
    main(sys.argv[1], start=int(sys.argv[2]), end=int(sys.argv[3]))
