import ctypes

import cv2
import time
from PIL import Image
from tkinter import *
from tkinter import messagebox as mb

import position


def main_app(name):
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"./data/classifiers/{name}_classifier.xml")
    cap = cv2.VideoCapture(0)
    pred = 0
    dt_time = time.time()
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            for i in range(0, 5):
                if time.time() - dt_time > 5 and time.time() - dt_time <= 9:
                    mb.showwarning(title='Внимание блокировка компьютера', message='Блокировка через '+str(round(10 - (time.time() - dt_time)))+' секунд')
                elif time.time() - dt_time >= 10:
                    print("THIS CODE FOR BLOCK")
                    ctypes.windll.user32.LockWorkStation()
                print(round(10 - (time.time() - dt_time)), "this is blue")

        for (x, y, w, h) in faces:  
            roi_gray = gray[y:y + h, x:x + w]

            id, confidence = recognizer.predict(roi_gray)
            confidence = 100 - int(confidence)
            pred = 0

            if confidence > 50:
                dt_time = time.time()
                pred += +1
                text = name.upper()
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                position.looping_func(name)

            else:
                for i in range(0, 5):
                    if time.time() - dt_time > 5 and time.time() - dt_time <= 9:
                        mb.showwarning(title='Внимание блокировка компьютера', message='Блокировка через ' + str(
                            round(10 - (time.time() - dt_time))) + ' секунд')
                    elif time.time() - dt_time >= 10:
                        print("THIS CODE FOR BLOCK")
                        ctypes.windll.user32.LockWorkStation()
                # if time.time() - dt_time > 10:
                #     print("THIS CODE FOR BLOCK")
                #     # appgui.MainUI.show_frame(appgui.MainUI, "Block")
                #     ctypes.windll.user32.LockWorkStation()

                pred += -1
                text = "UnknownFace"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                print(round(10 - (time.time() - dt_time)), "seconds remaining for block user")


        cv2.imshow("image", frame)

        if cv2.waitKey(20) & 0xFF == 17:
            print(pred)

            if pred > 0:
                dim = (124, 124)
                img = cv2.imread(f".\\data\\{name}\\{pred}{name}.jpg", cv2.IMREAD_UNCHANGED)
                resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                cv2.imwrite(f".\\data\\{name}\\50{name}.jpg", resized)
                Image1 = Image.open(f".\\2.png")

                Image1copy = Image1.copy()
                Image2 = Image.open(f".\\data\\{name}\\50{name}.jpg")
                Image2copy = Image2.copy()

                Image1copy.paste(Image2copy, (195, 114))

                Image1copy.save("end.png")
                frame = cv2.imread("end.png", 1)

                cv2.imshow("Result", frame)
                cv2.waitKey(5000)
            break

    cap.release()
    cv2.destroyAllWindows()

