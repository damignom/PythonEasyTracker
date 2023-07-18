import cv2
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QColor
from PyQt5.QtWidgets import QLabel
from cv2 import VideoCapture

from conf import settings


class ImgLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_capture = VideoCapture(0)  # Инициализация видеозахвата
        self.tracking_enabled = False  #лаг для отслеживания области
        self.tracker = None  # Трекер OpenCV
        self.selection_start = QPoint()  # Начальная точка выбора области
        self.selection_end = QPoint()  # Конечная точка выбора области

    def start_tracking(self):
        self.tracking_enabled = True
        self.tracker = cv2.TrackerKCF_create()  # Используйте нужный трекер OpenCV

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_start = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.selection_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_end = event.pos()
            self.tracking_enabled = True
            self.tracker = cv2.TrackerKCF_create()  # Используйте нужный трекер OpenCV
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        print(Qt.red)
        painter.drawRect(self.selection_start.x(), self.selection_start.y(),
                         self.selection_end.x() - self.selection_start.x(),
                         self.selection_end.y() - self.selection_start.y())

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            if self.tracking_enabled:
                success, bbox = self.tracker.update(frame)
                if success:
                    x, y, w, h = [int(coord) for coord in bbox]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio))