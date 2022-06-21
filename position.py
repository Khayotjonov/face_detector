import datetime
from ctypes import windll, Structure, c_long, byref
import time

# from Detector import main_app
from Detector import main_app

dt_time = time.time()
print("сейчас")


class POINTT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePositionn():
    pt = POINTT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


pos1 = queryMousePositionn()
print(pos1)


def getting_info_ever_schedule(dt_time):
    pos1 = queryMousePositionn()
    while True:

        if time.time() - dt_time > 5 and time.time() - dt_time <= 9:
            print('через ' + str(round(time.time() - dt_time)) + " секунд")

            x = get_position(pos1)
            if x is True:
                return True
            else:
                return False


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


def get_position(pos1):
    pos = queryMousePosition()
    if pos1 != pos:
        return True
    else:
        return False


def looping_func(obj):
    while True:
        dt_time = time.time()
        x = getting_info_ever_schedule(dt_time)
        print(x, "ETO X")
        if x is True:
            pass
        else:
            return main_app(obj)

