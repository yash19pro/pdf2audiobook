from pdf2image import convert_from_path
import cv2
import pytesseract
import pyttsx3              # Default rate of reading is 200 word per minute
import os
import shutil
import re


# Access tesseract OCR by providing its location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# above line should be commented/uncommented depending on OS

# To create a proper path for creation of temporary directory named 'imgs' which gets deleted later
path = "imgs"

# Start pyttsx3 engine with rate of 185wpm.
engine = pyttsx3.init()
engine.setProperty('rate', 185)


# Fetch PDF
pdfname = str(input("Enter name of PDF: "))
padfpath = "{}.pdf".format(pdfname)


# Convert PDF pages to images
# next line should be commented on MacOS and uncommented on Windows
# pages = convert_from_path(poppler_path="C:\\poppler-21.02.0\\Library\\bin", pdf_path=padfpath, dpi=300, fmt="jpeg", grayscale=True, size=(2921, 3449))
# next line should be commented on Windows and uncommented on MacOS
pages = convert_from_path('IAG.pdf')

# Create imgs folder at specified path if it doesn't exist. If it exists, then delete it and create once again
try:
    os.mkdir(path)
except FileExistsError:
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)


# Text is used to find whether the page has editorials or not
text = str()
print("Number of pages: ", len(pages))


# Saves the images in jpeg format
for i in range(len(pages)):
    imgname = "imgs/{}{}.jpeg".format(pdfname, i)
    pages[i].save(imgname, 'JPEG')


# Reads upper left corner of each page.
title = str()
for i in range(len(pages)):
    img = cv2.imread("imgs\\{}{}.jpeg".format(pdfname, i))
    img_title = img[80:140, 180:650]

    # Converts image to grey scale and then thresholds it.
    img_grey = cv2.cvtColor(img_title, cv2.COLOR_BGR2GRAY)
    ret, img_threshold = cv2.threshold(img_grey, 170, 255, cv2.THRESH_BINARY)

    # Converts title image to string
    text = pytesseract.image_to_string(img_threshold)
    try:
        # Gets title if multiple words are there
        title = text.split()[0]
    except IndexError:
        pass

    if title == "EDITORIAL":

        # Processes left column editorial
        img_edi1 = img[361: 3393, 81: 777]
        img_edi1 = cv2.resize(src=img_edi1, dsize=(400, 2000), fx=10, fy=0.01)
        ret, img_threshold = cv2.threshold(img_edi1, 170, 255, cv2.THRESH_BINARY)
        edi1 = pytesseract.image_to_string(img_threshold)

        # Removes unwanted newline characters so that speech quality can be improved
        edi1 = re.sub(r"\b\n", " ", edi1)
        edi1 = re.sub(r"\n\b", " ", edi1)
        edi1 = re.sub(r"-\s", "", edi1)

        print(edi1)
        engine.save_to_file("Edi1.mp3", edi1)
        engine.runAndWait()

        # Finds the point from where the lower right editorial starts
        img_temp = img[800:, 800:2850]
        data = pytesseract.image_to_data(img_temp)
        imgHeight, imgWidth, _ = img_temp.shape
        cut_at = 0
        tops = []
        for num, specs in enumerate(data.splitlines()):
            specs_list = specs.split()
            if num != 0:
                if len(specs_list) == 12:
                    word = specs_list[11]
                    x, y, w, h = int(specs_list[6]), int(specs_list[7]), int(specs_list[8]), int(specs_list[9])
                    if h >= 40:
                        tops.append(y)
        cut_at = min(tops) + 800
        print("\nThis is cut point: ", cut_at)
        img_edi2 = cv2.resize(src=img[200:cut_at - 2, 800:2850], dsize=(1500, 1000), fx=0.4, fy=0.1)
        cv2.imshow('Edi_2', img_edi2)
        cv2.waitKey(0)
        img_edi3 = cv2.resize(src=img[cut_at:2825, 800:2850], dsize=(1500, 1000), fx=0.4, fy=0.1)
        cv2.imshow("Edi_3", img_edi3)
        cv2.waitKey(0)

        # Finds the end of picture in upper right editorial and covers it with black colour so that if any text is there, it will not interfere with actual editorial.
        img_temp = img_edi2[300:, 623:900]
        edi_data = pytesseract.image_to_data(img_temp)
        imgHeight, imgWidth, _ = img_temp.shape
        edi2_cut_at = 0
        tops = []
        for num, specs in enumerate(edi_data.splitlines()):
            specs_list = specs.split()
            if num != 0:
                if len(specs_list) == 12:
                    word = specs_list[11]
                    x, y, w, h = int(specs_list[6]), int(specs_list[7]), int(specs_list[8]), int(specs_list[9])
                    if h <= 20:
                        tops.append(y)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255))
        edi2_cut_at = min(tops) + 300
        print("\nThis is cut point for Editorial 2: ", edi2_cut_at)
        img_edi2[93:edi2_cut_at, 610:900] = [0, 0, 0]

        edi2 = pytesseract.image_to_string(img_edi2)

        # Removes unwanted newline characters so that speech quality can be improved
        edi2 = re.sub(r"\b\n", " ", edi2)
        edi2 = re.sub(r"\n\b", " ", edi2)
        edi2 = re.sub(r"-\s", "", edi2)

        cv2.imwrite('edi2.jpeg', img_edi2)
        cv2.waitKey(0)
        os.system('start edi2.jpeg')
        engine.save_to_file("Edi2.mp3", edi2)
        engine.runAndWait()

        # Finds the end of picture in lower right editorial and covers it with black colour
        img_temp = img_edi3[300:, 623:900]
        edi_data = pytesseract.image_to_data(img_temp)
        imgHeight, imgWidth, _ = img_temp.shape
        edi3_cut_at = 0
        tops = []
        for num, specs in enumerate(edi_data.splitlines()):
            specs_list = specs.split()
            if num != 0:
                if len(specs_list) == 12:
                    word = specs_list[11]
                    x, y, w, h = int(specs_list[6]), int(specs_list[7]), int(specs_list[8]), int(specs_list[9])
                    if h <= 20:
                        tops.append(y)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255))
        edi3_cut_at = min(tops) + 300
        print("\nThis is cut point for Editorial 3: ", edi3_cut_at)
        img_edi3[113:edi3_cut_at, 610:900] = [0, 0, 0]

        edi3 = str(pytesseract.image_to_string(img_edi3))

        # Removes unwanted newline characters so that speech quality can be improved
        edi3 = re.sub(r"\b\n", " ", edi3)
        edi3 = re.sub(r"\n\b", " ", edi3)
        edi3 = re.sub(r"-\s", "", edi3)

        cv2.imwrite('edi3.jpeg', img_edi3)
        cv2.waitKey(0)
        os.system('start edi3.jpeg')
        engine.save_to_file("Edi3.mp3", edi3)
        engine.runAndWait()


shutil.rmtree(path, ignore_errors=True)
