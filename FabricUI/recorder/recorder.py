#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 03.02.2021
Updated on 03.02.2021

Author: haoshuai@handaotech.com
'''


class Recorder(object):
    def __init__(self, params):
        self.updateParams(params)
        
    def updateParams(self, params):
        self.params = params
        
    def __call__(self, results) -> bool:
        return True

