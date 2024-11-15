from ultralytics import YOLO
model = YOLO("../fire_detection/best.pt")
model.export(format="openvino")
ov_model = YOLO("../fire_detection/best_openvino_model/")

class_names = ov_model.names
print("Classes in the model:", class_names)