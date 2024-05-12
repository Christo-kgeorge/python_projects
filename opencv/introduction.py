import cv2

img =cv2.imread('/home/ckg/Documents/dl_luminar/python_projects/opencv/f1.jpeg')

# resized_img =cv2.resize(img,(400,400))
# print(img.shape) #shape of the image(h,w,c) = c=rgb/bw 

#print(img)
# grey_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

# (thresh,bw_img) = cv2.threshold(grey_img,128,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

# print(thresh)
# cv2.imwrite('greImage.jpg',grey_img)
# cv2.imwrite('binaryimg.jpg',bw_img)

#rectangle
img=cv2.rectangle(img,pt1=(31,108),pt2=(239,158),color=(255,0,0),thickness= -1)

#Circle
img=cv2.circle(img,center=(207,133),radius=25,color=(0,255,0),thickness=-1)

#text
img=cv2.putText(
            img,
            text='Face',
            org=(52,146),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=1,
            color=(0,255,0),
            thickness=1)

cv2.imshow('rgb image',img)
cv2.waitKey(10000)
cv2.destroyAllWindows()