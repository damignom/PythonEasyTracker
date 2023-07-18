#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import cv2
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QPaintEvent, QBrush
from PyQt5.QtWidgets import QApplication, QColorDialog, QMainWindow, QVBoxLayout
from PyQt5.uic import loadUi
import conf.settings as settings
from modules.ImgLabel import ImgLabel

from modules.Tracker import create_tracker

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        loadUi("ui/MainWindow.ui", self)

        self.btnColorPicker.clicked.connect(self.show_color_picker)
        #self.btnStartTracking.clicked.connect(self.tracking_objects)


        layout = QVBoxLayout(self.centralBodyContainer)

        self.imgLabel = ImgLabel()
        layout.addWidget(self.imgLabel)


        self.cmbTrackers.addItems(settings.TRACKERS_SOURCE_LIST)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.imgLabel.update_frame)
        self.timer.start(30)  # Обновление каждые 30 миллисекунд


    def show_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            settings.TRACKER_BORDER_COLOR = color.red(), color.green(), color.blue()

            self.btnCurrColor.setStyleSheet(f"background-color : rgb{settings.TRACKER_BORDER_COLOR}")
            print("Выбранный цвет:", settings.TRACKER_BORDER_COLOR)


    """
    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:

            if self.tracking_enabled:
                success, bbox = self.tracker.update(frame)
                if success:
                    x, y, w, h = [int(coord) for coord in bbox]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Преобразование кадра из формата BGR в RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Создание объекта QImage из массива байтов
            qformat = QImage.Format_Indexed8
            if len(image.shape) == 3:
                if image.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
            outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)



            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

    
    def tracking_objects(self, frame):
        # чтение трекера из cmbTrackers
        trackerName = self.cmbTrackers.currentText()

        # создание трекера
        self.tracker = create_tracker(trackerName)

        self.tracking_enabled = True

    def MousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            #print("click")
            self.selection_start = event.pos()
            print(self.selection_start)

    def MouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.selection_end = event.pos()
            self.imgLabel.update()

    def MouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_end = event.pos()
            print(self.selection_end)
            self.tracking_enabled = True
            self.tracker = cv2.TrackerCSRT_create()
            self.imgLabel.update()

    def handlePaintEvent(self, event):
        self.imgLabel.paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(self.selection_start.x(), self.selection_start.y(),
                         self.selection_end.x() - self.selection_start.x(),
                         self.selection_end.y() - self.selection_start.y())




"""











