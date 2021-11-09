import cv2 as cv
import time

cap = cv.VideoCapture(0)

tracker = cv.TrackerMOSSE_create()
success, findbboximg = cap.read()
bboxes = [
    {"bbox": cv.selectROI("1", findbboximg, False), "tracker": cv.TrackerMOSSE_create(), "name": "emoji"},
    {"bbox": cv.selectROI("2", findbboximg, False), "tracker": cv.TrackerMOSSE_create(), "name": "medal"}
]

# Initialising the bboxes;
for bboxArrayElementIndex in range(len(bboxes)):
    bboxes[bboxArrayElementIndex]["tracker"].init(findbboximg, bboxes[bboxArrayElementIndex]["bbox"])





def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 255), 3, 1)
    cv.putText(img, "Tracing", (75, 75), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

while True:
    timer = cv.getTickCount()
    success, img = cap.read()

    for bboxArrayElement in bboxes:

        success, bbox = bboxArrayElement["tracker"].update(img)


        print(bbox)

        if success:
            cv.putText(img, bboxArrayElement["name"], (int(bbox[0]), int(bbox[1]+(bbox[3]/2))), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            drawBox(img, bbox)
        else:
            cv.putText(img, "Lost: " + bboxArrayElement["name"], (75, 75), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        



    fps = cv.getTickFrequency()/(cv.getTickCount()-timer)


    cv.rectangle(img, (5, 5), (100, 100), (255, 0, 0), 5)

    cv.putText(img, str(int(fps)), (75, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv.imshow("Traaaaaaacking", img)

    if cv.waitKey(1) & 0xff == ord('q'):
        break







