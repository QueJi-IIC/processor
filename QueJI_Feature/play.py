import QueJI_Feature.main as main
import QueJI_Feature.classes as classes
import QueJI_Feature.cvo as cvo

shop_chosen = 'Person'
shop_capacity = 15

def set_object_index(shop_type):
    if shop_type == 'Person':
        return 0
    elif shop_type == 'Car':
        return 2

def Camera(shop_type):
    while True:
        global img
        success, img = cvo.cap.read()
        results = main.ov_model(img, stream=True)

        for r in results:
            boxes = r.boxes
            global i
            i = 0

            for box in boxes:
                cls = int(box.cls[0])

                if cls == set_object_index(shop_type):
                    i += 1
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    cvo.cv2.rectangle(img, (x1, y1), (x2, y2), (158, 255, 249), 3)

                    org = [x1, y1]
                    font = cvo.cv2.FONT_HERSHEY_COMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cvo.cv2.putText(img, classes.classNames[cls], org, font, fontScale, color, thickness)
                    return i

        return False

def availability(object, capacity):
    availabilty = capacity - (object + 10)
    return availabilty

def integrate():
    while True:
        x = Camera(shop_chosen)
        if x is False:
            return False
        y = availability(x, shop_capacity)
        return y

def boolx():
    while True:
        z = integrate()
        if z is False or z <= 2:
            return False
        else:
            return True

def runner():
    cvo.start_Cam()

    while True:
        e = boolx()
        print(e)
        print("Number of person: ", i)
        cvo.cv2.imshow('Webcam', img)
        if cvo.cv2.waitKey(1) == ord(':'):
            break

    return

runner()