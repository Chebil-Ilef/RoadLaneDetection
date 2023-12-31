import cv2
import numpy as np
from matplotlib import pyplot as plt

# defining Region of Interest (ROI) 
def roi(image, vertices):
    mask = np.zeros_like(image)
    mask_color = 255
    cv2.fillPoly(mask, vertices, mask_color)
    cropped_img = cv2.bitwise_and(image, mask)
    return cropped_img


def draw_lines(image, hough_lines):
    for line in hough_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


# lane detection in image
def process(img):
    height = img.shape[0]
    width = img.shape[1]
    roi_vertices = [
        (0, 650),
        (2*width/3, 2*height/3),
        (width, 1000)
    ]

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.dilate(gray_img, kernel=np.ones((3, 3), np.uint8))

    canny = cv2.Canny(gray_img, 130, 220)

    roi_img = roi(canny, np.array([roi_vertices], np.int32))

    lines = cv2.HoughLinesP(roi_img, 1, np.pi / 180, threshold=10, minLineLength=15, maxLineGap=2)

    final_img = draw_lines(img, lines)

    return final_img

# read video
cap = cv2.VideoCapture("Data/lane_vid_test.mp4")

# get frame hieght and width
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Xvid codec : XVID
# define fourCharCode for the output video
fourCharCode = cv2.VideoWriter_fourcc(*"XVID") 
saved_frame = cv2.VideoWriter("lane_detection_video.avi", fourCharCode, 30.0, (frame_width, frame_height))

# loop through the video which is a sequence of images
while cap.isOpened():
    # get the next frame
    ret, frame = cap.read()

    try:
        # detect road lanes in the frame
        frame = process(frame)

        # save the frame and show it in the result video and window
        saved_frame.write(frame)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    except Exception:
        break

cap.release()
saved_frame.release()
cv2.destroyAllWindows()

