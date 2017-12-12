import cv2
import numpy as np

# This is a brute-force module for creating a 3D analgyph video from a single video clip
# This module uses an alternating frames approach where the frames of the video alternate between a red channel extraction and a blue/green channel extraction

def get_alt_frames(filename, max_frames):
    cap = cv2.VideoCapture(filename)
    print("video capped...")

    frame_num = 0
    print("getting frames...")
    while frame_num < max_frames:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # save the resulting frame based on frame_num
        if frame_num % 2 == 0:
            get_red_channel(frame, frame_num, filename)
        else:
            get_blue_channel(frame, frame_num, filename)

        frame_num += 1

    print("done getting frames...")
    cap.release()
    cv2.destroyAllWindows()


def get_red_channel(frame, num, filename):
    # frame dimensions
    frame_h = frame.shape[0]
    frame_w = frame.shape[1]

    # empty image array
    red_copy = np.zeros((frame_h, frame_w, 3), np.uint8)
    for i in range(frame_h):
        for j in range(frame_w):
            red_copy[i, j, 2] = frame[i, j, 2]

    cv2.imwrite("{0}_alt/frame_{1}.jpg".format(filename, num), red_copy)


def get_blue_channel(frame, num, filename):
    # frame dimensions
    frame_h = frame.shape[0]
    frame_w = frame.shape[1]

    # empty image array
    blue_copy = np.zeros((frame_h, frame_w, 3), np.uint8)
    for i in range(frame_h):
        for j in range(frame_w):
            blue_copy[i, j, 0] = frame[i, j, 0]
            blue_copy[i, j, 1] = frame[i, j, 1]

    cv2.imwrite("{0}_alt/frame_{1}.jpg".format(filename, num), blue_copy)


def run_alt_frames(h, w, l, fps, n, e):
    height = h
    width = w
    vid_len = l
    frames_per_sec = fps
    max_frames = vid_len * frames_per_sec
    name = n
    ext = e

    get_alt_frames("{0}.{1}".format(name, ext), max_frames)    # get alternating frames

    video = cv2.VideoWriter('alt_{0}.avi'.format(name), cv2.VideoWriter_fourcc(*"MJPG"), frames_per_sec,
                            (width, height))

    for i in range(max_frames):     # loop through frames writing video
        print("writing frame {0}".format(i))
        frame = cv2.imread("{0}_alt/frame_{1}.jpg".format(name, i))
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()
    cv2.waitKey(0)

