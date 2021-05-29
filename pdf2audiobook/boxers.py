import cv2
import pytesseract

# reading the image
img = cv2.imread('lol.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# x, y => (coordinates of first corner) and w, h => (coordinates of the 4th corner)
yash = pytesseract.image_to_boxes(img)

# detecting characters and printing the boxes around them
imgHeight, imgWidth, _ = img.shape
for xx in yash.splitlines():
    yolo = xx.split(' ')
    # print(yolo)
    x, y, w, h = int(yolo[1]), int(yolo[2]), int(yolo[3]), int(yolo[4])
    cv2.rectangle(img, (x, imgHeight - y), (w, imgHeight - h), (0, 0, 255))

# detecting the words and printing the boxes around them
patel = pytesseract.image_to_data(img)
imgHeight, imgWidth, _ = img.shape
for qoo, xx in enumerate(patel.splitlines()):
    yolo = xx.split()
    if qoo != 0:
        if len(yolo) == 12:
            word = yolo[11]
            x, y, w, h = int(yolo[6]), int(yolo[7]), int(yolo[8]), int(yolo[9])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255))
            cv2.putText(img, word, (x, y), cv2.FONT_HERSHEY_COMPLEX,
                        0.50, (0, 0, 255), 1)

cv2.imshow('res', img)
cv2.waitKey(0)
