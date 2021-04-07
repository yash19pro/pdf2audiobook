# importing the necessary libraries
import pytesseract
import threading
import cv2
import pyttsx3
import os
import re
import time

text = str()


def next_img(name):
    global text
    print("Thread execution started")
    time.sleep(5)
    img = cv2.imread(name)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(img)
    text = re.sub(r"\b\n", " ", text)
    text = re.sub(r"\n\b", " ", text)
    text = re.sub(r"-\s", "", text)
    print(text)
    print("Thread execution ended")


class Image2audio:
    def __init__(self, name, speechrate, start, end):
        self.speechrate = speechrate
        self.text = str()
        self.start = start
        self.end = end
        self.pdfpath = os.path.dirname(__file__)
        self.pdfname = name

        # Initializing TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.speechrate)

    def converter(self):
        global text
        img = cv2.imread("{}/pdf2audiobook/media/{}/page{}.jpg".format(self.pdfpath, self.pdfname, 0))
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(img)
        text = re.sub(r"\b\n", " ", text)
        text = re.sub(r"\n\b", " ", text)
        text = re.sub(r"-\s", "", text)
        print(text)

        # scanning the images and extracting the text from the image
        for i in range(self.start, self.end+1):
            b = "{}/pdf2audiobook/media/{}/page{}.jpg".format(self.pdfpath, self.pdfname, str(i + 1 - self.start))
            t = threading.Thread(target=next_img, args=(b,))
            print(b)
            t.start()
            self.engine.say("page " + str(i - self.start) + ' started!')
            self.engine.runAndWait()
            self.engine.say(text)
            self.engine.runAndWait()
            print('page ' + str(i - self.start) + ' done')
            try:
                t.join()
            except:
                print("Thread doesn't exist")

a = Image2audio("IAG", 500, 0, 1)
a.converter()