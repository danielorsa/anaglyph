import cv2
import numpy as np

# This is a brute-force module for creating a 3D anaglyph video from a single video clip
# This module uses an overlay approach in which an anaglyph image is created from each frame

def get_frames(video_file, max_frames, filename):
    cap = cv2.VideoCapture(video_file)
    print("video capped...")

    print("getting frames...")
    frame_num = 0
    while frame_num < max_frames:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # save the resulting frame
        cv2.imwrite("{0}_frames/frame_{1}.jpg".format(filename, frame_num), frame)

        frame_num += 1

    print("done getting frames...")
    cap.release()
    cv2.destroyAllWindows()


def save_colored_copies(filename, max_frames, h, w, shift):
    frame_h = h
    frame_w = w
    frame_num = 0
    while frame_num < max_frames:
        # read all frames
        frame = cv2.imread("{0}_frames/frame_{1}.jpg".format(filename, frame_num))

        # empty image arrays
        anaglyph_copy = np.zeros((frame_h, frame_w+shift, 3), np.uint8)

        # store color channels in respective arrays
        for i in range(frame_h):
            for j in range(frame_w):
                # red channel
                anaglyph_copy[i, j, 2] = frame[i, j, 2]
                # blue/green channel
                anaglyph_copy[i, j+shift, 0] = frame[i, j, 0]
                anaglyph_copy[i, j+shift, 1] = frame[i, j, 1]

        # save images
        cv2.imwrite("{0}_anaglyph/ana_frame{1}.jpg".format(filename, frame_num), anaglyph_copy)

        frame_num += 1


def run_overlay(h, w, l, fps, n, e, s):
    height = h
    width = w
    vid_len = l
    frames_per_sec = fps
    max_frames = vid_len * frames_per_sec
    name = n
    ext = e
    shift = s

    get_frames("{0}.{1}".format(name, ext), max_frames, name)            # get frames
    save_colored_copies(name, max_frames, height, width, shift)     # save color extractions of frames

    video = cv2.VideoWriter('over_{0}_{1}.avi'.format(name, str(shift)), cv2.VideoWriter_fourcc(*"MJPG"),
                            frames_per_sec,
                            (width + shift, height))

    for i in range(max_frames):                # loop through frames writing to video
        frame = cv2.imread("{0}_anaglyph/ana_frame{1}.jpg".format(name, i))
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()
    cv2.waitKey(0)

