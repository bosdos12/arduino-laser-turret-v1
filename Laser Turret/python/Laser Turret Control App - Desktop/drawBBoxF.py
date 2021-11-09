import cv2 as cv

RED   = (255, 0, 0)
GREEN = (0, 255, 0)

def drawBBoxF(img, bbox, bboxVisible):
    if (bboxVisible):
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv.rectangle(img, (x, y), ((x+w), (y+h)), GREEN, 3, 1)
    else:
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv.rectangle(img, (x, y), ((x+w), (y+h)), RED, 3, 1)