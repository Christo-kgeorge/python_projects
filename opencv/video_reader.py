import cv2

# webcam index =0,1,-1,2,-1
video =cv2.VideoCapture(0)

while True:
    success, frame =video.read()
    frame=cv2.flip(frame,-1)
    print(success)

    cv2.imshow('video reader',frame)
    if cv2.waitKey(1) & 0xFF==27:
        break
video.release()
cv2.destroyAllWindows()