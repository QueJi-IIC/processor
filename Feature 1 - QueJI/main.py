from ultralytics import YOLO
model = YOLO("yolov9c.pt")
model.export(format="openvino")
ov_model = YOLO("yolov9c_openvino_model/")

