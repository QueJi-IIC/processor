from ultralytics import YOLO
model = YOLO("../parking_navigation/best.pt")
model.export(format="openvino")
ov_model = YOLO("../parking_navigation/best_openvino_model/")

class_names = ov_model.names
print("Classes in the model:", class_names)