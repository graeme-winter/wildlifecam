import sys

import numpy as np
from matplotlib import pyplot as plt

import cv2


def baseline(filename):
    """Read the first frame from filename, assumed to be the background
    image."""

    capture = cv2.VideoCapture(filename)

    status, frame = capture.read()

    if not status:
        raise RuntimeError(f"Failed to read frame from {filename}")

    return frame


def scan(background_filename, filenames):
    """Scan through the frames in the given file, crop out the actual image
    (i.e. remove the time stamps etc.) then compute the total counts in the
    image: if something happens one may expect that this would change."""

    background = baseline(background_filename)[:1020, :, 0]
    background = cv2.GaussianBlur(background, (21, 21), 0)

    for filename in filenames:
        capture = cv2.VideoCapture(filename)

        ret, frame = capture.read()

        signal = 0

        while ret:
            crop = cv2.GaussianBlur(frame[:1020, :, 0], (21, 21), 0)

            diff = cv2.absdiff(background, crop)

            thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            if np.count_nonzero(thresh) > 10000:
                signal += 1

            ret, frame = capture.read()

        print(f"{filename}: {signal} frames")


if __name__ == "__main__":
    scan(sys.argv[1], sys.argv[2:])
