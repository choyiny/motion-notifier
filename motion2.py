import numpy as np
import cv2
import time

sdThresh = 10
font = cv2.FONT_HERSHEY_SIMPLEX


def dist_map(frame1, frame2):
    """ outputs pythagorean distance between two frames """
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = (np.sqrt(diff32[:, :, 0] ** 2 + diff32[:, :, 1] ** 2 + diff32[:, :, 2] ** 2)
              / np.sqrt(255 ** 2 + 255 ** 2 + 255 ** 2))
    dist = np.uint8(norm32 * 255)
    return dist


cv2.namedWindow('frame')
cv2.namedWindow('dilated')

# capture video stream from camera source.
# 0 refers to first camera, 1 referes to 2nd and so on.
cap = cv2.VideoCapture(0)

# read the first two frames
_, frame1 = cap.read()
_, frame2 = cap.read()

# set the reference frame as the first frame
reference_frame = frame1

# store contours in last frame
last_contours = set()

# reset reference frame every 30 ticks
ticks = 0

while True:
    _, frame3 = cap.read()
    rows, cols, _ = np.shape(frame3)
    dist = dist_map(reference_frame, frame3)

    frame1 = frame2
    frame2 = frame3

    # apply Gaussian smoothing
    mod = cv2.GaussianBlur(dist, (9, 9), 0)

    # apply threshold
    _, thresh = cv2.threshold(mod, 100, 255, 0)

    # dilate to fill in holes
    dilated = cv2.dilate(thresh, None, iterations=2)

    image, contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)

    # draw a rectangle over each contour
    # if the contour has been stationary for more than 5 seconds, reset the reference frame
    this_contours = set()
    for c in contours:
        if cv2.contourArea(c) > 10000:
            (x, y, w, h) = cv2.boundingRect(c)
            this_contours.add((x, y, w, h))
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # only keep the contours that are similar
    last_contours = last_contours.intersection(this_contours)

    # reset reference frame if needed
    if ticks > 50 and len(last_contours) > 0:
        reference_frame = frame1
        ticks = 0
    elif ticks > 100:
        ticks = 0

    # calculate standard deviation
    # _, stDev = cv2.meanStdDev(mod)
    #
    # if stDev > sdThresh:
    #     # print("Found you, bitch!");
    #     pass

    cv2.imshow('frame', frame2)
    cv2.imshow('dilated', dilated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    ticks += 1

cap.release()
cv2.destroyAllWindows()