from ultralytics import YOLO
model = YOLO("../Weapon_Detection/best.pt")
model.export(format="openvino")
ov_model = YOLO("../Weapon_Detection/best_openvino_model/")

class_names = ov_model.names
print("Classes in the model:", class_names)