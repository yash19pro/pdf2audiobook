# importing the necessary libraries
from pdf2image import convert_from_path
import pytesseract
import threading
import cv2
import pyttsx3
import os

# Creates a folder to store images
os.system('mkdir images')


# Fetch PDF
pdfname = str(input("Enter name of PDF: "))
pdfpath = "{}.pdf".format(pdfname)


# Convert PDF pages to images
# next line should be commented on MacOS and uncommented on Windows
# pages = convert_from_path(poppler_path="C:\\poppler-21.02.0\\Library\\bin", pdf_path=pdfpath, dpi=300, fmt="jpeg", grayscale=True, size=(2921, 3449))
# next line should be commented on Windows and uncommented on MacOS
pages = convert_from_path('IAG.pdf')

# Initializing TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 185)


# Getting the range to process
start, end = map(int, input("Enter the range of pages separated by '-': ").rstrip().split('-'))


# Saving image objects generated by poppler in jpg format
for i in range(start, end+1):
    pages[i].save('images/page{}.jpg'.format(i), 'JPEG')
    print('Page ' + str(i) + " done...")

print("Processing..!!")
os.system('mkdir sound')


# Thread function to get data of next page
text = str()
def next_img(name):
    global text
    print("Thread execution started")
    img = cv2.imread(name)
    # time.sleep(5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(img_threshold)
    print("Thread execution ended")


# scanning the images and extracting the text from the image
for i in range(start, end+1):
    img = cv2.imread('images/page{}.jpg'.format(i))
    try:
        t = threading.Thread(target=next_img, args=("images/page{}.jpg".format(i+1),))
        t.start()
    except FileNotFoundError:
        print("i+1 error")
    engine.say("page " + str(i) + ' started!')
    engine.runAndWait()
    engine.say(text)
    engine.runAndWait()
    print('page ' + str(i) + ' done')
    try:
        t.join()
    except:
        print("t doesn't exist")
