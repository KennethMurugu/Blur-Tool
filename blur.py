# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:17:57 2017

@author: Kenneth
"""
from PIL import Image, ImageFilter
class BlurImage():
    def __init__(self, path, radius):
        self.path = path
        self.radius = radius
        
    def blur(self):
        img = Image.open(self.path)
        img_blurred = img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        return img_blurred