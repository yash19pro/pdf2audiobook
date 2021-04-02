# importing the necessary libraries
import pdf2image
import pytesseract
import PIL as Image
import cv2
import pyttsx3
import os

# converting the pdf to image
os.system('mkdir images')
pages = pdf2image.convert_from_path("a.pdf", 500)
cnt = 0
for page in pages:
    page.save('images/page' + str(cnt) + '.jpg', 'JPEG')
    cnt += 1
    print('Page ' + str(cnt - 1) + " done...")

numb = int(input("Enter the number of chapts: "))
lolo = []
for i in range(numb):
    print("Enter the range: ")
    no = list(map(int, input().split(' ')))
    lolo.append(no)

print("Processing..!!")
os.system('mkdir sound')

# scanning the images and extracting the text from the image
for x in range(numb):
    os.system('mkdir sound/chapter' + str(x + 1))
    for i in range(lolo[x][0] - 1, lolo[x][1]):
        text = str()
        img = cv2.imread('images/page' + str(i) + ".jpg")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(img_threshold)

        engine = pyttsx3.init()
        engine.say("page " + str(i) + ' started!')
        engine.save_to_file(text, 'sound/chapter' +
                            str(x + 1) + '/' + str(i) + '.mp3')
        engine.runAndWait()
        engine.stop()
        print('page ' + str(i) + ' done')
