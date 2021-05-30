from pdf2image import convert_from_path
import cv2
import pytesseract
import pyttsx3  # Default rate of reading is 200 word per minute
import os
import shutil
import re
# from google_drive_downloader import GoogleDriveDownloader as Gdd
import threading
import time


class Editorial2audiobook:
    def __init__(self, mode, drive_link, file_name):
        # Access tesseract OCR by providing its location
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # above line should be commented/uncommented depending on OS

        # To create a proper path for creation of temporary directory named 'imgs' which gets deleted later
        path = "imgs"

        # Start pyttsx3 engine with rate of 185wpm.
        engine = pyttsx3.init()
        engine.setProperty('rate', 185)

        # PDF input mode
        # Make necessary changes "HERE!!!" while integrating
        pdf_path = str()
        pdf_name = str()
        # mode = int(input("#####\tMENU\t#####\n1: Input using Google Drive link\n2: Upload PDF\nYour choice: "))
        if mode == 1:
            # drive_link = input("Enter drive link for The Hindu Newspaper pdf: ").strip()
            # file_name = input("Save as (*.pdf): ").strip()
            file_id = re.split(r'/', drive_link)
            # Gdd.download_file_from_google_drive(file_id=file_id[5], dest_path='./media/books/{}.pdf'.format(file_name), showsize=True)
            pdf_name = file_name
            pdf_path = './media/books/{}.pdf'.format(file_name)
        elif mode == 2:
            # pdf_name = str(input("Enter name of PDF: "))
            pdf_name = file_name
            pdf_path = "./media/books/{}.pdf".format(pdf_name)
        else:
            print("Invalid input!!!")
            exit(0)

        # Convert PDF pages to images
        # next line should be commented on MacOS and uncommented on Windows
        pages = convert_from_path(poppler_path="C:/poppler-21.02.0/Library/bin", pdf_path=pdf_path, dpi=300, fmt="jpeg", grayscale=True, size=(2921, 3449))
        # next line should be commented on Windows and uncommented on MacOS
        # pages = convert_from_path(pdf_path)

        # Create imgs folder at specified path if it doesn't exist. If it exists, then delete it and create once again
        try:
            os.makedirs("./{}".format(path), exist_ok=True)
            os.makedirs(
                "./media/audiobook_books/{}/audio".format(pdf_name), exist_ok=True)
            os.makedirs(
                "./media/audiobook_books/{}/images".format(pdf_name), exist_ok=True)
        except FileExistsError:
            # shutil.rmtree(path, ignore_errors=True)
            os.makedirs("./{}".format(path), exist_ok=True)
            os.makedirs(
                "./media/audiobook_books/{}/audio".format(pdf_name), exist_ok=True)
            os.makedirs(
                "./media/audiobook_books/{}/images".format(pdf_name), exist_ok=True)

        # Text is used to find whether the page has editorials or not
        # text = str()
        print("Number of pages: ", len(pages))

        editorial_audiobooks_path = "./media/audiobook_books/{}/audio".format(
            pdf_name)
        editorial_thumbnails_path = "./media/audiobook_books/{}/images".format(
            pdf_name)

        # Saves the images in jpeg format
        for i in range(len(pages)):
            imgname = "imgs/{}{}.jpeg".format(pdf_name, i)
            pages[i].save(imgname, 'JPEG')

        def left_column_editorial(img):
            # Processes left column editorial
            print("Column editorial processing started")
            img_edi1 = img[361: 3393, 81: 777]
            img_edi1 = cv2.resize(
                src=img_edi1, dsize=(400, 2000), fx=10, fy=0.01)
            ret, img_threshold = cv2.threshold(
                img_edi1, 170, 255, cv2.THRESH_BINARY)
            edi1 = pytesseract.image_to_string(img_threshold)

            # Removes unwanted newline characters so that speech quality can be improved
            edi1 = re.sub(r"\b\n", " ", edi1)
            edi1 = re.sub(r"\n\b", " ", edi1)
            edi1 = re.sub(r"-\s", "", edi1)

            os.makedirs("./media/audiobook_books/{}/audio/Chapter0".format(pdf_name), exist_ok=True)
            os.makedirs("./media/audiobook_books/{}/images/Chapter0".format(pdf_name), exist_ok=True)
            cv2.imwrite(
                '{}/Chapter0/page0.jpeg'.format(editorial_thumbnails_path), img_edi1)
            cv2.waitKey(0)
            engine.save_to_file(
                edi1, "{}/Chapter0/page0.mp3".format(editorial_audiobooks_path))
            engine.runAndWait()
            print("Column editorial processing done!!!")

        def upper_right_editorial(img_edi2):
            # Finds the end of picture in upper right editorial and covers it with black colour so that if any text is there, it will not interfere with actual editorial.
            print("Upper right editorial processing started")
            img_temp = img_edi2[300:, 623:900]
            edi_data = pytesseract.image_to_data(img_temp)
            imgHeight, imgWidth, _ = img_temp.shape
            tops = []
            for num, specs in enumerate(edi_data.splitlines()):
                specs_list = specs.split()
                if num != 0:
                    if len(specs_list) == 12:
                        x, y, w, h = int(specs_list[6]), int(specs_list[7]), int(
                            specs_list[8]), int(specs_list[9])
                        if h <= 20:
                            tops.append(y)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255))
            edi2_cut_at = min(tops) + 300
            img_edi2[93:edi2_cut_at, 610:900] = [0, 0, 0]

            edi2 = pytesseract.image_to_string(img_edi2)

            # Removes unwanted newline characters so that speech quality can be improved
            edi2 = re.sub(r"\b\n", " ", edi2)
            edi2 = re.sub(r"\n\b", " ", edi2)
            edi2 = re.sub(r"-\s", "", edi2)

            os.makedirs("./media/audiobook_books/{}/audio/Chapter1".format(pdf_name), exist_ok=True)
            os.makedirs("./media/audiobook_books/{}/images/Chapter1".format(pdf_name), exist_ok=True)
            cv2.imwrite(
                '{}/Chapter1/page0.jpeg'.format(editorial_thumbnails_path), img_edi2)
            cv2.waitKey(0)
            engine.save_to_file(
                edi2, "{}/Chapter1/page0.mp3".format(editorial_audiobooks_path))
            engine.runAndWait()
            print("Upper right editorial processing done!!!")

        def lower_right_editorial(img_edi3):
            # Finds the end of picture in lower right editorial and covers it with black colour
            print("Lower right editorial processing started")
            img_temp = img_edi3[300:, 623:900]
            edi_data = pytesseract.image_to_data(img_temp)
            imgHeight, imgWidth, _ = img_temp.shape
            tops = []
            for num, specs in enumerate(edi_data.splitlines()):
                specs_list = specs.split()
                if num != 0:
                    if len(specs_list) == 12:
                        x, y, w, h = int(specs_list[6]), int(specs_list[7]), int(
                            specs_list[8]), int(specs_list[9])
                        if h <= 20:
                            tops.append(y)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255))
            edi3_cut_at = min(tops) + 300
            img_edi3[113:edi3_cut_at, 610:900] = [0, 0, 0]

            edi3 = pytesseract.image_to_string(img_edi3)

            # Removes unwanted newline characters so that speech quality can be improved
            edi3 = re.sub(r"\b\n", " ", edi3)
            edi3 = re.sub(r"\n\b", " ", edi3)
            edi3 = re.sub(r"-\s", "", edi3)

            os.makedirs("./media/audiobook_books/{}/audio/Chapter2".format(pdf_name), exist_ok=True)
            os.makedirs("./media/audiobook_books/{}/images/Chapter2".format(pdf_name), exist_ok=True)
            cv2.imwrite(
                '{}/Chapter2/page0.jpeg'.format(editorial_thumbnails_path), img_edi3)
            cv2.waitKey(0)
            # os.system('start edi3.jpeg')
            engine.save_to_file(
                edi3, "{}/Chapter2/page0.mp3".format(editorial_audiobooks_path))
            engine.runAndWait()
            print("Lower right editorial processing done!!!")

        # Reads upper left corner of each page.
        title = str()
        flag = 0
        for i in range(len(pages)):
            img = cv2.imread("imgs/{}{}.jpeg".format(pdf_name, i))
            img_title = img[80:140, 180:650]

            # Converts image to grey scale and then thresholds it.
            img_grey = cv2.cvtColor(img_title, cv2.COLOR_BGR2GRAY)
            ret, img_threshold = cv2.threshold(
                img_grey, 170, 255, cv2.THRESH_BINARY)

            # Converts title image to string
            text = pytesseract.image_to_string(img_threshold)
            try:
                # Gets title if multiple words are there
                title = text.split()[0]
            except IndexError:
                pass

            if title == "EDITORIAL":

                flag = 1
                # Processing left column editorial using thread to achieve speed
                t1 = threading.Thread(
                    target=left_column_editorial, args=(img,))
                t1.start()

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
                            x, y, w, h = int(specs_list[6]), int(specs_list[7]), int(
                                specs_list[8]), int(specs_list[9])
                            if h >= 40:
                                tops.append(y)
                cut_at = min(tops) + 800
                img_edi2 = cv2.resize(
                    src=img[200:cut_at - 2, 800:2850], dsize=(1500, 1000), fx=0.4, fy=0.1)

                # Finds the point where the lower right editorial finishes
                img_temp = img[cut_at + 500:, 800:2850]
                data = pytesseract.image_to_data(img_temp)
                imgHeight, imgWidth, _ = img_temp.shape
                top = a = b = x = y = w = h = 0
                for num, specs in enumerate(data.splitlines()):
                    specs_list = specs.split()
                    if num != 0:
                        b = int(specs_list[6])
                        if len(specs_list) == 12:
                            word = specs_list[11]
                            x, y, w, h = int(specs_list[6]), int(specs_list[7]), int(
                                specs_list[8]), int(specs_list[9])
                            if b - a >= 1000:
                                top = y
                                break
                    a = b
                cut_at_lower = y + cut_at - 40
                img_edi3 = cv2.resize(
                    src=img[cut_at:cut_at_lower, 800:2850], dsize=(1500, 1000), fx=0.4, fy=0.1)

                t2 = threading.Thread(
                    target=upper_right_editorial, args=(img_edi2,))
                t2.start()

                time.sleep(5)

                t3 = threading.Thread(
                    target=lower_right_editorial, args=(img_edi3,))
                t3.start()

                t1.join()
                t2.join()
                t3.join()
                break

        if flag == 0:
            print("There is 'NO EDITORIAL' in this Newspaper")
        shutil.rmtree(path, ignore_errors=True)


# a = Editorial2audiobook(2, "https://drive.google.com/file/d/1mbBv1BQaWGr8qp7etr85r6B7imZ6KHLD/view?usp=sharing", "TH29May")
