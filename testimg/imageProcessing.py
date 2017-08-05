# -*- coding: utf-8 -*-
import cv2
import math
import os
import numpy as np

def image_zoom(inputImg, OutputPath, times):
    resImg = cv2.resize(inputImg, None, fx = times, fy = times, interpolation = cv2.INTER_CUBIC)
    #cv2.imwrite(OutputPath, resImg)
    dirname = os.path.dirname(OutputPath)
    basename = os.path.basename(OutputPath)
    name,ext = os.path.splitext(basename)
    cv2.imencode(ext, resImg)[1].tofile(OutputPath)
    return OutputPath

def image_rotate(inputImg, OutputPath, angle):
    height, width = inputImg.shape[:2]
    if angle % 180 == 0:
        scale = 1
    elif angle % 90 == 0:
        scale = float(min(height, width)) / max(height, width)
    else:
        scale = 1/ (math.sqrt(pow(height, 2) + pow(width, 2)) / min(height, width))
    print(scale)
    rotateMat = cv2.getRotationMatrix2D((width/2, height/2), angle, scale)
    resImg = cv2.warpAffine(inputImg, rotateMat, (width, height))
   # cv2.imwrite(OutputPath, resImg)
    dirname = os.path.dirname(OutputPath)
    basename = os.path.basename(OutputPath)
    name,ext = os.path.splitext(basename)
    cv2.imencode(ext, resImg)[1].tofile(OutputPath)
    return OutputPath

def image_gray(inputImg, OutputPath):
    resImg = cv2.cvtColor(inputImg, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite(OutputPath, resImg)
    dirname = os.path.dirname(OutputPath)
    basename = os.path.basename(OutputPath)
    name,ext = os.path.splitext(basename)
    cv2.imencode(ext, resImg)[1].tofile(OutputPath)
    return OutputPath


def image_thresholdAdapt(inputImg, OutputPath):
    grayImg = cv2.cvtColor(inputImg, cv2.COLOR_BGR2GRAY)
    resImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
    #cv2.imwrite(OutputPath, resImg)
    dirname = os.path.dirname(OutputPath)
    basename = os.path.basename(OutputPath)
    name,ext = os.path.splitext(basename)
    cv2.imencode(ext, resImg)[1].tofile(OutputPath)
    return OutputPath


def image_GaussianBlur(inputImg, OutputPath):
    resImg = cv2.GaussianBlur(inputImg, (5, 5), 0)
    #cv2.imwrite(OutputPath, resImg)
    dirname = os.path.dirname(OutputPath)
    basename = os.path.basename(OutputPath)
    name,ext = os.path.splitext(basename)
    cv2.imencode(ext, resImg)[1].tofile(OutputPath)
    return OutputPath

def create_outputPath_name(inputPath, addStr):
    dirname = os.path.dirname(inputPath)
    basename = os.path.basename(inputPath)
    name,ext = os.path.splitext(basename)
    OutputPath = dirname + '/' + name + addStr + ext
    if not os.path.exists(OutputPath):
        return OutputPath
    else:
        i = 0
        while True:
            OutputPath = dirname + '/' + name + addStr + str(i) + ext
            if not os.path.exists(OutputPath):
                return OutputPath
            i += 1


def choose_model(model_type, inputPath):
    inputImg = cv2.imdecode(np.fromfile(inputPath, dtype=np.uint8), -1)
    OutputPath = create_outputPath_name(inputPath, '_'+model_type)

    if model_type == 'gray':
        str_tmp = image_gray(inputImg, OutputPath)
    elif model_type == 'binary':
        str_tmp = image_thresholdAdapt(inputImg, OutputPath)
    elif model_type == 'gaussian':
        str_tmp = image_GaussianBlur(inputImg, OutputPath)
    elif model_type == 'shrink':
        str_tmp = image_zoom(inputImg, OutputPath, 0.5)   #shrink
    elif model_type == 'enlarge':
        str_tmp = image_zoom(inputImg, OutputPath, 2)
    elif model_type == 'rotate90':
        str_tmp = image_rotate(inputImg, OutputPath, 90)
    elif model_type == 'rotate180':
        str_tmp = image_rotate(inputImg, OutputPath, 180)
    elif model_type == 'rotate270':
        str_tmp = image_rotate(inputImg, OutputPath, 270)

    return str_tmp


'''
if __name__ == '__main__':
    outpath = choose_model('binary', 'image/pic2.png')
    print(outpath)
'''