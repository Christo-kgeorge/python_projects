import cv2
import pytesseract
from pytesseract import Output

# for windows we need to insatll pytesseract from google and must use a line of code in terminal

img = cv2.imread('/home/ckg/Documents/dl_luminar/python_projects/ocr/Untitled.png')
text = pytesseract.image_to_string(img)
data = pytesseract.image_to_data(img,output_type=Output.DICT)

print(data['text'])
print(data['left'])
# print(data.keys())

n_boxes = len(data['text'])
print(n_boxes)

for i in range(n_boxes):
    if data['conf'][i]>80:
        x,y,w,h = data['left'][i],data['top'][i],data['width'][i],data['height'][i]
        print(x,y,w,h)
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(0,255,0),thickness=3)


cv2.imshow('ocr',img)
cv2.waitKey()
cv2.destroyAllWindows()
