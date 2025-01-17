#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 11.20.2020
Updated on 02.05.2021

Author: haoshuai@handaotech.com
'''

import os
import cv2
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen


colors = [(255,0,0), (255,165,0), (0,0,255)]
font = cv2.FONT_HERSHEY_SIMPLEX


def draw_results(image, results):
    image = format_image(image)
    if results is None or len(results)==0: return image
    
    boxes = results['boxes']
    labels = results['labels']
    scores = results['scores']
    if len(boxes) == 0: return image
    
    for box, label, score in zip(boxes, labels, scores):
        xmin, ymin, xmax, ymax = box
        image = cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax),int(ymax)), colors[label], thickness=3)
        #image = cv2.putText(image, str(round(score,3)), (xmin,ymin), fontFace=font, 
        #    fontScale=0.5, color=color[label], thickness=2)
            
    return image
    
    
def format_image(image): # Gray to RGB
    if image.shape[-1] == 4: 
        image = image[:,:,:3]
    elif image.shape[-1] != 3: 
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    return image
    

class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.config_matrix = None
        self.pixmap = None
        self.scale = None
        
    def setConfig(self, config_matrix):
        self.config_matrix = config_matrix
        
    def refresh(self, image, results=None):
        image = draw_results(image, results)
        
        h, w, ch = image.shape[:3]
        bytesPerLine = ch*w
        convertToQtFormat = QImage(image.data.tobytes(), w, h, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(convertToQtFormat).scaled(self.size(), Qt.KeepAspectRatio, 
            Qt.SmoothTransformation)
        self.update()
        
    def resizeEvent(self, event):
        super(Canvas, self).resizeEvent(event)
        if self.pixmap is not None:
            self.pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        if self.pixmap is not None: 
            off_x = (self.size().width() - self.pixmap.width()) / 2
            off_y = (self.size().height() - self.pixmap.height()) / 2
            painter.drawPixmap(off_x, off_y, self.pixmap)
        
