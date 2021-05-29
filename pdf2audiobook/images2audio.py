# importing the necessary libraries
import pytesseract
import threading
import cv2
import pyttsx3
import os
import re
import time
import ast

# text = str()

# def next_img(name):
#     global text
#     print("Thread execution started")
#     time.sleep(5)
#     img = cv2.imread(name)
#     # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
#     text = pytesseract.image_to_string(img)
#     text = re.sub(r"\b\n", " ", text)
#     text = re.sub(r"\n\b", " ", text)
#     text = re.sub(r"-\s", "", text)
#     print(text)
#     print("Thread execution ended")


class Image2audio:
    def __init__(self, name, chapter_name, speechrate, start, end):
        self.speechrate = speechrate
        self.text = str()
        self.start = start
        self.end = end
        self.pdfpath = os.path.dirname(__file__)
        self.pdfname = name
        self.chapter_name = chapter_name
        os.makedirs("{}/media/audiobook_books/{}/audio/{}".format(self.pdfpath, self.pdfname, self.chapter_name), exist_ok=True)

        # Initializing TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.speechrate)

    def next_img(self, name):
        self.text
        print("Thread execution started")
        time.sleep(5)
        img = cv2.imread(name)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
        self.text = pytesseract.image_to_string(img)
        self.text = re.sub(r"\b\n", " ", self.text)
        self.text = re.sub(r"\n\b", " ", self.text)
        self.text = re.sub(r"-\s", "", self.text)
        print(self.text)
        print("Thread execution ended")

    
    def converter(self):
        # global self.text
        img = cv2.imread("{}/media/audiobook_books/{}/images/{}/page{}.jpg".format(self.pdfpath, self.pdfname, self.chapter_name, 0))
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
        self.text = pytesseract.image_to_string(img)
        self.text = re.sub(r"\b\n", " ", self.text)
        self.text = re.sub(r"\n\b", " ", self.text)
        self.text = re.sub(r"-\s", "", self.text)
        print(self.text)

        # scanning the images and extracting the self.text from the image
        for i in range(self.start, self.end+1):
            if i < self.end:
                b = "{}/media/audiobook_books/{}/images/{}/page{}.jpg".format(self.pdfpath, self.pdfname, self.chapter_name, str(i + 1 - self.start))
                t = threading.Thread(target=self.next_img, args=(b,))
                print(b)
                t.start()
            self.engine.say("page " + str(i - self.start) + ' started!')
            self.engine.runAndWait()
            # self.engine.say(self.text)
            self.engine.save_to_file(self.text, "{}/media/audiobook_books/{}/audio/{}/page{}.mp3".format(self.pdfpath, self.pdfname, self.chapter_name, i - self.start))
            self.engine.runAndWait()
            print('page ' + str(i - self.start) + ' done')
            if i < self.end:
                t.join()


# name_of_pdf = input("Enter the name of PDF to be processed: ").strip()
# f = open('{}/pdf2audiobook/media/audiobook_books/{}/Index.txt'.format(os.path.dirname(__file__), name_of_pdf))
# makemyindex = f.read()
# makemyindex = ast.literal_eval(makemyindex)

# index_keys = list(makemyindex.keys())
# index_values = list(makemyindex.values())
# for x in range(len(index_values)):
#     a = Image2audio(name_of_pdf, index_keys[x], 500, index_values[x][0], index_values[x][1])
#     a.converter()
