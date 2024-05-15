import cv2

# webcam index =0,1,-1,2,-1,
video =cv2.VideoCapture('/home/ckg/Documents/dl_luminar/python_projects/face-detection/VID-20240509-WA0000.mp4')
face_cascade = cv2.CascadeClassifier('/home/ckg/Documents/dl_luminar/python_projects/face-detection/haarcascade_frontalface_default.xml')
eye_cascade= cv2.CascadeClassifier('/home/ckg/Documents/dl_luminar/python_projects/face-detection/haarcascade_eye.xml')

#pass grey img to face_cascade

while True:
    success, frame =video.read()
    grey_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey_img)
    eyes = eye_cascade.detectMultiScale(grey_img)
    print(faces)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,pt1=(x,y),pt2=(x+w,y+h),color=(0,255,0),thickness=3)

    for(x,y,w,h) in eyes:
        cv2.rectangle(frame,pt1=(x,y),pt2=(x+w,y+h),color=(0,255,0),thickness=3)

    cv2.imshow('video reader',frame)
    if cv2.waitKey(1) & 0xFF==27:
        break
cv2.release()
cv2.destroyAllWindows()