import time

import cv2
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QColor
from PyQt5.QtWidgets import QLabel
from cv2 import VideoCapture

from conf import settings
#from modules.Tracker import create_tracker
from modules.FpsMonitor import FpsMonitor
from modules.Tracker import Tracker


class ImgLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_capture = VideoCapture(settings.CAM_SOURCE_LIST[1])  # Инициализация видеозахвата
        self.tracking_enabled = False  #лаг для отслеживания области
        self.tracker = Tracker()  # Трекер OpenCV
        self.selection_start = QPoint()  # Начальная точка выбора области
        self.selection_end = QPoint()  # Конечная точка выбора области

        self.bbox = 0

        self.FpsMonitor = FpsMonitor()

        self.trackingOk = None

    def start_tracking(self, name, frame):
        # чтение трекера из cmbTrackers

        # создание трекера
        #self.tracker = create_tracker(name)

        print(self.tracker)
        # иницилизация трекера
        #self.tracker.init(frame, self.bbox)

        self.tracking_enabled = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.selection_start = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.selection_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_end = event.pos()
            self.update()

    def paintEvent(self, event):

        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(*settings.TRACKER_BORDER_COLOR), 2, Qt.SolidLine)
        painter.setPen(QPen(pen))
        #print(settings.TRACKER_BORDER_COLOR)
        painter.drawRect(self.selection_start.x(), self.selection_start.y(),
                         self.selection_end.x() - self.selection_start.x(),
                         self.selection_end.y() - self.selection_start.y())
        self.bbox = (self.selection_start.x(), self.selection_start.y(), self.selection_end.x() - self.selection_start.x(), self.selection_end.y() - self.selection_start.y())
        #print(self.bbox)

    def update_frame(self, keyboard=None):
        ret, self.frame = self.video_capture.read()
        if ret:
            self.frame = cv2.resize(self.frame, (self.size().width(), self.size().height()), cv2.INTER_LINEAR)

            if self.tracking_enabled:
                success, bbox = self.tracker.update(self.frame)
                if success:
                    self.trackingOk = True
                    x, y, w, h = [int(coord) for coord in bbox]
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), settings.TRACKER_BORDER_COLOR, 2)
                else:
                    self.trackingOk = False


            self.FpsMonitor.update()
            fps = self.FpsMonitor.getFps()

            #fps_current_time = time.time() - self.fps_start_time
            #fps = self.fps_frame_count / fps_current_time

            # Display FPS on the frame
            cv2.putText(self.frame, f": {round(fps, 2)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio))



