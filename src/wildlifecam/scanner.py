import sys

import numpy as np
from matplotlib import pyplot as plt

import cv2


def scan(filename):
    """Scan through the frames in the given file, crop out the actual image
    (i.e. remove the time stamps etc.) then compute the total counts in the
    image: if something happens one may expect that this would change."""

    capture = cv2.VideoCapture(filename)

    sizes = []

    ret, frame = capture.read()

    while ret:
        crop = frame[:, :1020, 0]
        sizes.append(np.sum(crop))
        ret, frame = capture.read()

    mean = sum(sizes) / len(sizes)
    print(f"{100 * (max(sizes) - min(sizes)) / mean:.2f}% variation")


if __name__ == "__main__":
    scan(sys.argv[1])
