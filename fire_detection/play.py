import cv2
from ultralytics import YOLO
model = YOLO("../fire_detection/best.pt")
classesNames = ["fire"]
# Load the image
image_path = "fire.jpg"
image = cv2.imread(image_path)
image = cv2.resize(image, (640, 480))  # Resize the image to 640x480

if image is None:
    print("Error: Could not open or find the image.")
    exit()

# Predict using the YOLO model
results = model(image)

# Ensure the correct class index for weapons
weapon_class_index = classesNames.index("fire")

for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        if cls == weapon_class_index:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, "SOS PUSH", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

# Display the image with detected weapons
cv2.imshow("Weapon Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()