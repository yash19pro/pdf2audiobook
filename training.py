from google_drive_downloader import GoogleDriveDownloader as gdd
import re

drive_link = input("Enter drive link for The Hindu Newspaper pdf: ").strip()
file_id = re.split(r'/', drive_link)
gdd.download_file_from_google_drive(file_id=file_id[5], dest_path='./data/mnist.pdf', showsize=True)
