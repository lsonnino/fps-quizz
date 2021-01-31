import numpy as np
import cv2
from util import *

###### SETTINGS ######
# Resolution
width = 1920
height = 1080
smoothness = 0.25

# Colors
background_color = (50, 50, 50)
foreground_color = (200, 200, 200)
text_color = foreground_color

# Text
font = cv2.FONT_HERSHEY_DUPLEX
stroke = 3
######################

# Constants
ANCHOR_BOTTOM_LEFT = 0
ANCHOR_BOTTOM_CENTER = 1
ANCHOR_BOTTOM_RIGHT = 2
ANCHOR_CENTER_LEFT = 3
ANCHOR_CENTER = 4
ANCHOR_CENTER_RIGHT = 5
ANCHOR_TOP_LEFT = 6
ANCHOR_TOP_CENTER = 7
ANCHOR_TOP_RIGHT = 8

# Preprocess colors: convert from RGB to BGR
# alternatively, frames can be converted using:
#    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
background_color = (background_color[2], background_color[1], background_color[0])
foreground_color = (foreground_color[2], foreground_color[1], foreground_color[0])
text_color = (text_color[2], text_color[1], text_color[0])

# Prepare smooth
kernel_size = min(height, width)
kernel = gaussian_kernel(sigma=smoothness, n=kernel_size)
kernel_fft = np.fft.fftshift(np.fft.fft2(resize_and_fix_origin(kernel, (height, width))))

def create_frame():
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    # Set background color
    frame[:, :, 0] = background_color[0]
    frame[:, :, 1] = background_color[1]
    frame[:, :, 2] = background_color[2]

    return frame

def draw_text(frame, text, position, size, anchor=ANCHOR_BOTTOM_LEFT):
    text_size = cv2.getTextSize(text, font, size, stroke)[0]
    x, y = position
    # Horizontal anchor. default: left
    if anchor % 3 == 1: # center
        x = position[0] - text_size[0] // 2
    elif anchor % 3 == 2: # right
        x = position[0] - text_size[0]
    # Vertical anchor. default: bottom
    if anchor // 3 == 1: # center
        y = position[1] - text_size[1] // 2
    elif anchor // 3 == 2: # top
        y = position[1] + text_size[1]

    cv2.putText(frame, text, (x, y), font, size, text_color, stroke, cv2.LINE_AA)

def draw_square(frame, position, size):
    # Get array indices
    s = size // 2
    x = (max(0, position[0] - s), min(width, position[0] + s))
    y = (max(0, position[1] - s), min(height, position[1] + s))

    # Draw
    frame[y[0]:y[1], x[0]:x[1], 0] = foreground_color[0]
    frame[y[0]:y[1], x[0]:x[1], 1] = foreground_color[1]
    frame[y[0]:y[1], x[0]:x[1], 2] = foreground_color[2]

def smooth(img):
    for i in range(img.shape[2]):
        img[:, :, i] = convolve(img[:, :, i], kernel_fft)
    return img
