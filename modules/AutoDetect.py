from ultralytics import YOLO

class AutoDetect:
    def __init__(self, model='yolov8n.pt'):
        self.model = model

        self.auto_detect_enable = False
