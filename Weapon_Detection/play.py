import cv2
from Weapon_Detection.main import ov_model
from Weapon_Detection.classes import classesNames
import torch

# Check if CUDA is available and set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
ov_model.to(device)

video_path = "in-y2mate.com - 13 Hours The Secret Soldiers of Benghazi 2016  Welcome to Benghazi Scene 110  Movieclips_720pFH.mp4"
cap = cv2.VideoCapture(video_path)
cap.set(3, 1100)
cap.set(4, 1100)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

output_path = "output_with_sos.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to tensor and move to CUDA
    frame_tensor = torch.from_numpy(frame).to(device)

    # Predict using the YOLO model
    results = ov_model(frame_tensor)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == classesNames.index("weapon"):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "SOS", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Write the frame to the output video file
    out.write(frame)

cap.release()
out.release()