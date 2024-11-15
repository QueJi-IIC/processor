import cv2
cap = 0
def start_Cam():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(3, 1100)
    cap.set(4, 1100)
