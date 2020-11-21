#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 11.20.2020
Updated on 11.20.2020

Author: haoshaui@handaotech.com
'''

import time, cv2
import functools
import numpy as np
import glob as gb
import os, sys, json, time, cv2

from PyQt5.Qt import QMutex
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot


class testInferWorker(QThread):
    resSignal = pyqtSignal(dict)
    stopSignal = pyqtSignal()

    def __init__(self, model, valid_dir, valid_suffix, parent=None):
        super(testInferWorker, self).__init__(parent)
        self.img_list = gb.glob(valid_dir + r"/*"+valid_suffix)
        self.model = model

    def run(self):
        img_list = self.img_list
        for img_file in img_list:
            image = cv2.imread(img_file, cv2.IMREAD_COLOR)
            boxes, labels, scores = model.infer(image)
            resDict = {
                "image":  image,
                "boxes":  boxes,
                "labels": labels,
                "scores": scores}
            self.resSignal.emit(resDict)
        self.stopSignal.emit()
            
        """
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch*w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.changePixmap.emit(convertToQtFormat)
        time.sleep(0.05)  # Note: This is the temperory method
        """


    