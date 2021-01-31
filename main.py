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

# STEP 1. setup experiment   ###################################################
chosen_fps = FPS * n_iterations
np.random.shuffle(chosen_fps)

max_fps = max(FPS)
video = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), max_fps, (width, height))

# STEP 2. create video and display rules   #####################################
print('Drawing rules ...', end='', flush=True)
frame = create_frame()
draw_text(frame, text="For each video, guess the number of FPS", position=(width//2, height//2 - 40), size=2, anchor=ANCHOR_BOTTOM_CENTER)
draw_text(frame, text="The possible options are: " + str(FPS) + " FPS", position=(width//2, height//2 + 40), size=2, anchor=ANCHOR_TOP_CENTER)
frame = smooth(frame)
for _ in range(2 * max_fps): # Lasts 2 seconds
    video.write(frame)
print(' done')

# STEP 3. draw   ###############################################################
print('Drawing challenge ... 0%', end='\r', flush=True)
frames = np.zeros((speed * max_fps, height, width, 3), dtype=np.uint8)
y = height // 2
x = -size//2
dx = (width + size) // len(frames)
for i in range(len(frames)):
    frames[i] = create_frame()
    draw_square(frames[i], position=(x + i*dx, y), size=size)
    print(f"Drawing challenge ... {round(100 * i / (len(frames) + len(chosen_fps)))}%", end='\r', flush=True)

for i in range(len(chosen_fps)):
    print(f"Drawing challenge ... {round(100 * (len(frames) + i) / (len(frames) + len(chosen_fps)))}%", end='\r', flush=True)
    frame = create_frame()
    draw_text(frame, text=str(i + 1), position=(width//2, height//2), size=2, anchor=ANCHOR_CENTER)
    frame = smooth(frame)
    for j in range(max_fps): # lasts 1 second
        video.write(frame)

    duppl = max_fps//chosen_fps[i]
    for j in range(0, len(frames), duppl):
        f = np.copy(frames[j])
        draw_text(f, text=str(i + 1), position=(100, 100), size=2, anchor=ANCHOR_TOP_LEFT)
        f = smooth(f)
        for k in range(duppl):
            video.write(f)
print(f"Drawing challenge ... done")


# STEP 4. results   ############################################################
print('Drawing results ...', end='', flush=True)
frame = create_frame()
draw_text(frame, text="The results are the following:", position=(width//2, height//2 - 40), size=2, anchor=ANCHOR_BOTTOM_CENTER)
draw_text(frame, text=str(chosen_fps), position=(width//2, height//2 + 40), size=2, anchor=ANCHOR_TOP_CENTER)
frame = smooth(frame)
for _ in range(5 * max_fps): # Lasts 5 seconds
    video.write(frame)
print('done')

# Close video
video.release()
