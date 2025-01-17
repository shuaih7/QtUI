#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 03.02.2021
Updated on 03.18.2021

Author: haoshuai@handaotech.com
'''

import os


def preprocessResults(results):
    boxes = results['boxes']
    labels = results['labels']
    
    width = list()
    s_boxes = list()
    boxes_info = list()
    boxes_index = list()
    
    for i, box in enumerate(boxes):
        label = labels[i]
        if label == 0: # Select the long defects
            boxes_info.append((box[0] + box[2]) / 2)
            boxes_index.append(i)
            width.append(box[2] - box[0])
        elif label == 1:
            s_boxes.append(box)
            
    pattern = {
        'x': boxes_info,
        'width': width,
        'indices': boxes_index,
        's_boxes': s_boxes
    }
    results['pattern'] = pattern
    
    return results