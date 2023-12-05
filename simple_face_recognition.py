import cv2
import os, sys, glob, shutil, face_recognition
from threading import Thread, Lock
from progress.bar import IncrementalBar
import time

g_files_parsed = 0 
lock = Lock()

def find_and_save_images_contains_faces(images):
    for image_path in images:
        global g_files_parsed
        img = cv2.imread(image_path)
        if img is None:
            g_files_parsed += 1
            continue
        color_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        is_face = face_recognition.face_encodings(color_image, model="large")
        if len(is_face):
            temp = sys.argv[2] + str(image_path)[str(image_path).rfind("/"):]
            shutil.copyfile(image_path, temp)
        g_files_parsed += 1

if __name__ == "__main__":
    folder_name = sys.argv[1]
    files_in_folder = sorted(glob.glob(os.path.join(folder_name, '*.jpg')), reverse=True)
    x = []
    x.append(Thread(target=find_and_save_images_contains_faces, args=(files_in_folder,)))
    x[0].start()

    bar = IncrementalBar('Parsed files', max = len(files_in_folder))

    while g_files_parsed != len(files_in_folder):
        time.sleep(1)
        bar.index =g_files_parsed
        bar.update()

    x[0].join()




