import numpy as np
import cv2 as cv

hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

cv.startWindowThread()

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv.resize(frame, (800, 600))

    # using a greyscale picture, also for faster detection
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    boxes, weights = hog.detectMultiScale(frame, winStride=(4, 4))
    #
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    #
    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()

cv.destroyAllWindows()
cv.waitKey(1)
