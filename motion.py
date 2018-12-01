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

_, frame1 = cap.read()
_, frame2 = cap.read()

reference_frame = frame1

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

    for c in contours:
        if cv2.contourArea(c) < 10000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # calculate standard deviation
    _, stDev = cv2.meanStdDev(mod)

    if stDev > sdThresh:
        # print("Found you, bitch!");
        pass

    cv2.imshow('frame', frame2)
    cv2.imshow('dilated', dilated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()