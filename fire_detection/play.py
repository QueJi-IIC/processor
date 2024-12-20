import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("../fire_detection/best.pt")
model.export(format="openvino")
ov_model = YOLO("../fire_detection/best_openvino_model/")
classesNames = ["fire"]

# Open the video file
video_path = "fire2.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object
output_path = "output_video2.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Ensure the correct class index for fire
fire_class_index = classesNames.index("fire")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Predict using the YOLO model
    results = ov_model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == fire_class_index:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "SOS PUSH", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Write the frame to the output video file
    out.write(frame)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()