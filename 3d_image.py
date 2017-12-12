import cv2
import numpy as np

# This is a brute-force module for creating a 3D anaglyph from a pair of images
# The input images can be a proper stereo pair or a single image 

def overlap(im1, im2, s):
    # image dimensions
    width1 = im1.shape[1]
    height1 = im1.shape[0]
    width2 = im2.shape[1]
    height2 = im2.shape[0]

    # final image
    composite = np.zeros((height2, width2+s, 3), np.uint8)

    # iterate through "left" image, filling in red values of final image
    for i in range(height1):
        for j in range(width1):
            try:
                composite[i, j, 2] = im1[i, j, 2]
            except IndexError:
                pass

    # iterate through "right" image, filling in blue/green values of final image
    for i in range(height2):
        for j in range(width2):
            try:
                composite[i, j+s, 1] = im2[i, j, 1]
                composite[i, j+s, 0] = im2[i, j, 0]
            except IndexError:
                pass
    return composite

def run_anaglyph(n1, e1, n2, e2, s):
    imageL = cv2.imread(n1 + e1)    # file name and extension for "left" image
    imageR = cv2.imread(n2 + e2)    # file name and extension for "right" image
    shift = s

    anaglyph = overlap(imageL, imageR, shift)

    cv2.imshow("anaglyph", anaglyph)
    cv2.imwrite(im_name + "_anaglyph.jpg", anaglyph)
    cv2.waitKey()
