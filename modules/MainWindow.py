#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import cv2
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QPaintEvent, QBrush
from PyQt5.QtWidgets import QApplication, QColorDialog, QMainWindow, QVBoxLayout
from PyQt5.uic import loadUi
import conf.settings as settings
from modules.FpsMonitor import FpsMonitor
from modules.ImgLabel import ImgLabel
from modules.Tracker import Tracker


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        loadUi("ui/MainWindow.ui", self)

        #self.width = 640
        #self.height = 480

        self.btnColorPicker.clicked.connect(self.show_color_picker)

        #self.centralBodyContainer.setStyleSheet("background-color: yellow;")


        layout = QVBoxLayout()
        self.imgLabel = ImgLabel()
        layout.addWidget(self.imgLabel)
        self.centralBodyContainer.setLayout(layout)

        self.btnStartTracking.clicked.connect(self.tracking_objects)


        self.cmbTrackers.addItems(settings.TRACKERS_SOURCE_LIST)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.imgLabel.update_frame)
        self.timer.start(30)

        self.timerInfo = QTimer(self)
        self.timerInfo.timeout.connect(self.update_information)
        self.timerInfo.start(30)

        #self.fpsMonitor = FpsMonitor()


    def show_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            settings.TRACKER_BORDER_COLOR = color.red(), color.green(), color.blue()

            self.btnCurrColor.setStyleSheet(f"background-color : rgb{settings.TRACKER_BORDER_COLOR}")
            print("Выбранный цвет:", settings.TRACKER_BORDER_COLOR)
            self.listWidget.addItem("Выбранный цвет:" + str(settings.TRACKER_BORDER_COLOR))

    def tracking_objects(self):
        if self.imgLabel.bbox:
            trackerName = self.cmbTrackers.currentText()
            self.imgLabel.tracker = Tracker(trackerName)
            self.imgLabel.tracking_enabled = True
            self.imgLabel.tracker.create_tracker(self.imgLabel.frame, self.imgLabel.bbox)
        elif self.imgLabel.bbox == 0:
            self.listWidget.addItem("Select area")

    def update_information(self):
        self.lblFps.setText(str(self.imgLabel.FpsMonitor.getFps()))

















