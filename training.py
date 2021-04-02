import threading
import pytesseract
import cv2
import pyttsx3
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
engine = pyttsx3.init()
engine.setProperty('rate', 185)

text = str()

def next_img(name):
    global text
    print("Thread execution started")
    img = cv2.imread(name)
    # time.sleep(5)
    text = pytesseract.image_to_string(img)
    print("Thread execution ended")



_ = 2
img_name = "edi{}.jpeg".format(_)
img = cv2.imread(img_name)
text = pytesseract.image_to_string(img)
for i in range(2, 5):
    # img_name = "edi{}.jpeg".format(_)
    # img = cv2.imread(img_name)
    # text = pytesseract.image_to_string(img)
    try:
        t = threading.Thread(target=next_img, args=("edi{}.jpeg".format(_+1),))
        _ += 1
        t.start()
    except FileNotFoundError:
        print("i+1 error")
    engine.say(text)
    engine.runAndWait()
    try:
        t.join()
    except:
        print("t doesn't exist")
    if _ > 4:
        engine.say("Thank You!\nThis states that I am working perfectly fine as a parallel processing system.")
        engine.runAndWait()