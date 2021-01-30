import numpy as np
import cv2
from graphics import *

###### MAIN PARAMETERS ######
# The fps's to put into the quizz
FPS = [30, 60, 120] # For now, fps's must be divisors of the biggest number of FPS
# Number of iterations
n_iterations = 2
# Number of seconds for the rectangle to pass the screen
speed = 2
# Square size
size = 300
#############################

# STEP 1. setup experiment
chosen_fps = FPS * n_iterations
np.random.shuffle(chosen_fps)

max_fps = max(FPS)
video = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), max_fps, (width, height))

# STEP 2. create video and display rules
frame = create_frame()
draw_text(frame, text="For each video, guess the number of FPS", position=(width//2, height//2 - 40), size=2, anchor=ANCHOR_BOTTOM_CENTER)
draw_text(frame, text="The possible options are: " + str(FPS), position=(width//2, height//2 + 40), size=2, anchor=ANCHOR_TOP_CENTER)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # Convert color space
for _ in range(2 * max_fps): # Lasts 2 seconds
    video.write(frame)

# STEP 3. draw
frames = np.zeros((speed * max_fps, height, width, 3), dtype=np.uint8)
y = height // 2
x = -size//2
dx = (width + size) // len(frames)
for i in range(len(frames)):
    frames[i] = create_frame()
    draw_square(frames[i], position=(x + i*dx, y), size=size)

for i in range(len(chosen_fps)):
    frame = create_frame()
    draw_text(frame, text=str(i), position=(width//2, height//2), size=2, anchor=ANCHOR_CENTER)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # Convert color space
    for j in range(max_fps): # lasts 1 second
        video.write(frame)

    duppl = max_fps//chosen_fps[i]
    for j in range(0, len(frames), duppl):
        f = np.copy(frames[j])
        draw_text(f, text=str(i), position=(100, 100), size=2, anchor=ANCHOR_TOP_LEFT)
        f = cv2.cvtColor(f, cv2.COLOR_RGB2BGR) # Convert color space
        for k in range(duppl):
            video.write(f)


# STEP 4. results
frame = create_frame()
draw_text(frame, text="The results are the following:", position=(width//2, height//2 - 40), size=2, anchor=ANCHOR_BOTTOM_CENTER)
draw_text(frame, text=str(chosen_fps), position=(width//2, height//2 + 40), size=2, anchor=ANCHOR_TOP_CENTER)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # Convert color space
for _ in range(5 * max_fps): # Lasts 5 seconds
    video.write(frame)

# Close video
video.release()
