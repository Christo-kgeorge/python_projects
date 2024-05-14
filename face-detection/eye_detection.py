import cv2

img=cv2.imread('/home/ckg/Documents/dl_luminar/python_projects/face-detection/iage.jpg')

eye_cascade= cv2.CascadeClassifier('/home/ckg/Documents/dl_luminar/python_projects/face-detection/haarcascade_eye.xml')

grey_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


eyes = eye_cascade.detectMultiScale(grey_img)

print(eyes)

for(x,y,w,h) in eyes:
    cv2.rectangle(img,pt1=(x,y),pt2=(x+w,y+h),color=(0,255,0),thickness=3)


cv2.imshow('eye detection',img)
cv2.waitKey(5000)
cv2.destroyAllWindows()