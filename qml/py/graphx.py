#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyotherside
import threading
import time
import os
import shutil
import random
from random import gauss
import math
import operator
import colorsys
from pathlib import Path    #for getting Home directory path
from itertools import chain #for LUTcube files

try:
    import PIL
    try:
        version = float((PIL.__version__).split(".")[0])
        if version < 7:
            pyotherside.send('warningPIL2old', )
    except:
        pyotherside.send('warningPIL2old', )
except ImportError:
    pyotherside.send('warningPILNotAvailable', )

from PIL import Image
from PIL import ImageOps
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import ImageChops
from PIL import ImageMath # for LUTimage files
from PIL.ExifTags import TAGS
from PIL import ExifTags
from io import BytesIO




def argb2rgba ( paintColor ) :
    first2 = paintColor[1:3]
    last6 = paintColor[3:9]
    rgbaColor = "#" + last6 + first2
    return rgbaColor
def argb2rgb ( paintColor ) :
    first2 = paintColor[1:3]
    last6 = paintColor[3:9]
    rgbColor = "#" + last6
    return rgbColor
def argb2alpha ( paintColor ) :
    first2 = paintColor[1:3]
    alphaValue = int(first2, 16)
    return alphaValue

def createTmpAndSaveFolder ( tempImageFolderPath, saveImageFolderPath ):
    if os.path.exists("/" + "/home" + "/nemo" + "/imageworks_tmp/"): #if folder exists from older versions, remove it
        shutil.rmtree("/" + "/home" + "/nemo" + "/imageworks_tmp/")
    if not os.path.exists("/"+tempImageFolderPath):
        os.makedirs("/"+tempImageFolderPath)
        pyotherside.send('folderExistence', )
    if not os.path.exists("/"+saveImageFolderPath):
        os.makedirs("/"+saveImageFolderPath)
        pyotherside.send('folderExistence', )

def createPreviewBaseImage ( inputPathPy, previewBaseImagePath, previewBaseImageWidth ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    origWidth, origHeight = img.size
    factor = origWidth / origHeight
    previewBaseImageHeight = previewBaseImageWidth / factor
    size = (int(previewBaseImageWidth), int(previewBaseImageHeight))
    output_img = img.resize(size)
    output_img.save(previewBaseImagePath, compress_level=1)
    pyotherside.send('previewImageCreated', previewBaseImagePath)
    img.close()
    output_img.close()





def cropNowFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, undoNr ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    output_img = img.crop(area)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def cropCoordinatesFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, undoNr ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    rectX_real = int(rectX)
    rectY_real = int(rectY)
    rectWidth_real = int(rectWidth)
    rectHeight_real = int(rectHeight)
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    output_img = img.crop(area)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def cropCanvasPolygonFunction( inputPathPy, outputPathPy, freeDrawPolyCoordinates, scaleFactor, paintColor, actionSelection ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    if "keep" in actionSelection:
        mask_im = Image.new( 'L', (img.size), 0 )
    else:
        mask_im = Image.new( 'L', (img.size), 255 )
    draw = ImageDraw.Draw(mask_im)
    strokesList = list( freeDrawPolyCoordinates.split("/") )
    for i in range (0, len(strokesList)-1) :
        coordinatesList = list( strokesList[i].split(";") )
        del coordinatesList[-1] # remove last comma
        coordinatesList = list(map(float, coordinatesList))
        coordinatesList = [i * float(scaleFactor) for i in coordinatesList]
        pairSublist = []
        fullPairsList = []
        for i in range(0, len(coordinatesList)-1, 2):
            pairSublist.append ( coordinatesList[i] )
            pairSublist.append ( coordinatesList[i+1] )
            fullPairsList.append ( tuple(pairSublist) )
            pairSublist.clear()
        coordinatesTuples = tuple(fullPairsList)
        if not 0 < len(coordinatesTuples) < 2:
            if "keep" in actionSelection:
                draw.polygon( (coordinatesTuples), fill = 255,)
            else:
                draw.polygon( (coordinatesTuples), fill = 0,)
    output_img = Image.new( 'RGBA', (img.size), argb2rgba(paintColor) )
    output_img.paste(img, (0,0), mask_im)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    pyotherside.send('clearDrawCanvas', )
    img.close()
    output_img.close()


def cropCanvasShapeFunction( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, paintColor, actionSelection, solidTypeTool ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    if "keep" in actionSelection:
        mask_im = Image.new( 'L', (img.size), 0 )
    else:
        mask_im = Image.new( 'L', (img.size), 255 )

    draw = ImageDraw.Draw(mask_im)
    if "keep" in actionSelection:
        if "circle" in solidTypeTool:
            draw.ellipse( (area), fill=255 )
        else:
            draw.rectangle( (area), fill=255 )
    else:
        if "circle" in solidTypeTool:
            draw.ellipse( (area), fill=0 )
        else:
            draw.rectangle( (area), fill=0 )
    output_img = Image.new( 'RGBA', (img.size), argb2rgba(paintColor) )
    output_img.paste(img, (0,0), mask_im)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    pyotherside.send('clearDrawCanvas', )
    img.close()
    output_img.close()


def perspectiveCorrectionFunction ( inputPathPy, outputPathPy, coeffs, scaleFactor, undoNr, fillColor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    width, height = img.size
    deform = img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC )
    fff = Image.new('RGBA', deform.size, argb2rgba(fillColor))
    output_img = Image.composite(deform, fff, deform)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    deform.close()
    fff.close()
    output_img.close()






def rotateLeftFunction ( inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    output_img = img.rotate(90, expand = True)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def mirrorHorizontalFunction ( inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    output_img = ImageOps.mirror(img)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def mirrorVerticalFunction ( inputPathPy, outputPathPy  ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    output_img = ImageOps.flip(img)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def rotateRightFunction ( inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    output_img = img.rotate(270, expand = True)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def tiltAngleFunction ( inputPathPy, outputPathPy, tiltAngle, fillColor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    angleT = int(tiltAngle)
    rot = img.rotate(angleT, expand = True)
    fff = Image.new('RGBA', rot.size, argb2rgba(fillColor))
    output_img = Image.composite(rot, fff, rot)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    fff.close()
    rot.close()
    output_img.close()





def scaleFunction ( inputPathPy, outputPathPy, factor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    output_img = ImageOps.scale(img, factor)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def freescaleFunction ( inputPathPy, outputPathPy, widthX, heightY ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    size = (int(widthX), int(heightY))
    output_img = img.resize(size)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def paddingImageFunction ( inputPathPy, outputPathPy, paddingRatio, paddingFill, paintColor, blurFactor ) :
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    origWidth, origHeight = img.size
    origRatio = origWidth / origHeight
    if ( origRatio < paddingRatio ) :
        # pad on width (sides)
        backfillHeight = origHeight
        backfillWidth = backfillHeight * paddingRatio
        if "color" in paddingFill:
            backfillImage = Image.new( 'RGBA', (int(backfillWidth), int(backfillHeight)), argb2rgba(paintColor) )
        if "blur" in paddingFill:
            sizeFill = ( int(backfillWidth), int(backfillHeight) )
            backfillImage = img.resize(sizeFill)
            backfillImage = backfillImage.filter(ImageFilter.GaussianBlur(int(blurFactor)))
        pasteX = backfillWidth/2 - origWidth/2
        pasteY = 0
        backfillImage.paste(img, (int(pasteX), int(pasteY)))
        output_img = backfillImage
    else :
        # pad on height (top, bottom)
        backfillWidth = origWidth
        backfillHeight = backfillWidth / paddingRatio
        if "color" in paddingFill:
            backfillImage = Image.new( 'RGBA', (int(backfillWidth), int(backfillHeight)), argb2rgba(paintColor) )
        if "blur" in paddingFill:
            sizeFill = ( int(backfillWidth), int(backfillHeight) )
            backfillImage = img.resize(sizeFill)
            backfillImage = backfillImage.filter(ImageFilter.GaussianBlur(int(blurFactor)))
        pasteX = 0
        pasteY = backfillHeight/2 - origHeight/2
        backfillImage.paste(img, (int(pasteX), int(pasteY)))
        output_img = backfillImage
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    pyotherside.send('updateSliderScale',)
    img.close()
    backfillImage.close()
    output_img.close()







def enhanceContrastFunction ( targetImage, inputPathPy, outputPathPy, factorEnhance, previewBaseImageWidth ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    if "preview" in targetImage:
        origWidth, origHeight = img.size
        factor = origWidth / origHeight
        previewBaseImageHeight = previewBaseImageWidth / factor
        size = (int(previewBaseImageWidth), int(previewBaseImageHeight))
        img2 = img.resize(size)
        output_img = ImageEnhance.Contrast(img2)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('previewImageMainCreated', outputPathPy)
    else:
        output_img = ImageEnhance.Contrast(img)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()


def enhanceBrightnessFunction ( targetImage, inputPathPy, outputPathPy, factorEnhance, previewBaseImageWidth ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    if "preview" in targetImage:
        origWidth, origHeight = img.size
        factor = origWidth / origHeight
        previewBaseImageHeight = previewBaseImageWidth / factor
        size = (int(previewBaseImageWidth), int(previewBaseImageHeight))
        img2 = img.resize(size)
        output_img = ImageEnhance.Brightness(img2)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('previewImageMainCreated', outputPathPy)
    else:
        output_img = ImageEnhance.Brightness(img)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()


def enhanceColorFunction ( targetImage, inputPathPy, outputPathPy, factorEnhance, previewBaseImageWidth ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    if "preview" in targetImage:
        origWidth, origHeight = img.size
        factor = origWidth / origHeight
        previewBaseImageHeight = previewBaseImageWidth / factor
        size = (int(previewBaseImageWidth), int(previewBaseImageHeight))
        img2 = img.resize(size)
        output_img = ImageEnhance.Color(img2)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('previewImageMainCreated', outputPathPy)
    else:
        output_img = ImageEnhance.Color(img)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()


def enhanceSharpnessFunction ( targetImage, inputPathPy, outputPathPy, factorEnhance, previewBaseImageWidth ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    if "preview" in targetImage:
        origWidth, origHeight = img.size
        factor = origWidth / origHeight
        previewBaseImageHeight = previewBaseImageWidth / factor
        size = (int(previewBaseImageWidth), int(previewBaseImageHeight))
        img2 = img.resize(size)
        output_img = ImageEnhance.Sharpness(img2)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('previewImageMainCreated', outputPathPy)
    else:
        output_img = ImageEnhance.Sharpness(img)
        output_img.enhance(factorEnhance).save(outputPathPy, compress_level=1)
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()


def enhanceHueFunction ( targetImage, inputPathPy, outputPathPy, hueAngle, previewBaseImageWidth ):
    def newBandH(intensity):
        iO = int( intensity + hueAngle8bit)
        return iO
    hueAngle8bit = hueAngle * 255/360
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    if "preview" in targetImage:
        origWidth, origHeight = img.size
        factor = origWidth / origHeight
        previewBaseImageHeight = previewBaseImageWidth / factor
        size = (int(previewBaseImageWidth), int(previewBaseImageHeight))
        img2 = img.resize(size)
        A = img2.getchannel('A')
        img2 = img2.convert('HSV')
        multiBands = img2.split()
        newH = multiBands[0].point(newBandH)
        hsv_img = Image.merge("HSV", (newH, multiBands[1], multiBands[2]))
        rgb_img = hsv_img.convert('RGB')
        R,G,B = rgb_img.split() # add original Alpha
        output_img = Image.merge('RGBA',(R,G,B,A))
        output_img.save(outputPathPy, compress_level=1)
        pyotherside.send('previewImageMainCreated', outputPathPy)
    else:
        A = img.getchannel('A')
        img = img.convert('HSV')
        multiBands = img.split()
        newH = multiBands[0].point(newBandH)
        hsv_img = Image.merge("HSV", (newH, multiBands[1], multiBands[2]))
        rgb_img = hsv_img.convert('RGB')
        R,G,B = rgb_img.split() # add original Alpha
        output_img = Image.merge('RGBA',(R,G,B,A))
        output_img.save(outputPathPy, compress_level=1)
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()









def autocontrastFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('RGB')
    rgb_img = ImageOps.autocontrast(img)
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def stretchContrastFunction ( targetImage, inputPathPy, outputPathPy ):
    def normalizeRed(intensity):
        iI      = intensity
        minI    = 86
        maxI    = 230
        minO    = 0
        maxO    = 255
        iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
        return iO
    def normalizeGreen(intensity):
        iI      = intensity
        minI    = 90
        maxI    = 225
        minO    = 0
        maxO    = 255
        iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
        return iO
    def normalizeBlue(intensity):
        iI      = intensity
        minI    = 100
        maxI    = 210
        minO    = 0
        maxO    = 255
        iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
        return iO
    imgTemp = Image.open(inputPathPy)
    imgTemp = ImageOps.exif_transpose(imgTemp)
    imgTemp = imgTemp.convert('RGBA')
    A = imgTemp.getchannel('A')
    img = Image.new("RGBA", imgTemp.size)
    img.paste(imgTemp)
    multiBands = img.split()
    normalizedRedBand = multiBands[0].point(normalizeRed)
    normalizedGreenBand = multiBands[1].point(normalizeGreen)
    normalizedBlueBand = multiBands[2].point(normalizeBlue)
    rgb_img = Image.merge("RGB", (normalizedRedBand, normalizedGreenBand, normalizedBlueBand))
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()
    imgTemp.close()


def blackWhiteFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    rgb_img = img.convert("1")
    rgb_img = rgb_img.convert('RGB')
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def coalFilterFunction( targetImage, inputPathPy, outputPathPy, blurRadius ):
    def dodge(front,back):
        if back != 255:
            result = int(front*255/(255-back))
        else:
            result = int(255)
        if result > 255:
            result = 255
        return result
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    rgbGray_img = ImageOps.grayscale(img)
    pixdata_back = rgbGray_img.load()
    rgbInvertedGray_img = ImageOps.invert(rgbGray_img)
    rgbBlurInverted_img = rgbInvertedGray_img.filter(ImageFilter.GaussianBlur(blurRadius))
    pixdata_front = rgbBlurInverted_img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            xBack = pixdata_back[x, y]
            xFront = pixdata_front[x, y]
            pixdata_back[x, y] = ( dodge(xBack, xFront) )
            #pixdata_back[x, y] = ( dodge(xFront, xBack) )
    rgbGray_img = rgbGray_img.convert('RGB')
    R2,G2,B2 = rgbGray_img.split()
    output_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def grayscaleFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    rgb_img = ImageOps.grayscale(img)
    rgb_img = rgb_img.convert('RGB')
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def equalizeFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('RGB')
    rgb_img = ImageOps.equalize(img)
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def solarizeFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('RGB')
    rgb_img = ImageOps.solarize(img)
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def invertFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('RGB')
    rgb_img = ImageOps.invert(img)
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()




def brightspotFilterFunction ( targetImage, inputPathPy, outputPathPy, spotType, spotSize ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('RGB')
    if "min" in spotType:
        rgb_img = img.filter(ImageFilter.MinFilter( int(spotSize) ))
    if "max" in spotType:
        rgb_img = img.filter(ImageFilter.MaxFilter( int(spotSize) ))
    if "med" in spotType:
        rgb_img = img.filter(ImageFilter.MedianFilter( int(spotSize) ))
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()



def modedrawingFunction ( targetImage, inputPathPy, outputPathPy, brushSize ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    output_img = img.filter(ImageFilter.ModeFilter(size=int(brushSize)))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def posterizeFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('RGB')
    rgb_img = ImageOps.posterize(img, bits=2) # bits from 1...8 possible
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def blurFunction ( targetImage, inputPathPy, outputPathPy, factor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    output_img = img.filter(ImageFilter.GaussianBlur(factor))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def unsharpmaskFunction ( targetImage, inputPathPy, outputPathPy, radiusMask, percentMask, thresholdMask ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    output_img = img.filter(ImageFilter.UnsharpMask(radius=int(radiusMask), percent=int(percentMask), threshold=int(thresholdMask)))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def findedgesFunction ( targetImage, inputPathPy, outputPathPy, fileTargetType ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if ".gif" in fileTargetType :
        img = img.convert('RGBA')
    if ".GIF" in fileTargetType :
        img = img.convert('RGBA')
    if ".png"  in fileTargetType :
        img = img.convert('RGB')
    if ".bmp"  in fileTargetType :
        img = img.convert('RGB')
    output_img = img.filter(ImageFilter.FIND_EDGES)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def contourFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    output_img = img.filter(ImageFilter.CONTOUR)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def embossFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    output_img = img.filter(ImageFilter.EMBOSS)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def edgeenhanceFunction ( targetImage, inputPathPy, outputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    output_img = img.filter(ImageFilter.EDGE_ENHANCE)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()



def sepiaFunction ( targetImage, inputPathPy, outputPathPy ):
    def make_linear_ramp(white):
        ramp = []
        r, g, b = white
        for i in range(255):
            ramp.extend((int(r*i/255), int(g*i/255), int(b*i/255)))
        return ramp
    sepia = make_linear_ramp((255, 240, 192))
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('L')
    img.putpalette(sepia)
    img = img.convert('RGB')
    rgb_img = img.convert('RGB', (
        1.07, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 0.94, 0,
    ))
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def colorToAlphaFunction ( targetImage, inputPathPy, outputPathPy, targetColor2Alpha, targetColorTolerance ) :
    targetColorTolerance = int(targetColorTolerance)
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGBA")
    pixdata = img.load()
    if "black" in targetColor2Alpha :
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = pixdata[x, y] # way faster than getpixel
                if (r <= targetColorTolerance) and (g <= targetColorTolerance) and (b <= targetColorTolerance):
                    pixdata[x, y] = (0, 0, 0, 0)
    if "white" in targetColor2Alpha :
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = pixdata[x, y]
                if (r >= (255-targetColorTolerance)) and (g >= (255-targetColorTolerance)) and (b >= (255-targetColorTolerance)):
                    pixdata[x, y] = (0, 0, 0, 0)
    output_img = img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def repixelMiddleStepFunction ( oldA, oldR, oldG, oldB, newA, newR, newG, newB, compareA, compareR, compareG, compareB, tolA, tolR, tolG, tolB, changeA, changeR, changeG, changeB, modePixeldraw ) :
        pyotherside.send('startRepixelFunctionFromPy', oldA, oldR, oldG, oldB, newA, newR, newG, newB, compareA, compareR, compareG, compareB, tolA, tolR, tolG, tolB, changeA, changeR, changeG, changeB, modePixeldraw )

def replacePixelsFunction ( inputPathPy, outputPathPy, oldA, oldR, oldG, oldB, newA, newR, newG, newB, compareA, compareR, compareG, compareB, tolA, tolR, tolG, tolB, changeA, changeR, changeG, changeB, modePixeldraw ) :
    oldA = int(oldA)
    oldR = int(oldR)
    oldG = int(oldG)
    oldB = int(oldB)
    newA = int(newA)
    newR = int(newR)
    newG = int(newG)
    newB = int(newB)
    lowerR = oldR-int(tolR)
    upperR = oldR+int(tolR)
    lowerG = oldG-int(tolG)
    upperG = oldG+int(tolG)
    lowerB = oldB-int(tolB)
    upperB = oldB+int(tolB)
    lowerA = oldA-int(tolA)
    upperA = oldA+int(tolA)
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGBA")
    pixdata = img.load()    
    # lookup table for operators
    op = { '=': lambda x, y, v, w: ( (x >= v) and (x <= w) ),
        '!=': lambda x, y, v, w: ( (x < v) or (x > w) ),
        #'!=': lambda x, y, z: (x not in z),
        '<=': lambda x, y, v, w: operator.le(x,y),
        '>=': lambda x, y, v, w: operator.ge(x,y),}
    if "normal" in modePixeldraw:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = pixdata[x, y]
                if ( (op[compareA](a, oldA, lowerA, upperA)) and (op[compareR](r, oldR, lowerR, upperR)) and (op[compareG](g, oldG, lowerG, upperG)) and (op[compareB](b, oldB, lowerB, upperB)) ) :
                    if "true" in changeR:
                        writeR = newR
                    else:
                        writeR = r
                    if "true" in changeG:
                        writeG = newG
                    else:
                        writeG = g
                    if "true" in changeB:
                        writeB = newB
                    else:
                        writeB = b
                    if "true" in changeA:
                        writeA = newA
                    else:
                        writeA = a
                    pixdata[x, y] = ( writeR, writeG, writeB, writeA )
    if "invert" in modePixeldraw:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = pixdata[x, y]
                if ( (op[compareA](a, oldA, lowerA, upperA)) and (op[compareR](r, oldR, lowerR, upperR)) and (op[compareG](g, oldG, lowerG, upperG)) and (op[compareB](b, oldB, lowerB, upperB)) ) :
                    writeR = r
                    writeG = g
                    writeB = b
                    writeA = a
                    pixdata[x, y] = ( writeR, writeG, writeB, writeA )
                else:
                    if "true" in changeR:
                        writeR = newR
                    else:
                        writeR = r
                    if "true" in changeG:
                        writeG = newG
                    else:
                        writeG = g
                    if "true" in changeB:
                        writeB = newB
                    else:
                        writeB = b
                    if "true" in changeA:
                        writeA = newA
                    else:
                        writeA = a
                    pixdata[x, y] = ( writeR, writeG, writeB, writeA )
    output_img = img
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def addFrameFunction ( targetImage, inputPathPy, outputPathPy, radiusEdgeBlur, paintColor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    RADIUS = int(radiusEdgeBlur)
    diam = 2*RADIUS
    back = Image.new('RGBA', (img.size[0]+diam, img.size[1]+diam), argb2rgba(paintColor) )
    back.paste(img, (RADIUS, RADIUS))
    mask = Image.new('L', back.size, 0)
    draw = ImageDraw.Draw(mask)
    x0, y0 = 0, 0
    x1, y1 = back.size
    for d in range(diam+RADIUS):
        x1, y1 = x1-1, y1-1
        alpha = 255 if d<RADIUS else int(255*(diam+RADIUS-d)/diam)
        draw.rectangle([x0, y0, x1, y1], outline=alpha)
        x0, y0 = x0+1, y0+1
    blur = back.filter(ImageFilter.GaussianBlur(RADIUS/2))
    back.paste(blur, mask=mask)
    back.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    back.close()


def tintWithColorFunction ( targetImage, inputPathPy, outputPathPy, tint_color, factorBrightness ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    if "warmer" in tint_color:
        A = img.getchannel('A')
        img = img.convert('RGB')
        rgb_img = img.convert('RGB', (
            1.1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 0.9, 0,
        ))
        R,G,B = rgb_img.split() # add original Alpha
        output_img = Image.merge('RGBA',(R,G,B,A))
        output_img.save(outputPathPy, compress_level=1)
    elif "colder" in tint_color:
        A = img.getchannel('A')
        img = img.convert('RGB')
        rgb_img = img.convert('RGB', (
            0.9, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1.1, 0,
        ))
        R,G,B = rgb_img.split() # add original Alpha
        output_img = Image.merge('RGBA',(R,G,B,A))
        output_img.save(outputPathPy, compress_level=1)
    else:
        img = img.convert('RGBA')
        img2 = Image.new( 'RGBA', img.size, argb2rgba(tint_color) )
        output_img = ImageChops.multiply(img, img2)
        enhanced_img = ImageEnhance.Brightness(output_img)
        enhanced_img.enhance(factorBrightness).save(outputPathPy, compress_level=1)
        img2.close()
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def miniatureFocusFunction ( targetImage, inputPathPy, outputPathPy, alphaMaskPath, radiusEdgeBlur, enhanceColorFaktor, enhanceContrastFaktor, addExtraBlurAroundPath ) :
    blurRadius = radiusEdgeBlur
    im_base = Image.open( inputPathPy )
    #im_base = ImageOps.exif_transpose(im_base)
    if im_base.mode not in ('RGBA'):
        im_base = im_base.convert('RGBA')
    # the alpha-mask that will be blurred, could also be programmatically created instead of loading an imageMask
    im_mask = Image.open( alphaMaskPath )
    #im_mask = ImageOps.exif_transpose(im_mask)
    im_mask = im_mask.convert("L").resize(im_base.size)    
    if enhanceColorFaktor != 1:
        enh = ImageEnhance.Color(im_base)
        im_base = enh.enhance(enhanceColorFaktor)
    if enhanceContrastFaktor != 1:
        enh = ImageEnhance.Contrast(im_base)
        im_base = enh.enhance(enhanceContrastFaktor)
    im_blurred = im_base.copy()
    im_blurred = im_blurred.filter(ImageFilter.GaussianBlur(blurRadius))
    im_base = im_base.convert("RGBA")
    im_base.paste( im_blurred, mask = im_mask )
    # add extra bluring around the center
    if "none" not in addExtraBlurAroundPath:
        im_mask = Image.open( addExtraBlurAroundPath )
        #im_mask = ImageOps.exif_transpose(im_mask)
        im_mask = im_mask.convert("L").resize(im_base.size)
        im_blurred = im_base.copy()
        im_blurred = im_blurred.filter(ImageFilter.GaussianBlur(4))
        im_base = im_base.convert("RGBA")
        im_base.paste( im_blurred, mask = im_mask )
    output_img = im_base
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    output_img.close()
    im_blurred.close()
    im_base.close()
    im_mask.close()


def smoothSurfaceFunction ( targetImage, inputPathPy, outputPathPy, smoothingStrength ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    if "normal" in smoothingStrength:
        output_img = img.filter(ImageFilter.SMOOTH)
    else:
        output_img = img.filter(ImageFilter.SMOOTH_MORE)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def quantizeFunction ( targetImage, inputPathPy, outputPathPy, colorsAmount ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    output_img = img.quantize(int(colorsAmount))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def addAlphaFunction ( targetImage, inputPathPy, outputPathPy, percentAlpha ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    amountAlpha = 255/100 * int(percentAlpha)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    img.putalpha(int(amountAlpha))
    output_img = img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def extractColorFunction ( targetImage, inputPathPy, outputPathPy, colorExtract ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    data = img.getdata()
    if "R" in colorExtract:
        r = [(d[0], 0, 0, d[3]) for d in data]
        img.putdata(r)
        output_img = img
    if "G" in colorExtract:
        g = [(0, d[1], 0, d[3]) for d in data]
        img.putdata(g)
        output_img = img
    if "B" in colorExtract:
        b = [(0, 0, d[2], d[3]) for d in data]
        img.putdata(b)
        output_img = img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def extractChannelFunction ( targetImage, inputPathPy, outputPathPy, channelExtract ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    if "A" in channelExtract:
        output_img = img.getchannel("A")
    if "R" in channelExtract:
        output_img = img.getchannel("R")
    if "G" in channelExtract:
        output_img = img.getchannel("G")
    if "B" in channelExtract:
        output_img = img.getchannel("B")
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def rechannelMiddleStepFunction ( channelPathAlpha, channelPathRed, channelPathGreen, channelPathBlue, factorA, factorR, factorG, factorB, saturationA, saturationR, saturationG, saturationB, invertA, invertR, invertG, invertB ) :
    pyotherside.send('startRechannelFunctionFromPy', channelPathAlpha, channelPathRed, channelPathGreen, channelPathBlue, factorA, factorR, factorG, factorB, saturationA, saturationR, saturationG, saturationB, invertA, invertR, invertG, invertB )

def rechannelFunction ( inputPathPy, outputPathPy, channelPathAlpha, channelPathRed, channelPathGreen, channelPathBlue, factorA, factorR, factorG, factorB, saturationA, saturationR, saturationG, saturationB, invertA, invertR, invertG, invertB ) :
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    originalAlpha = img.getchannel("A")
    originalRed = img.getchannel("R")
    originalGreen = img.getchannel("G")
    originalBlue = img.getchannel("B")
    if "original" in channelPathAlpha :
        setAlpha = originalAlpha
    else:
        imgNewAlpha = Image.open(channelPathAlpha)
        imgNewAlpha = ImageOps.exif_transpose(imgNewAlpha)
        imgNewAlpha = imgNewAlpha.convert('RGBA').resize(img.size)
        if "gray" in factorA:
            setAlpha = imgNewAlpha.convert('L')
        else:
            setAlpha = imgNewAlpha.getchannel(factorA)
        imgNewAlpha.close()
    if "original" in channelPathRed :
        setRed = originalRed
    else:
        imgNewRed = Image.open(channelPathRed)
        imgNewRed = ImageOps.exif_transpose(imgNewRed)
        imgNewRed = imgNewRed.convert('RGBA').resize(img.size)
        if "gray" in factorR:
            setRed = imgNewRed.convert('L')
        else:
            setRed = imgNewRed.getchannel(factorR)
        imgNewRed.close()
    if "original" in channelPathGreen :
        setGreen = originalGreen
    else:
        imgNewGreen = Image.open(channelPathGreen)
        imgNewGreen = ImageOps.exif_transpose(imgNewGreen)
        imgNewGreen = imgNewGreen.convert('RGBA').resize(img.size)
        if "gray" in factorG:
            setGreen = imgNewGreen.convert('L')
        else:
            setGreen = imgNewGreen.getchannel(factorG)
        imgNewGreen.close()
    if "original" in channelPathBlue :
        setBlue = originalBlue
    else:
        imgNewBlue = Image.open(channelPathBlue)
        imgNewBlue = ImageOps.exif_transpose(imgNewBlue)
        imgNewBlue = imgNewBlue.convert('RGBA').resize(img.size)
        if "gray" in factorB:
            setBlue = imgNewBlue.convert('L')
        else:
            setBlue = imgNewBlue.getchannel(factorB)
        imgNewBlue.close()
    combined_img = Image.merge("RGBA", (setRed, setGreen, setBlue, setAlpha))
    # now apply Alpha and RGB intensity changes
    A = combined_img.getchannel('A')
    A = Image.eval (A, lambda px: int(px*saturationA) )
    combined_img = combined_img.convert('RGB')
    rgb_img = combined_img.convert('RGB', (
        saturationR, 0, 0, 0,
        0, saturationG, 0, 0,
        0, 0, saturationB, 0,
    ))
    R,G,B = rgb_img.split()

    if "invert" in invertA:
        A = ImageChops.invert(A)
    if "invert" in invertR:
        R = ImageChops.invert(R)
    if "invert" in invertG:
        G = ImageChops.invert(G)
    if "invert" in invertB:
        B = ImageChops.invert(B)

    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def createHistogramImageFunction ( inputPathPy, outputPathPy, outputPathHistA, outputPathHistR, outputPathHistG, outputPathHistB, outputPathHistRGB ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    histogram = img.histogram()

    redAmounts = histogram[0:256]
    max_red = max(redAmounts)
    redNormalized = list(map(lambda x: x/max_red, redAmounts))
    greenAmounts = histogram[256:512]
    max_green = max(greenAmounts)
    greenNormalized = list(map(lambda x: x/max_green, greenAmounts))
    blueAmounts = histogram[512:768]
    max_blue = max(blueAmounts)
    blueNormalized = list(map(lambda x: x/max_blue, blueAmounts))
    alphaAmounts = histogram[768:1024]
    max_alpha = max(alphaAmounts)
    alphaNormalized = list(map(lambda x: x/max_alpha, alphaAmounts))
    rgbAmounts = [ redAmounts[i]+greenAmounts[i]+blueAmounts[i] for i in range(len(redAmounts)) ]
    max_rgb = max(rgbAmounts)
    rgbNormalized = list(map(lambda x: x/max_rgb, rgbAmounts))

    heightY = 256
    widthX = 256
    column_width = 1
    imgHistRGB = Image.new("RGBA", (widthX, heightY), (0,0,0,0))
    imgHistR = Image.new("RGBA", (widthX, heightY), (0,0,0,0))
    imgHistG = Image.new("RGBA", (widthX, heightY), (0,0,0,0))
    imgHistB = Image.new("RGBA", (widthX, heightY), (0,0,0,0))
    imgHistA = Image.new("RGBA", (widthX, heightY), (0,0,0,0))
    drawRGB = ImageDraw.Draw(imgHistRGB)
    drawR = ImageDraw.Draw(imgHistR)
    drawG = ImageDraw.Draw(imgHistG)
    drawB = ImageDraw.Draw(imgHistB)
    drawA = ImageDraw.Draw(imgHistA)
    for i in range (0,256):
        drawRGB.line (xy = [ (i, heightY), (i, heightY - (heightY*rgbNormalized[i]) ) ], fill = (i,i,i,255), width = column_width )
        drawR.line (xy = [ (i, heightY), (i, heightY - (heightY*redNormalized[i]) ) ], fill = (i,0,0,255), width = column_width )
        drawG.line (xy = [ (i, heightY), (i, heightY - (heightY*greenNormalized[i]) ) ], fill = (0,i,0,255), width = column_width )
        drawB.line (xy = [ (i, heightY), (i, heightY - (heightY*blueNormalized[i]) ) ], fill = (0,0,i,255), width = column_width )
        drawA.line (xy = [ (i, heightY), (i, heightY - (heightY*alphaNormalized[i]) ) ], fill = (0,0,0,255), width = column_width )
    imgHistR.save(outputPathHistR, compress_level=1)
    imgHistG.save(outputPathHistG, compress_level=1)
    imgHistB.save(outputPathHistB, compress_level=1)
    imgHistA.save(outputPathHistA, compress_level=1)
    imgHistRGB.save(outputPathHistRGB, compress_level=1)
    pyotherside.send('histogramsReady', max_alpha, max_red, max_green, max_blue, max_rgb)
    img.close()
    imgHistR.close()
    imgHistG.close()
    imgHistB.close()
    imgHistA.close()
    imgHistRGB.close()


def colorcurveMiddleStepFunction ( curveFactors, currentColor, minValue, maxValue ) :
    pyotherside.send('startColorCurveFunctionFromPy', curveFactors, currentColor, minValue, maxValue )


def colorCurveFunction ( inputPathPy, outputPathPy, curveFactors, currentColor, minValue, maxValue ):
    factorsTempList = list( curveFactors.split(";") )
    del factorsTempList[-1] # remove last semicolon
    factorsList = list(map(float, factorsTempList))

    #pyotherside.send('debugPythonLogs', factorsList)
    def newBand(intensity):
        iO = int( intensity * factorsList[intensity])
        if iO < int(minValue):
            iO = int(minValue)
        if iO > int(maxValue):
            iO = int(maxValue)
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    if "red" in currentColor:
        R = R.point(newBand)
    if "green" in currentColor:
        G = G.point(newBand)
    if "blue" in currentColor:
        B = B.point(newBand)
    if "alpha" in currentColor:
        A = A.point(newBand)
    if "rgb" in currentColor:
        R = R.point(newBand)
        G = G.point(newBand)
        B = B.point(newBand)
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()






def filtersEffectsMiddleStepFunction( effectName, coalValue, blurValue, centerFocusValue, miniatureBlurValue, miniatureColorValue, addFrameValue, brushSize, quantizeColors, targetColor2Alpha, alphaTolerance, opacityValue, colorExtractARGB, channelExtractARGB, unsharpRadiusMask, unsharpPercentMask, unsharpThresholdMask, brightspotSize ):
    pyotherside.send('startFiltersEffectsFunctionFromPy', effectName, coalValue, blurValue, centerFocusValue, miniatureBlurValue, miniatureColorValue, addFrameValue, brushSize, quantizeColors, targetColor2Alpha, alphaTolerance, opacityValue, colorExtractARGB, channelExtractARGB, unsharpRadiusMask, unsharpPercentMask, unsharpThresholdMask, brightspotSize )


def gothamFilterFunction( targetImage, inputPathPy, outputPathPy, sharpenFactor ):
    factorsList1 = [0,0.14599184782608696,0.1486243206521739,0.1513870018115942,0.15427989130434783,0.15729959239130437,0.16044497282608697,0.16371797360248447,0.1671195652173913,0.1706483997584541,0.17430366847826087,0.1780864006916996,0.18199728260869566,0.18603548285953175,0.19020040760869564,0.19449275362318844,0.19891304347826086,0.2034606777493606,0.2081351902173913,0.21293710669336385,0.21786684782608695,0.22292394539337473,0.22810801630434782,0.2334194825141777,0.2388586956521739,0.24442527173913042,0.2501188858695652,0.2559398902979066,0.26188858695652173,0.2679646504872564,0.2741677989130435,0.2804983345021038,0.28695652173913044,0.29341032608695655,0.2997452445652174,0.3059835986024845,0.3121452294685991,0.31824829245005876,0.3243090317505721,0.3303415900222965,0.3363586956521739,0.3423722494697773,0.34839301889233953,0.3544303747472194,0.36049283596837944,0.3665885416666667,0.37272492320415884,0.37890841813135984,0.3851449275362319,0.39144021739130436,0.39779959239130436,0.4042276081628304,0.41072846989966555,0.41730638586956526,0.42396525261674717,0.4307083745059289,0.4375388198757764,0.4444597397025172,0.4514740676536732,0.45858425064480474,0.46579257246376815,0.4731014455630791,0.48051312675315566,0.4880294599723948,0.4956521739130435,0.5032937918060201,0.5108747117918313,0.5184072842310188,0.5259031329923274,0.5333737003780719,0.5408297748447205,0.5482810586344152,0.5557367149758454,0.5632058703097083,0.5706971577555816,0.5782182971014492,0.5857766018306636,0.5933794466403163,0.6010338280379042,0.6087459583104018,0.6165217391304348,0.6243672000805153,0.6322880766171792,0.6402894185437402,0.6483760351966874,0.6565529092071611,0.6648247914560161,0.6731958239630186,0.6816699604743083,0.6902513586956521,0.6989439915458937,0.7077512840420449,0.7166765122873346,0.7257231767180925,0.7348946288159113,0.744193721395881,0.753623188405797,0.7632964827991932,0.7732985109804792,0.7835913482652613,0.7941385869565218,0.8049050930908309,0.8158571105072464,0.8269623588539469,0.8381897993311037,0.8495094138198758,0.8608923169606235,0.8723108619463633,0.8837384259259259,0.8951492072197845,0.9065183423913044,0.9178220169898159,0.9290372670807453,0.9401417913139669,0.951114070842868,0.9619334829867675,0.9725801161919041,0.9830345944816054,0.9932781986919677,1.0032929815948117,1.0130615942028984,1.0225671206881064,1.0317931998396295,1.0407241405973842,1.049344758064516,1.0576402173913042,1.0655961546756383,1.0731987921516604,1.087494075455005,1.0945644335284281,1.101629397610355,1.1086730072463769,1.1156799096927101,1.122635210496431,1.129524330716586,1.1363331202046036,1.1430479659235164,1.1496556494171393,1.1561432104316547,1.1624980590062113,1.1687080827937095,1.1747615106399265,1.1806467818865916,1.186352657004831,1.1918683236506749,1.197183265708755,1.2022871376811595,1.2071698736780259,1.2118217920192589,1.2162334692028987,1.2203956188813705,1.2242991990846683,1.2279355429898409,1.2312960986024843,1.234372562017882,1.237156842251951,1.2396410544603296,1.2418175134149696,1.2436787272268937,1.2452173913043478,1.2464667319993923,1.2474719454508858,1.248243620173713,1.2487920864262991,1.2491274240365613,1.2492594699449975,1.249197825476764,1.2489518633540373,1.2485307344594159,1.2479433743606139,1.2471985096062166,1.24630466380182,1.2452701634754335,1.2441031437406298,1.242811553765528,1.241403162055336,1.2398855615558215,1.2382661745847583,1.236552257598069,1.2347509057971016,1.2328690575831731,1.2309134988652652,1.2288908672264791,1.2268076559546315,1.224670217942127,1.222484769460028,1.2202573938110324,1.2179940448658648,1.2157005504874052,1.213382615846682,1.2110458266347028,1.208695652173913,1.2062845833802658,1.2037658281039891,1.2011457462374582,1.1984305678793257,1.1956263966287797,1.1927392127799736,1.1897748764201441,1.1867391304347827,1.183637603423102,1.180475812526905,1.1772591661758407,1.1739929667519182,1.170682413176034,1.1673326034191642,1.1639485369407687,1.1605351170568563,1.1570971532400665,1.1536393633540374,1.1501663758242324,1.146682731747334,1.1431928869412125,1.1397012139374239,1.1362120039180992,1.1327294685990337,1.1292577420607093,1.125800882528919,1.1223628741066112,1.118947628458498,1.1155589864499311,1.1122007197414807,1.1088765323406122,1.105590062111801,1.1023248037439612,1.0990615380915738,1.0957997899109366,1.0925390922959572,1.0892789864961079,1.0860190217391306,1.0827587550583475,1.0794977511244377,1.076235582081545,1.0729718273875883,1.0697060736586494,1.0664379145173177,1.0631669504448724,1.059892788637194,1.0566150428642895,1.0533333333333335,1.0500472865551147,1.046756535213798,1.0434607180398998,1.0401594796863862,1.0368524706078084,1.0335393469423826,1.0302197703969371,1.0268934081346424,1.0235599326654443,1.0202190217391305,1.0168703582409493,1.013513630089717,1.01014853013834,1.006774756076686,1.0033920103367435,1]
    factorsList2 = [0,0.5225929054054055,0.5447107263513514,0.5663974521396397,0.5876332875844595,0.6084195523648649,0.6287610853040541,0.6486486486486486,0.6680875211148649,0.6870806353228229,0.7056218327702704,0.7237167920761671,0.7413605011261262,0.7585576110966736,0.7753039032335908,0.7916015625,0.8074522276182433,0.8228524940381559,0.8378041127064565,0.8523070768136558,0.8663613809121623,0.8799657637548263,0.893122792536855,0.9058299977967098,0.9180886208474099,0.9298986486486487,0.9412600701663203,0.9521718984609611,0.962635172840251,0.9726498791356012,0.9822151252815315,0.9913318371294683,1,1.0089394259316133,1.0187495342309223,1.0292659568050193,1.0403414889498874,1.0518448399835647,1.0636599284317214,1.0756805483367984,1.0878127639358108,1.099970838311635,1.1120778283864223,1.1240633347737272,1.1358639578854424,1.1474216403903905,1.1586833734209754,1.1696003787198102,1.1801287676836993,1.1902271571635412,1.1998582664695947,1.208987738887785,1.2175833529593296,1.2256155680297043,1.233057031641016,1.239882620546683,1.2460687703607627,1.2515931072931485,1.256435938228099,1.2605777868042831,1.2640011349239866,1.2666893968763846,1.2686270569965128,1.2697993752681254,1.2701931515255491,1.2700631821725572,1.2696814134802417,1.2690589230788625,1.2682065251142687,1.2671340243096358,1.2658508536438227,1.2643661005305482,1.2626879809496998,1.2608246222463904,1.2587833557797663,1.2565712978603605,1.2541953638980263,1.2516615958998771,1.2489765719746189,1.2461457019222546,1.2431744549725507,1.2400680302698532,1.2368315342781808,1.2334695093719474,1.2299865958313223,1.226386749801272,1.222674510675283,1.2188532990156105,1.2149271297220516,1.2108993924138323,1.2067736193224474,1.2025528973771162,1.1982403227361194,1.1938390002906132,1.1893516220259488,1.1847809054943101,1.1801295924831081,1.1753072539356366,1.170239136617485,1.1649502840909092,1.1594647381756757,1.1538057192015654,1.1479951487562932,1.1420546096004986,1.1360044737119934,1.1298644626769627,1.123653678368817,1.1173902619032585,1.1110918046953204,1.104775373674994,1.0984571752149879,1.0921530694545898,1.0858781144425678,1.079647068770928,1.0734739416637034,1.067372369822268,1.0613557472477866,1.055436446061446,1.0496270900137425,1.043939324040427,1.0383847348324888,1.0329744169854256,1.0277189931670914,1.022628955174687,1.0177143499346122,1.0129849028716216,1.0084499259303947,1.0041187495012238,0.9959869480672533,0.9919723923141893,0.9879641240715907,0.9839697985449939,0.9799967414842004,0.9760523554104478,0.972143432494995,0.9682768562450318,0.9644590202086212,0.9606965151292597,0.9569953623250048,0.9533616938646235,0.9498012806689669,0.9463199169680245,0.942922958059677,0.9396158854166666,0.9364039382863468,0.9332922123750463,0.930285574956334,0.9273887617558437,0.9246066470728279,0.9219437112894144,0.9194042287061482,0.9169927952469329,0.9147133691596009,0.912570148654133,0.9105672235996077,0.9087082406174204,0.9069971737013686,0.9054377291898308,0.9040333541826026,0.9027876570418074,0.9016587464065385,0.9006029141120286,0.89962067728196,0.8987127013637113,0.8978795157017814,0.8971217561334868,0.8964398852211118,0.8958345116182032,0.8953061514847873,0.8948552700218602,0.8944824373098429,0.8941880950831829,0.8939727511448408,0.8938368257805219,0.8937808427847491,0.8938051640840947,0.8939103298213468,0.8940966826530711,0.8943646681663332,0.894714722046265,0.8951471974391518,0.8956625122396608,0.896261039151344,0.896943178636347,0.897709251164171,0.8985596057877435,0.8994946546646916,0.9005146958897895,0.9016200561610719,0.9028110900271159,0.9040881446113981,0.9054514567057291,0.9069558915396129,0.9086458977300432,0.9105064048423425,0.9125227173322877,0.9146804045479491,0.9169652940404894,0.9193635645499457,0.9218616052576014,0.9244461418624782,0.9271041302557199,0.9298227833552457,0.9325895648060745,0.9353921828650298,0.9382185844635595,0.9410569175663436,0.9438956532309805,0.9467233884508762,0.9495289688404923,0.952301467107844,0.9550301310117606,0.9577044257202846,0.9603140441478278,0.9628488095881129,0.9652987643405124,0.9676541646638358,0.9699054001993321,0.972043036119917,0.9740578541298757,0.975940757994986,0.9776828450996394,0.9792753429271831,0.9807096503416084,0.9820917499530781,0.9835255150018312,0.9849994349215682,0.9865022300260788,0.9880227888402868,0.9895502074764984,0.9910737922822884,0.9925829984268517,0.9940674691863438,0.9955170460236378,0.9969217222541691,0.9982716747778466,0.9995572323646333,1.0007688932572607,1.001897321625774,1.0029333303640555,1.0038678780042685,1.0046920827491117,1.0053972090037087,1.0059746609993303,1.0064159833063293,1.0067128546288764,1.006857098446775,1.006840658478874,1.0066556144870868,1.0062941729571369,1.0057486629311514,1.0050115352124935,1.0040753607744337,1.0029328259591677,1.0015767342588167,1]
    def newBand1(intensity):
        iO = int( intensity * factorsList1[intensity])
        return iO
    def newBand2(intensity):
        iO = int( intensity * factorsList2[intensity])
        return iO
    def liftBand(intensity):
        iO = int( intensity * 1.2)
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # stretch red channel + lift blue channel
    R = R.point(newBand1)
    B = B.point(liftBand)
    # sharpen image
    temp_img = Image.merge('RGBA',(R,G,B,A))
    temp_img = ImageEnhance.Sharpness(temp_img)
    temp_img = temp_img.enhance(sharpenFactor)
    A2 = temp_img.getchannel('A')
    R2 = temp_img.getchannel('R')
    G2 = temp_img.getchannel('G')
    B2 = temp_img.getchannel('B')
    # change blue according to given curve
    B2 = B2.point(newBand2)
    output_img = Image.merge('RGBA',(R2,G2,B2,A2))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def cremaFilterFunction ( targetImage, inputPathPy, outputPathPy, colorFactor, contrastFactor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    img = img.convert('RGB')
    rgb_img = img.convert('RGB', (
        1.09, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 0.9, 0,
    ))
    R,G,B = rgb_img.split()
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img = ImageEnhance.Color(output_img)
    output_img = output_img.enhance(colorFactor)
    output_img = ImageEnhance.Contrast(output_img)
    output_img = output_img.enhance(contrastFactor)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def junoFilterFunction( targetImage, inputPathPy, outputPathPy, brightnessFactor, saturationValue ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    img = ImageEnhance.Brightness(img)
    img = img.enhance(brightnessFactor)
    img = ImageEnhance.Color(img)
    img = img.enhance(saturationValue)
    A = img.getchannel('A')
    img = img.convert('RGB')
    rgb_img = img.convert('RGB', (
        1.09, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 0.9, 0,
    ))
    R,G,B = rgb_img.split() # add original Alpha
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def kelvinFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [0,0.7684755067567568,0.8062183277027027,0.8429317989864865,0.8786159206081081,0.9132654138513514,0.9468829180743245,0.979473334942085,1.0110325168918919,1.0415610923423424,1.071062077702703,1.0995301942567568,1.1269685212556306,1.1533771602130978,1.1787561836389961,1.2031056447072073,1.2264239336993243,1.2487129247813993,1.269971143018018,1.290198813122333,1.309397434543919,1.3275644506113256,1.3447025683353808,1.3608105813014102,1.3758874841638515,1.3899350717905405,1.402952325071466,1.414939353415916,1.4258967219172298,1.4358235525396088,1.44471996410473,1.4525869115082826,1.459423168285473,1.4658559038441852,1.4724835273002783,1.4792697273166022,1.4861814939939941,1.4931890294010226,1.5002667140825037,1.5073902027027029,1.5145389041385138,1.5216932705380686,1.5288362441682755,1.5359517402576996,1.5430260360680281,1.550045748873874,1.5569992334386016,1.5638752740439907,1.5706644144144146,1.5773568929260895,1.5839445206925677,1.5904197510930047,1.5967751104469854,1.60300443611359,1.609101044403779,1.6150596974815727,1.6208748246712115,1.6265414777441916,1.6320555047908902,1.6374121406894182,1.6426075978322072,1.6476383369793974,1.6525008343777245,1.6571915805314243,1.6617076976879224,1.6663266632016633,1.6712881427236896,1.676535436731041,1.6820151809668127,1.6876772960120447,1.6934741870777028,1.6993613125118958,1.705296238621434,1.711239399180859,1.7171526533395727,1.7230004222972972,1.72874882618021,1.7343659164948229,1.7398210447526856,1.7450852813355289,1.7501313080658787,1.754932992888722,1.7594653175469677,1.7637047874776133,1.7676288698017215,1.771216092011129,1.774445980318982,1.777299078105584,1.779756663179515,1.7818010772139767,1.783415153434685,1.7845827696901917,1.7852882896270932,1.7855168913242883,1.7852542431893332,1.7844868254356332,1.7832014754011825,1.7814920998841948,1.7794739543832736,1.777166126531361,1.7745866765202702,1.7717532759399253,1.768682515235824,1.7653906608747705,1.761893226798012,1.758205135939511,1.7543407481036462,1.7503138862796792,1.7461379225905593,1.7418256173676543,1.737389386901106,1.7328410811571708,1.7281923036317568,1.7234540718989177,1.718637074831822,1.713751629516745,1.7088077541610849,1.7038150680728805,1.6987828085633305,1.693720068791875,1.6886354463594455,1.683537390979241,1.6784340482820808,1.673333218531985,1.6682425567972836,1.6631694203969596,1.658120933084312,1.6531039942424586,1.643147760883158,1.6381308319662813,1.6330760580400892,1.6279848240907813,1.6228585726748248,1.6176986294246674,1.6125063295717592,1.6072829448172323,1.602029685650523,1.596747799196105,1.5914384492195095,1.5861027426701255,1.5807417784930875,1.5753566711449014,1.5699484346945285,1.5645180779534418,1.55906660465692,1.5535949458461564,1.5481040521149338,1.5425948260734341,1.537068157171827,1.531524900144285,1.525965876158521,1.5203919281830658,1.5148038232396,1.509202340562204,1.5035882499182651,1.49796225904014,1.492325089149784,1.4866774536508671,1.481020006500457,1.475353426546664,1.4696503223459534,1.4638869419549758,1.4580692423455377,1.4522030452559793,1.4462940412891587,1.4403477739876314,1.4343696442366534,1.4283649537860963,1.4223388398568688,1.4162963576081828,1.410242415009582,1.4041818154824748,1.3981192513865022,1.3920593166914221,1.3860064862225507,1.3799651424773496,1.373939559594022,1.3679339249301312,1.3619523276631862,1.3559987706823036,1.3500771547442536,1.3441913175342133,1.338344990318027,1.3325418366948811,1.3267854410510067,1.321079301820249,1.3154268470143355,1.3098314404830365,1.304296357427461,1.2988248214613154,1.293419975733106,1.2880849065007391,1.2827957809313626,1.2775270808005472,1.2722793208999263,1.2670529928907004,1.2618485826379005,1.2566665620254487,1.2515074058863256,1.246371560998865,1.2412594816642086,1.2361716050211045,1.2311083616262555,1.2260701715725089,1.22105745077919,1.2160706050875807,1.2111100285120804,1.2061761154206527,1.201269246713936,1.196389796037318,1.1915381338618638,1.186714619778055,1.1819196104957979,1.1771534522033213,1.1724164846481429,1.1677090470139329,1.1630314646302904,1.1583840625326893,1.1537671560536753,1.1491810566670186,1.1446260711419871,1.1401024979339889,1.1356106329189621,1.1311507648482746,1.126717542127088,1.1223054578845453,1.1179145643123205,1.1135449108776747,1.1091965497855552,1.1048695278503922,1.1005638946465364,1.0962796975604197,1.0920169827224844,1.0877757963558135,1.0835561830192686,1.0793581873902038,1.0751818525218844,1.0710272220435697,1.0668943371288004,1.0627832395536407,1.0586939699729756,1.054626568369709,1.050581074068589,1.0465575257496968,1.0425559616720093,1.038576419053301,1.0346189349260382,1.0306835453096637,1.0267702860590509,1.0228791923522949,1.0190102984988165,1.015163638621428,1.0113392461506352,1.0075371540665856,1.0037573947057437,1]
    factorsListG = [0,0.5295344172297297,0.5581846494932433,0.5859287021396397,0.6127731735641893,0.6387246621621622,0.6637765695382883,0.6879298383204634,0.7111849398226352,0.733542135885886,0.7550015836148649,0.7755657824017199,0.7952298001126127,0.8139963130197506,0.831867232746139,0.8488386824324325,0.8649127032305743,0.8800877508942767,0.8943670232732733,0.9077474884423898,0.9202306798986488,0.9318153253700129,0.9425027833230959,0.9522918808754407,0.9611838400900902,0.9691786317567568,0.976274200883576,0.9824736846221221,0.987774116192085,0.9921774886416589,0.9956828899211713,0.998290377070619,1,1.0011989084254709,1.0022877024542927,1.003287509049228,1.0042171077327327,1.0050925344685901,1.0059291790762803,1.0067394994152807,1.0075360272381757,1.0083294279416612,1.0091290369610684,1.0099439351233501,1.0107823777257372,1.0116512997372373,1.0125573199728262,1.0135067747268545,1.0145054722691442,1.0155579387582736,1.0166693940033784,1.0178438721350027,1.0190858583192568,1.0203985032349567,1.0217857017173424,1.0232503455159705,1.024795591140806,1.0264241420697013,1.0281385153337605,1.0299412809923272,1.0318343978744369,1.033819912702149,1.035900165853858,1.0380767206939083,1.0403512490762248,1.0427234927234927,1.0451850110053236,1.0477258975393304,1.0503366346010534,1.0530086387338427,1.0557332513875484,1.0585028594285306,1.0613099060975038,1.0641474294821363,1.0670088439896823,1.069887915259009,1.0727785634112732,1.0756751957923834,1.0785723373614,1.081465124390609,1.0843487713788007,1.0872184032991326,1.0900698657403594,1.0928988865088736,1.095701553953507,1.098474140500795,1.1012130919527814,1.1039148658356632,1.1065762306607034,1.1091941001746128,1.11176537865991,1.114287396513959,1.116757169873678,1.1191722689171026,1.121530226827559,1.1238284028271692,1.12606481603674,1.1282849124494985,1.13053187913679,1.1328003696167759,1.1350848553631758,1.1373801574625368,1.1396814294763513,1.1419837569289557,1.1442826681474143,1.1465737361245174,1.1488528254079553,1.1511157084727834,1.1533584365615617,1.155577326896851,1.15776871064957,1.159929051200694,1.1620549382390204,1.164143082172327,1.1661905403553225,1.1681938987220917,1.1701505435257455,1.172057499205937,1.1739120029059782,1.175711384638315,1.177453173388232,1.1791347616986823,1.1807539521142556,1.1823082431230774,1.183795426758664,1.1852134184966217,1.1865599905150686,1.1878331929832147,1.1902002270257177,1.1913847798369284,1.1925790014280742,1.1937772233792743,1.1949740469734302,1.196164234649178,1.1973425574011511,1.1985041340887073,1.1996441297593214,1.2007578017895615,1.2018407339162456,1.2028884003981661,1.2038964974781963,1.204860935566949,1.2057776471838972,1.2066426320118948,1.2074520910997206,1.2082022843825204,1.2088896184529556,1.2095105524390524,1.2100616405258027,1.2105395287865992,1.2109409521405718,1.2112628182510226,1.2115019862463567,1.2116554396827834,1.2117202825305144,1.2116936084221241,1.2115727111217507,1.2113548693818423,1.2110373889145631,1.2106177252692145,1.2101177416012674,1.2095617345861487,1.2089506543665023,1.2082855083789965,1.2075672396473178,1.20679680822106,1.205975170910291,1.2051031831915622,1.2041816998153387,1.2032116330484897,1.202193758056988,1.20112894706798,1.2000179377184719,1.1988615644537317,1.1976605483832048,1.1964156504638073,1.1951275958161554,1.193797093266019,1.192424817368215,1.1910114826740805,1.1895577332609284,1.1880642171779867,1.1865315683094726,1.184960424689933,1.1833513748915723,1.1817050125667503,1.1800219363121478,1.1783026968904993,1.1765478857764013,1.1747579951713638,1.1729336106087271,1.171075219506616,1.169183384652666,1.1672586232182973,1.1653014925231724,1.1633124711825187,1.1612920615878808,1.1592407559814788,1.1571590367112166,1.1550473517340583,1.1529061811271977,1.1507359627960263,1.1485371422694632,1.1463101482542974,1.1440554091391315,1.1417733369865808,1.1394643358966983,1.137128810129146,1.1347671483137407,1.13237973953306,1.1299669576757037,1.1275291695757705,1.1250667429230508,1.1225800308262228,1.1200693874970538,1.1175351529508024,1.1149776685370028,1.11239725420796,1.1097942429031398,1.1071689502612965,1.1045216936725153,1.1018527736622021,1.0991624964611297,1.0964511591495234,1.0937190608577327,1.0909664771739902,1.088193671563393,1.0854008956337609,1.0825884001997614,1.0797564281279837,1.0769052180795344,1.074035009933429,1.0711460341407202,1.0682385189755186,1.0653126905813104,1.0623687695211848,1.0594069708955645,1.0564275096552822,1.053430593702624,1.0504164309115025,1.0473852239944375,1.0443371714612644,1.0412724702512843,1.0381913140752859,1.0350938909565357,1.0319803883756447,1.0288509907770997,1.0257058783833006,1.0225452289355639,1.0193692169189452,1.0161780156808893,1.0129717937716596,1.0097507185029775,1.0065149537399238,1.0032646612319986,1]
    factorsListB = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.00024873950655200655,0.0009346432829888712,0.00197574806949807,0.003296265015015015,0.004832878697954712,0.006524771070412518,0.008320745625433125,-0.010172745988175675,-0.012037404210613053,-0.013876111044079795,-0.015653848797925835,-0.017339383062039315,-0.018902496246246247,-0.020317319697414807,-0.02155906321880391,-0.022605552329673425,-0.023435884066464425,-0.02403241131756757,-0.024376800973767886,-0.02445314530275468,-0.024246239163691993,-0.023743470032532535,-0.022931223126535626,-0.021798270089285716,-0.02033278138335704,-0.01852510848671948,-0.0163658096655978,-0.013845632742117118,-0.010956797601905184,-0.0076907489646904975,-0.00404073157979408,0,0.003914777156964658,0.007251036547911548,0.010108347620008068,0.012578870230524643,0.014750951698981591,0.016706759773166026,0.018524948253711458,0.020278701553115615,0.02203827864679748,0.023869070717677136,0.025833333333333333,0.027990740020448084,0.03039717883467884,0.03310533339830215,0.036165888000342115,0.03962699271537162,0.04353441983650317,0.04793074324324324,0.052858075036633013,0.05835495093307594,0.06445964576709062,0.07120711963780642,0.0786316354069587,0.08676589853347666,0.09564114456802308,0.10528634102852853,0.11573063233219483,0.1270007482006463,0.13912255249200814,0.15212137004025303,0.16602034806187768,0.1808430439717061,0.19675026992198386,0.21381036050399893,0.23190946628446632,0.25093776393581085,0.27079056353692804,0.29136676313261795,0.3125691870572029,0.33430477784725837,0.3564835203507079,0.3790191697077384,0.40182870516544583,0.4248316920436061,0.4479513738222167,0.47111330524416467,0.49424572376430487,0.5172796654425073,0.5401483739685482,0.5627877826428402,0.5851355941539366,0.6071318869044152,0.6287190134846385,0.6498408332856161,0.6704433145724507,0.6904744466145833,0.709883501786911,0.7286216320059815,0.7466416850348825,0.7638978168251418,0.7803458614864865,0.7959429504839662,0.8106474615609705,0.8375941575659962,0.8505327442827443,0.8632324923922015,0.8756911319167179,0.8879062627006706,0.8998756547183845,0.911597241773023,0.9230687273325716,0.9342882672247979,0.9452537838449864,0.9559632593756078,0.9664150164394306,0.9766071444616159,0.9865377866863344,0.9962053228654791,1.0056080861134573,1.014744455527726,1.0236128094195438,1.032211615114796,1.040539381362993,1.0485946569472155,1.0563760293496622,1.0638821234702212,1.071111600395626,1.0780631130901122,1.0847354351993024,1.09112728687609,1.0972375056847714,1.1030649167778448,1.1086082915267919,1.113866556710012,1.1188386659364444,1.1235561809504575,1.1280544867784452,1.1323381441976872,1.1364115222787574,1.1402789641559172,1.1439445890614826,1.1474125360975684,1.1506867672639156,1.1537712288726412,1.156669696753279,1.1593858969989725,1.1619234690495366,1.1642859300548742,1.166476811115399,1.168499449505309,1.1703571628879859,1.1720531939513668,1.1735907125139975,1.17497281756049,1.1762025025513796,1.1772827494762115,1.17821643853138,1.179006423014972,1.179655440405589,1.1801662046601078,1.1805413713707409,1.180783539325589,1.1808952344704662,1.1808789292920152,1.180737096317123,1.1804720871988645,1.180086221780863,1.1795562500547019,1.1788620968720616,1.1780107631670131,1.1770090901647823,1.1758637969296628,1.1745814667872774,1.173168534156212,1.171631329510663,1.1699760327243638,1.1682087176299716,1.1663353302526087,1.1643617000286708,1.1622935506962757,1.1601364948529955,1.1578960207022582,1.1555775267666442,1.1531863003549117,1.1507275359204072,1.1482063177164223,1.145627645738632,1.142996418341482,1.1403174461755947,1.137595450391116,1.1348350608909692,1.1320408222342446,1.1292172069440787,1.1263685907888572,1.123499277475718,1.1206134890845225,1.1177153827675597,1.1148090226161034,1.1118984148769306,1.1089480636642501,1.105922860467414,1.10282726994099,1.099665680221044,1.0964423991932324,1.093161665202588,1.089827637847047,1.086444410340095,1.0830160003155902,1.079546362017065,1.0760393771171022,1.0724988658658638,1.068928581426592,1.0653322147505409,1.0617133941529604,1.0580756900546786,1.0544226101940224,1.0507576073124016,1.0470840751945794,1.0434053524120435,1.0397247242914402,1.0360454210630488,1.032370621897953,1.0287034538588322,1.0250469943955112,1.0214042713062184,1.017778264137417,1.0141719055503082,1.0105880815342774,1.0070296324778425,1.0034993545429127,1]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    output_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    output_img.close()


def xproiiFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [0,0.3125,0.3271484375,0.3414449605855856,0.35536977407094594,0.3689241976351352,0.3821086711711712,0.3949196126930502,0.4073651288006757,0.4194379926801802,0.4311391469594595,0.4424715909090909,0.45343292511261263,0.46402351871101877,0.4742455206322394,0.48409522804054056,0.49357646220439194,0.5026874875794913,0.5114269542980481,0.5197965749466572,0.5277963999155405,0.5354252131595882,0.5426844191492629,0.549572883005288,0.5560907587274775,0.5622381756756757,0.5680162584459459,0.5734240099474475,0.5784605755308881,0.5831279488000933,0.5874243384009009,0.5913507383391456,0.5949063687711149,0.5982025171478297,0.6013668769872814,0.6044250723938225,0.6073991471940691,0.6103087620982469,0.6131708137002134,0.6160024958853084,0.6188166437922298,0.6216274153345419,0.6244457347972974,0.6272821240571967,0.6301467483108109,0.6330482826576577,0.6359940740672738,0.6389919673663025,0.6420480539132883,0.6451695437465528,0.6483609586148649,0.6516285357048226,0.6549765097128379,0.6584090447316421,0.6619309739426927,0.6655458192567567,0.6692570866765203,0.6730682676920342,0.6769821579391893,0.6810015871936556,0.685129416525901,0.6893683193952149,0.6937201582252616,0.6981875150820464,0.702772398252745,0.7074740530795218,0.712282572878276,0.7171860818374345,0.7221730145816773,0.7272332412235606,0.7323564566240348,0.7375334938261325,0.7427555118595158,0.748013973412625,0.7533009809852083,0.7586090582770271,0.7639309488353486,0.7692602873266936,0.7745901888968296,0.7799149525316456,0.7852286673880913,0.7905258774399401,0.795801231872116,0.8010499557351026,0.8062671872486327,0.8114484486784579,0.8165894705570396,0.8216861797141971,0.8267346881238484,0.8317311342241118,0.8366718280780782,0.8415536770028957,0.8463732924500588,0.8511275735160564,0.8558134108593302,0.8604279649715506,0.8649685146572353,0.8694679598251602,0.8739598774476007,0.8784430293219356,0.8829159628378379,0.8873774135753948,0.8918262960800875,0.8962614389267909,0.9006815888529757,0.9050857917068855,0.9094728803464432,0.9138421012645239,0.9181922400916542,0.9225226113082693,0.9268320744394963,0.9311198867786706,0.9353853321443654,0.939627369349438,0.94384545678491,0.948038727416275,0.9522065716376399,0.9563481750981752,0.9604628628893724,0.9645500936861232,0.9686091242609798,0.9726394540847666,0.976640382698272,0.980611554294386,0.9845521988407258,0.988461887668919,0.9923401009826792,0.9961862314455204,1.003854076642049,1.007811180320946,1.0118563592815144,1.0159750148763822,1.0201530867392299,1.0243767372491428,1.028632734296797,1.0329080408821045,1.0371902896281318,1.0414670891169704,1.0457268317525035,1.0499578174016653,1.0541490522270942,1.058289573271555,1.0623688626618315,1.066376694687852,1.0703030347157503,1.0741382586166004,1.0778728694814075,1.0814977162418964,1.0850038492115228,1.0883826013513513,1.0916254915149006,1.0947242617437545,1.0976709131006006,1.10045761156601,1.103076725288797,1.1055208604036728,1.107782769396088,1.109855388232873,1.1117319135910675,1.113405547270904,1.1149189635093169,1.1163214809861945,1.1176165980973305,1.118807768145909,1.1198982407478502,1.120891266713815,1.1217900980134328,1.1225977128076738,1.123317213987286,1.123951514991554,1.1245034611091353,1.124975908184711,1.1253716078908569,1.1256932107214974,1.1259433442929536,1.1261245765029946,1.1262394172178005,1.126290319902065,1.1262796463319116,1.1262097607861767,1.1260829388392193,1.1259014423076923,1.125667429484428,1.1253830476036923,1.1250503974730643,1.1246715347214655,1.124248453364377,1.123783122540343,1.1232774697130168,1.1227333644036719,1.12215265425459,1.1215371484155054,1.1208882424664788,1.1202056536139071,1.1194887157289501,1.118736725779311,1.117949011754656,1.1171248985580042,1.1162637578199275,1.1153649407464106,1.1144278278686803,1.1134518283173334,1.1124363141090985,1.1113807180917132,1.1102844680856543,1.1091469950139194,1.1079677487652395,1.106746189807408,1.1054817731485598,1.1041739955985561,1.102822332234393,1.1014262913806532,1.0999853828506654,1.0984991102033144,1.0969670015787045,1.0953886091291487,1.0937634552530282,1.0920911013799244,1.0903711094174227,1.0886030417402488,1.086786476108196,1.084920997888989,1.0830061924903989,1.0810416674521899,1.0790346767666104,1.076992824128358,1.0749162141872823,1.0728049569923543,1.0706591534668026,1.0684789063647548,1.0662643166610453,1.0640154835895634,1.0617325046806128,1.0594154757973118,1.0570644841514971,1.0546796329514019,1.0522610027823511,1.0498086884702413,1.0473227763518373,1.0448033513249577,1.0422504985895316,1.0396643036413544,1.0370448454775305,1.034392206870617,1.0317064650336223,1.0289876992769018,1.0262359859567984,1.023451401029552,1.02063401840311,1.0177839108028928,1.01490115102762,1.0119858090839688,1.0090379550943211,1.0060576574679105,1.0030449835408852,1]
    factorsListG = [0,0.3420080236486487,0.3590450802364865,0.3756070523648649,0.3916939400337838,0.40730574324324326,0.42244246199324326,0.4371040962837838,0.45128734691722977,0.4649991788663664,0.47823057432432436,0.4909877917690418,0.503270604588964,0.5150768256237007,0.5264067778716217,0.5372589386261262,0.5476371146537162,0.5575395593203497,0.566966380442943,0.5759162740042675,0.5843908361486487,0.5923901021557272,0.5999129011824325,0.6069594135575793,0.6135308892877253,0.6196262668918919,0.6252456633316008,0.6303891782407407,0.635055954391892,0.6392479831663561,0.6429634712837838,0.6462034110723628,0.648967846019848,0.6514191748566749,0.6537395046701113,0.6559528836872588,0.6580821544200451,0.6601469765796202,0.6621642458659318,0.6641511553620929,0.6661211993243243,0.6680865554960449,0.6700607555099742,0.6720523894170334,0.674072265625,0.6761290587462463,0.6782301153055229,0.6803832797225416,0.6825946429828266,0.684871414782129,0.6872186444256756,0.6896412439553524,0.6921442551325364,0.69473258820436,0.6974098121559059,0.7001799562346438,0.7030465262276786,0.7060127819019677,0.7090819857438257,0.7122567317052222,0.7155398807010136,0.7189338897042534,0.7224412700250654,0.7260639545795796,0.7298039616765203,0.733635776702183,0.7375288329878175,0.7414776308491328,0.7454777703944755,0.7495245330248728,0.7536136583011583,0.7577411258089075,0.7619029552012951,0.7660955650106442,0.7703155673621257,0.7745597550675676,0.7788250897381758,0.7831085194366445,0.7874074871145184,0.7917192310981868,0.7960412927576014,0.8003713348765432,0.8047071342493408,0.8090464158152881,0.8133871699545528,0.8177274816176471,0.8220656782782055,0.8263997092458839,0.8307279169705928,0.8350488666774218,0.8393610407282283,0.8436626981548857,0.8479526040136605,0.8522294345757048,0.8564917820496694,0.8607385757467995,0.8649685146572353,0.8692149079653108,0.8735072813965113,0.8778398426835927,0.8822063714104731,0.8866011548367675,0.8910188336314255,0.8954541284685779,0.8999018361811331,0.9043572031853283,0.9088155307798955,0.9132721725814601,0.9177230208724351,0.9221636343912721,0.9265902132601351,0.9309987378637083,0.9353853321443654,0.9397466076073309,0.944078947368421,0.9483789751028203,0.9526435446761417,0.9568693919279858,0.9610534751846657,0.9651929659110267,0.9692849099099099,0.9733266687723364,0.9773155824241251,0.9812489700065921,0.9851244499918266,0.9889396114864866,0.9926920153970936,0.9963796111872207,1.0036188873284624,1.007296302462318,1.0110217378339694,1.0147851042626435,1.0185767152255638,1.0223870748663777,1.0262068709334335,1.0300273561705087,1.0338396534079701,1.0376355253011165,1.04140668672832,1.0451452306798987,1.0488434744585011,1.0524938123780692,1.0560890822121292,1.059622091573996,1.0630860285123487,1.0664741321212052,1.0697799152388996,1.0729970214487081,1.076119264975966,1.079140668989302,1.0820553275880394,1.0848576205214262,1.0875419019663046,1.0901028441311644,1.0925351715753053,1.0948337441257363,1.0969935945972844,1.0990097980323086,1.1008775948708143,1.1025924270217484,1.1042003826905322,1.1057500778773566,1.1072406012943543,1.1086711443484263,1.1100408780584563,1.1113489934187766,1.1125947403124494,1.1137772686539777,1.1148958656095076,1.1159498739318363,1.116938458812431,1.117860996670726,1.1187168020621778,1.1195052052995884,1.1202255520028959,1.1208772026643121,1.1214594949491337,1.1219719296851276,1.1224137976794881,1.1227845887880068,1.123083713002324,1.123310611408756,1.123464755338715,1.1235456096859853,1.123552633080716,1.1234853490082826,1.1233432382185828,1.1231258276072367,1.122832636626582,1.1224631774815523,1.1220170244125425,1.1214937089799761,1.120897610136448,1.1202346321333416,1.1195065990720288,1.1187153146599644,1.1178625292339055,1.116949991095499,1.1159793636680022,1.1149523100981842,1.1138704440214469,1.1127353797853392,1.111548651170991,1.110311810403004,1.1090263472313777,1.1076937224789263,1.10631537670908,1.1048927307128906,1.103427170196419,1.1019200623265566,1.1003727248983286,1.0987864819672082,1.0971626094899918,1.0955023749906265,1.0938070070661141,1.092077719198691,1.0903157177059333,1.0885221565032817,1.0866981910273394,1.0848449482085958,1.0829635345806072,1.0810550367393894,1.0791205217904458,1.0771610451481057,1.0751811039555181,1.0731837106817392,1.0711677007156264,1.0691319226427292,1.0670752487623831,1.0649965638139414,1.06289478256031,1.0607688278098697,1.058617647943385,1.0564402022684494,1.054235478335924,1.0520024738669997,1.049740203498965,1.047447696697054,1.0451240077973707,1.04276819658709,1.0403793453033883,1.0379565479448127,1.0354989151206329,1.0330055703301317,1.0304756547493363,1.027908319327837,1.02530273126948,1.0226580695474055,1.0199735296363877,1.0172483157596073,1.0144816476972442,1.011672755977413,1.0088208843125657,1.005925287919289,1.0029852336970473,1]
    factorsListB = [38.019874366554056,38.40770164695946,19.41988888302365,13.104624155405405,9.956945470861488,8.075857791385136,6.827693904842342,5.940884034145753,5.279646589949325,4.7685400243994,4.362307326858108,4.032141383215602,3.758844049127253,3.529118210758836,3.333471585424711,3.164937887105856,3.018296525285051,2.889553731120827,2.7756017736486487,2.6739899593261027,2.582756413640203,2.500312324042793,2.4253583528485874,2.3568211341436545,2.2938067461993246,2.23556323902027,2.1814548547946986,2.1309405108233235,2.0835550079934846,2.0388991328343433,1.9966255806587838,1.9564327116935485,1.9180553539379224,1.8816191902129404,1.8472793651877981,1.8148588320463321,1.7841991161082957,1.7551599451013513,1.7276154649715505,1.7014527297730422,1.6765697582347976,1.652875162223962,1.6302859430300838,1.6087262089487746,1.5881281672297298,1.568429464620871,1.5495725961185371,1.5315057931102645,1.5141816010346283,1.497555631205185,1.481587837837838,1.4662407984731056,1.451480476871102,1.4372751565687152,1.4235952260854605,1.4104134674447175,1.3977048424680263,1.3854453754741585,1.373613654400629,1.3621890478269585,1.3511522997606984,1.3404858495790872,1.3301730567513077,1.320198337288181,1.310546875,1.3012045624350312,1.2921565475276413,1.2833886679356596,1.2748870121845193,1.2666392402932827,1.2586333403716217,1.250857791385135,1.2433020789344031,1.2359560839735284,1.2288102344320673,1.22185546875,1.2150833759334994,1.2084856391497016,1.2020547064492377,1.1957832412119398,1.1896642736486487,1.183691178157324,1.177857813272495,1.1721578565105015,1.16658607198158,1.1611366939089824,1.1558046850447832,1.1505850880514137,1.1454731709248311,1.140464562613878,1.1355546464433184,1.1307397337670777,1.12601557909812,1.121378687154897,1.11682514982569,1.1123516402916074,1.1079549703512106,1.1036278657442882,1.0993650997138722,1.0951663222171035,1.091031197212838,1.0869592713071983,1.0829504970273582,1.079004188123196,1.075120319199909,1.0712984887789576,1.0675384350299593,1.0638400292450747,1.0602027809059058,1.0566265807091495,1.053111083384521,1.0496561938839177,1.0462617027253258,1.0429272910562666,1.039652766973388,1.0364379452482375,1.0332826470395504,1.0301866996202935,1.027149936118587,1.0241720843742903,1.021253101245777,1.0183927268888207,1.0155908181490918,1.0128473438186663,1.0101620608448671,1.0075347339527028,1.0049654495455278,1.0024538756583847,0.997600127834957,0.995249561460499,0.9929465673032287,0.9906894643222769,0.9884766220343935,0.9863064586274709,0.984177439157908,0.9820879767922794,0.9800367236819393,0.9780222754174012,0.9760432680038403,0.9740982821549228,0.9721861260362756,0.9703055484511801,0.9684552409161784,0.9666341145833334,0.9648410196295435,0.9630747473447335,0.9613342116829839,0.9596184451184716,0.957926328961092,0.9562569503096847,0.9546092456539735,0.9529822662917852,0.9513751314503843,0.9497869403875264,0.9482167730356365,0.9466637752160213,0.9451271565404976,0.9436060631067182,0.9420997454928395,0.940607349292652,0.9391232052364865,0.9376430466925259,0.9361682981030303,0.9347002284654129,0.9332402759648855,0.9317896453847485,0.9303496706966137,0.9289215755585386,0.9275065156225012,0.9261057357909381,0.9247203360844397,0.9233514676672494,0.9220002169460828,0.9206676832746001,0.9193548654681467,0.9180628146234837,0.9167925580837724,0.9155450630361752,0.9143212381921901,0.913122045385229,0.9119484616479394,0.9108012975200475,0.9096814539949787,0.9085897766185004,0.9075271639883127,0.9064943534764605,0.9054922078244688,0.9045215012219667,0.9035829565614723,0.9026773857019026,0.9018054798601777,0.9009679845861487,0.9001652197149385,0.89939583188214,0.8986580555916495,0.8979501950431777,0.8972706223633214,0.8966176092640937,0.8959896279857905,0.8953850163640203,0.8948023094514759,0.8942399733137376,0.8936965042416956,0.8931704603558063,0.8926603957234673,0.892164924519483,0.8916826558215825,0.8912122889021082,0.890752484785174,0.8903019299991957,0.8898593359725246,0.889423531819703,0.888993213751824,0.8885672256843584,0.8881443716609052,0.88772350842053,0.8873034833688817,0.8868832255958653,0.8864615933624121,0.8860375256737562,0.8856099508816652,0.8851778760918858,0.8847402966307114,0.8842961373936716,0.883903053444069,0.8836114897564877,0.8834100471875372,0.883287454227974,0.8832326650647646,0.8832347972972974,0.8832832140937611,0.8833673909125991,0.8834770546893125,0.8836020374716664,0.8837324005355089,0.8838583596299888,0.8839702677979602,0.8840586679403604,0.8841142612359352,0.8841278900971284,0.8840905626191544,0.8839934218907053,0.8838277567932517,0.8835850260560895,0.8832568009256069,0.882834789701096,0.8823108483174787,0.8816769507623488,0.8809252132050162,0.8800478647592906,0.87903727152202,0.877885907671064,0.8765863794099189,0.8751313963908545,0.8735138085005962,0.8717265257964264]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def amaroFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [19.0140941722973,19.72994087837838,10.261995882601353,7.130832981418919,5.582935230152027,4.667604518581081,4.0679326787725225,3.6481094654922783,3.340226456925676,3.1065538194444446,2.92445629222973,2.779532017813268,2.662177558417793,2.5657423499220378,2.4854807025217185,2.4179080447635135,2.36041259765625,2.3109971184419713,2.268109662396772,2.2305215371621623,2.1972530880489867,2.1675100044240674,2.140642395769349,2.1161133960047005,2.0934750668637387,2.072352195945946,2.052426788266632,2.0334279592092095,2.0151235219594597,1.9973133154706433,1.9798238668355856,1.9625040867480386,1.945221772065034,1.9284685964373465,1.9127517481866059,1.8979857927123553,1.8840929552599475,1.871004582496348,1.8586599423230799,1.8470031780578655,1.8359853383657097,1.825561282032795,1.8156907954271237,1.806336791915462,1.7974661562308045,1.7890484234234236,1.7810557776696536,1.7734627704499715,1.7662463488879505,1.7593848033301158,1.752858688766892,1.7466495677662957,1.7407411825136436,1.7351175062149415,1.7297646767861612,1.7246691204699018,1.7198187043768098,1.7152019155257232,1.7108078074033086,1.706626622981562,1.7026490357545045,1.6988665471311475,1.6952707811137753,1.6918543124597814,1.6886097676045186,1.6856688945556133,1.683135661407146,1.6809646341770876,1.6791130514705883,1.6775408220720722,1.6762093915902512,1.6750834929339553,1.6741287185623124,1.6733132693909665,1.6726068868699782,1.6719807502815316,1.6714079030716573,1.6708622748661814,1.670319808991684,1.669756998642234,1.6691518422719596,1.6684834248310811,1.6677318515161503,1.6668780273119506,1.6659040806990026,1.6647926706577902,1.6635274161788969,1.662092689402765,1.6604734228635598,1.6586554487027407,1.6566250087978605,1.6543691673086207,1.6518754073791861,1.6491318214636008,1.6461269385242958,1.6428497705147582,1.6392899246903154,1.6355026045294652,1.631558064262445,1.6274683330347393,1.6232449588260136,1.6188989016089108,1.6144408856236752,1.6098810264489307,1.6052291774948027,1.6004948168034108,1.5956870025058962,1.590814454111676,1.5858856292816255,1.5809086753037442,1.5758912632447788,1.570841084961651,1.565765380859375,1.5606710766525653,1.5555650286902858,1.5504536827078437,1.5453434328219655,1.5402402853574728,1.5351502107907695,1.530078812563877,1.525031562324043,1.5200138599019992,1.515030819914433,1.5100873906490333,1.5051884139841707,1.5003385240709461,1.4955422079445517,1.490803863272106,1.4814810154449507,1.4768292781964658,1.4721737108649682,1.4675157001817158,1.4628563927237859,1.4581970978090966,1.453538890452953,1.448882911087788,1.4442303150122067,1.4395821762234382,1.4349394428713786,1.430303224541506,1.4256744589503068,1.4210541038672917,1.4164430671999033,1.4118422774581223,1.407252592031687,1.4026748674174496,1.398109936806226,1.3935586108701608,1.3890216563761224,1.3844998416385135,1.3799939146190374,1.375504603596195,1.3710325962451424,1.3665786052260662,1.362143282237631,1.357727262268278,1.353331227170393,1.3489557580102849,1.3446014627355836,1.340268934095228,1.3359558607520565,1.3316590516297548,1.3273776811344513,1.3231110242769448,1.3188583336532556,1.3146188798691387,1.3103919707565443,1.306176891351452,1.3019730021777047,1.2977796205845091,1.293596118476618,1.289421863184269,1.2852562557364084,1.2810986919705267,1.2769485815335426,1.272805366234932,1.2686684632195755,1.264537358334678,1.260411493623075,1.2562903785132788,1.2521734603647157,1.2480602711925954,1.2439503352129027,1.2398431331934856,1.2357382373795882,1.2316351671338048,1.2275334873852797,1.223432754771061,1.2193325440395753,1.2152324388919142,1.2111320317474707,1.2070309063335798,1.2029119196967775,1.198760960818865,1.1945821760763167,1.1903795935603971,1.1861571846945096,1.1819188406712822,1.1776683413106497,1.1734094403241133,1.1691457838946107,1.164880946003437,1.1606184464608158,1.1563617279748155,1.1521141660787122,1.1478790707614472,1.1436596800817462,1.1394591936202654,1.1352807102575813,1.1311273169793679,1.1270020109782286,1.1229077328959636,1.1188473836402424,1.1148238021877566,1.1108397670244736,1.1068980204569805,1.1030012466405958,1.0991520729131152,1.0953531012216733,1.0916068562125691,1.087915831765642,1.0842824842565857,1.0807092186032377,1.0771983967784748,1.0737549854542043,1.070379213863684,1.067066343870457,1.063811738550974,1.0606108311707503,1.0574591344167708,1.0543522422489708,1.0512858210383236,1.0482556150927786,1.0452574379423745,1.042287177885998,1.0393407894174713,1.0364142987893699,1.0335037955743953,1.0306054416938186,1.0277154492902327,1.0248301070648498,1.021945761654402,1.0190588130448157,1.0161657303796177,1.0132630337159148,1.0103472996952507,1.0074151637374422,1.0044633138668257,1.001488491312166,0.9984874877929687,0.9954571510857962,0.9923943724564758,0.9892960972108975,0.9861593171367495,0.9829810695921105,0.979758443059148]
    factorsListG = [0,0.7748891469594595,0.8187288851351352,0.8611169763513514,0.9020600190033784,0.941554054054054,0.9795933628941441,1.0161792652027029,1.0513157200168919,1.0850019941816818,1.117237647804054,1.1480200015356266,1.1773494686092343,1.2052303956600832,1.2316583464044402,1.2566353462837838,1.280159615181588,1.3022328969594594,1.3228550816441442,1.3420260824146515,1.3597458298141893,1.376013010778636,1.390828950399263,1.4041935957696827,1.416106902801239,1.4265688344594596,1.4355788518386174,1.443137962180931,1.4492451435810811,1.4539008802714353,1.457105152027027,1.4588579412325633,1.4591592324746623,1.458622862919738,1.457890593948728,1.4569988236003861,1.4559806388419672,1.454866263011322,1.453681696190434,1.4524509485446988,1.4511946394636825,1.4499326641809493,1.4486823947273166,1.44745928022863,1.446277665271806,1.4451512058933935,1.4440915099882492,1.4431091975452848,1.4422148283537446,1.441417292212493,1.4407250316722975,1.4401458271230791,1.4396871142476613,1.4393555185492097,1.439156930367868,1.439097291538698,1.4391821194799712,1.439415849854789,1.4398032950110673,1.440348717361429,1.4410563151041667,1.4419295784642225,1.4429719853421972,1.444187002292471,1.4455776730099241,1.4471998440748441,1.4490845826295047,1.4511986625151272,1.453511006123311,1.4559925287039759,1.4586152419160232,1.4613532918371717,1.464182077585398,1.467077984716309,1.4700193885819943,1.4729852899774776,1.4759557949190967,1.478912385650667,1.4818371556652807,1.4847132721625897,1.4875247439822634,1.490256369650901,1.4928935282939189,1.4954224626546728,1.4978302276886262,1.5001040217607315,1.502232099013985,1.5042029502562908,1.506005889367706,1.5076304139462497,1.5090666349943695,1.510304953176047,1.511336473404451,1.5121525412761554,1.512744589877444,1.5131048297475107,1.513225658519848,1.5132184223930762,1.513194837954185,1.513148269007644,1.5130722788217907,1.5129607509156746,1.5128078086703431,1.5126077396229665,1.5123551779130393,1.512044773568211,1.5116715029999044,1.5112305304172458,1.5107171380364741,1.510126841739245,1.5094553204660628,1.5086983494262844,1.5078519725431347,1.5069121985993184,1.505875292181573,1.504737590426704,1.5034956705425793,1.5021461703590613,1.5006857298406722,1.4991112127917046,1.4974195875563063,1.495607868166462,1.4936732747251606,1.4916130104475664,1.4894243687677093,1.487104782516892,1.48465171365562,1.4820628079943872,1.4764856210225488,1.4735327199194388,1.470481751357154,1.4673373435580466,1.4641038863258231,1.4607858353922953,1.4573873678365865,1.453912586400164,1.4503654258729535,1.4467498026219154,1.4430693779013952,1.4393278497526545,1.435528764510854,1.431675522146817,1.4277714967412234,1.4238198999170069,1.4198239002067803,1.415786601931287,1.4117109576093951,1.4075998845459163,1.4034561995864887,1.399282688450169,1.395081997515158,1.3908567469286206,1.3866094883371425,1.3823426856874121,1.378058781910691,1.3737600727041646,1.3694489003459074,1.365127443410826,1.3607979294152643,1.356462468327703,1.3520818469867384,1.3476204475960336,1.3430856063658079,1.338484440340207,1.3338239140241093,1.329110863852369,1.3243518834901986,1.3195534488869451,1.3147219217588058,1.3098634365063593,1.3049840419160939,1.3000896269236626,1.2951859443043567,1.2902786145857605,1.2853731486788127,1.2804748760101543,1.275589080125544,1.2707208702349206,1.265875259807206,1.2610571692297767,1.2562713919245558,1.251522579708615,1.2468153728619757,1.2421542211368979,1.2375435315752832,1.2329875898375064,1.228490607554831,1.2240566979748824,1.2196898785643904,1.215394108258135,1.2111732371713377,1.207031043800148,1.2029378602792196,1.1988621730597182,1.1948049057546128,1.1907669883765901,1.186749315307634,1.1827527628614054,1.178778198026662,1.174826453956398,1.1708983718443258,1.1669947598941959,1.163116410384561,1.1592641000591009,1.1554386065991678,1.1516406685622214,1.147871026172232,1.1441303974873311,1.1404194868229098,1.1367390007892937,1.133089601329336,1.1294719768020343,1.1258867716610759,1.1223346337310953,1.1188161834390713,1.1153320526336883,1.1118828463129748,1.108469158374078,1.1050915718667085,1.1017506704869375,1.0984470161698305,1.095181164440808,1.091953657162058,1.0887650302017977,1.0856355061115806,1.0825809861050644,1.0795956028119513,1.0766735845631816,1.07380926410662,1.070997069164953,1.0682315346621987,1.0655072755271435,1.0628190097558832,1.0601615421103947,1.0575297622724538,1.0549186535292245,1.0523232751377143,1.0497387797892594,1.0471603926740918,1.0445834219992698,1.042003253843935,1.0394153505503825,1.0368152491548623,1.0341985581668014,1.0315609611599603,1.0288982085410487,1.0262061212057358,1.023480587454599,1.020717559983388,1.0179130599563186,1.0150631682485378,1.0121640291709033,1.009211848401295,1.0062028913706966,1.003133481485097,1]
    factorsListB = [0,1.3289432010135136,1.4121489653716217,1.4922930743243243,1.5693755278716217,1.6434016047297297,1.7143686655405406,1.7822718086389961,1.847118480785473,1.9089010885885886,1.9676256334459459,2.0232911355958234,2.0758947423986487,2.1254405697765075,2.1719240166505793,2.215346987612613,2.255710911106419,2.293014550625994,2.3272576775994747,2.3584408061433146,2.3865643475506757,2.411626749517375,2.433629741246929,2.452571882344301,2.468454171945383,2.4812763935810813,2.491038871654106,2.4977404161974475,2.5013823638091215,2.501963591420084,2.499485325168919,2.493946504468178,2.485347438502956,2.4752432208486894,2.465182208863275,2.4551561745897685,2.4451581708661787,2.4351816449050405,2.425220386402027,2.4152694987655927,2.4053242451435812,2.395380028942815,2.3854333197594917,2.3754806086973606,2.365518705850737,2.355544704861111,2.345556238983549,2.335550300549885,2.3255249573303773,2.3154784348283233,2.305408572635135,2.295313638546635,2.28519203360512,2.275042777521035,2.264863740693819,2.2546541481111793,2.2444128088048987,2.234138383860835,2.2238303092963654,2.213487164667316,2.2031080641188066,2.19269261256646,2.182239801860833,2.171748687861969,2.161219004038218,2.1506695848492723,2.1401189230779076,2.1295660895270268,2.1190100155877385,2.108449694599491,2.0978840831624037,2.087312289594833,2.0767335633973816,2.0661470144159573,2.055551800612902,2.044947388795045,2.034333013369044,2.023708034206081,2.013071844004461,2.00242386621194,1.9917634706239444,1.9810902210804555,1.9704036222293178,1.9597032025907688,1.948988434584138,1.9382588930842608,1.927514249464763,1.91675403852128,1.9059779661586305,1.8951856032208474,1.8843766129410662,1.8735506733553609,1.8627074764982374,1.8518467276500292,1.8409681446323318,1.8300714571479375,1.8191564061620216,1.8081597524554194,1.7970301296194153,1.7857842306084493,1.7744383445945948,1.7630078543116139,1.7515077333192568,1.7399523736798086,1.7283553601302626,1.716730136944981,1.705089267573145,1.6934452158057591,1.6818096172344221,1.6701939831352282,1.6586092862215909,1.6470659849038227,1.6355743997345562,1.6241442523656122,1.612785096980204,1.6015060980647766,1.5903161040890028,1.5792236610107706,1.5682369691758762,1.5573640641856406,1.5466126038147523,1.5359901017527084,1.5255036630829089,1.515160376411091,1.504966995252561,1.4949299514358108,1.48505562970895,1.4753501617697915,1.4563646586266499,1.446889821010915,1.43740500325588,1.4279201298244266,1.4184446778633661,1.4089878416196047,1.399558640671922,1.3901657322821444,1.3808176172722677,1.3715224066202754,1.36228812030612,1.3531224549046816,1.3440329822425483,1.335026967920275,1.3261114743048337,1.3172935050529047,1.3085796885921481,1.299976562138444,1.2914905299112889,1.2831276892919101,1.2748941068270452,1.2667956432995497,1.2588379605417712,1.25102665821146,1.2433670601897853,1.2358644806154573,1.228524053917829,1.221350740576815,1.2143494167186695,1.207524876785409,1.200881670106132,1.1944243559966217,1.1881013965974905,1.181858901544774,1.1756978997186411,1.1696192339681526,1.1636238466804874,1.1577126177853305,1.1518864061362075,1.146146010861587,1.1404922902631738,1.1349260048191574,1.1294479743929784,1.1240589614187226,1.1187596725609281,1.1135508361607835,1.1084332016167955,1.1034074263139204,1.0984741900600283,1.093634194456043,1.0888880148370264,1.0842363603838214,1.0796798152390996,1.075218986962151,1.070854469832281,1.0665868452096798,1.0624166818845873,1.0583445009399521,1.054370918169172,1.0504963958722686,1.0467214913015694,1.0430467152493776,1.0394725332642034,1.0359994699289132,1.03260400438489,1.0292633388261005,1.0259791003443348,1.0227528828254275,1.019586147308873,1.016480425293902,1.013437200916958,1.0104578791437924,1.007543886222393,1.0046966038255536,1.001917386400987,0.9992075780111455,0.9965684482119316,0.9940012899542443,0.9915073712044246,0.9890879038217906,0.9867440922578157,0.98447711802204,0.982288140225719,0.9801783116723373,0.978148732538106,0.976200513268818,0.9743347129605987,0.9725523863707458,0.9708545840177015,0.9692423068764723,0.9677165527042454,0.9662783311098742,0.9649285587862679,0.9636682250768506,0.9624982128113259,0.9614194774259471,0.9605140003284535,0.9598490567447979,0.9594036492439576,0.9591572066515529,0.9590894594871209,0.9591805338159152,0.9594108712761057,0.959761293381036,0.9602128800902231,0.9607471193774906,0.9613457300801467,0.96199081078397,0.9626647343669817,0.9633501422370047,0.9640300146368421,0.9646875879786037,0.9653063905978398,0.9658702026394453,0.9663630916072323,0.9667693726721728,0.9670736305501931,0.9672606804951865,0.9673156170605544,0.9672237353004782,0.9669705863678532,0.9665419657939189,0.9659238691875237,0.9651025308145059,0.964064399320694,0.962796133511826,0.9612846047017836,0.9595168861182961]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def mayfairFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [30.2470703125,30.616791596283786,15.511124894425677,10.487339878941443,7.983668971706082,6.487753378378379,5.495486697635136,4.790812017374518,4.265700881545609,3.8601448127815314,3.538133445945946,3.276752293842138,3.060726131404843,2.8794767574064446,2.725452084338803,2.5931121551238743,2.4783003523543075,2.377841191375199,2.2892633844782284,2.210615220483642,2.1403366501266894,2.0771635195463323,2.02006332060043,1.9681808166862518,1.920804410367399,1.8773374155405407,1.8372734212577966,1.8001810404154155,1.7656919265805986,1.7334871745398417,1.703290839667793,1.6748625830972101,1.6479921083192568,1.6226337754658067,1.5987869044366059,1.5763404168677608,1.555194476703266,1.535261110984295,1.5164612597795166,1.4987232951100138,1.4819840714738177,1.466184994541035,1.4512749356499357,1.43720537397863,1.4239342991784398,1.4114219688438439,1.3996326702041717,1.3885337298734908,1.378094922314893,1.3682890280267515,1.3590902132601352,1.3504754467242979,1.342423214981809,1.3349133792548444,1.3279272925269021,1.3214481438114252,1.315459851592664,1.3099476944049313,1.3048979660560345,1.3002976659127348,1.2961350999436938,1.2923986919168144,1.2890780381566043,1.2861636050112615,1.2836460422825169,1.281532208290021,1.279813949247543,1.2784601590863252,1.2774421437177068,1.2767330637362908,1.2763068593146718,1.2761394963956034,1.276208276147241,1.276491562731396,1.2769688898146458,1.2776210585585588,1.278429533305921,1.2793772554514742,1.2804475336213619,1.281624855670544,1.2828943201013514,1.2842417612925425,1.2856537046287906,1.2871176428687725,1.2886211930401383,1.2901528654113674,1.2917013977549496,1.293256500708683,1.294807902718059,1.2963460904285606,1.2978619733014265,1.2993464253229878,1.3007914344796563,1.3021886238557108,1.303530534565483,1.3048097439544808,1.3060190011789132,1.3073191032930482,1.3088545886048677,1.3105960630374691,1.3125151763091216,1.314584700921528,1.3167783477411237,1.3190711048199293,1.3214386684235317,1.3238577863577865,1.3263060838698368,1.328762145980677,1.3312049842811562,1.3336148043291285,1.3359722315532863,1.3382587084550768,1.3404563992179959,1.342547924203241,1.3445167451065376,1.346346669359577,1.3480222334066287,1.3495283895674521,1.3508506002526626,1.3519749828774417,1.3528879526499156,1.3535763738622404,1.3540275955707244,1.3542294318899692,1.3541699303890584,1.3538376794763514,1.3532215774647416,1.3523108723265589,1.349626868420019,1.3479727699454263,1.3461430515976378,1.3441478032542484,1.341996662501905,1.3396991269633673,1.3372642173423424,1.3347008830981717,1.3320177160651756,1.3292231068534568,1.326325109675773,1.3233316900187018,1.3202504002090523,1.3170888121698943,1.3138541014517577,1.3105533359287023,1.3071933429927773,1.3037807629841958,1.300322100440683,1.2968236395178963,1.2932915399538591,1.289731709248311,1.2861500295048773,1.2825521412139935,1.2789434942755256,1.2753295255736663,1.2717154465453357,1.2681062927034608,1.2645071393796266,1.2609227246060342,1.2573578332164712,1.2538170067039698,1.2502523373893109,1.246617039402684,1.2429172501321297,1.2391589572732986,1.2353479833704444,1.2314900504149198,1.2275907038330434,1.2236553766552547,1.2196893733195566,1.2156978928606916,1.2116859355243401,1.2076585003596894,1.203620375478441,1.1995762958034815,1.1955308503257724,1.1914885424864674,1.1874537739540387,1.1834308474830608,1.1794239696771667,1.17543725365991,1.1714747034294741,1.167540271239002,1.163637786896784,1.1597710148848324,1.1559436382909514,1.152159260996758,1.1484214097954908,1.144733536442235,1.1410990021829868,1.137521132229063,1.1340031476072767,1.1305482194230365,1.1271369569760012,1.123747665392519,1.1203799897403413,1.1170336328286594,1.1137082700066023,1.1104035831819035,1.1071192772349925,1.103855062948691,1.1006106240335485,1.0973856831285957,1.0941799845903093,1.0909932130976336,1.0878251238567074,1.0846754608114257,1.0815439409773224,1.078430318534994,1.0753343523697143,1.0722557745384895,1.0691943847218444,1.0661499085686512,1.06312213883668,1.060110841323764,1.057115786184986,1.0541367631058793,1.0511735504450663,1.0482259533288845,1.0452937503133486,1.0423767464752571,1.039474735490935,1.0365875296155003,1.0337149296770847,1.0308567474247405,1.028030980198949,1.0252529564898314,1.0225185499203775,1.0198237137412394,1.0171644502781816,1.0145368600704134,1.011937089756914,1.0093613666346,1.0068059756880003,1.004267258356614,1.001741632392449,0.999225569273756,0.9967155930715625,0.9942083070691327,0.991700357594372,0.9891884331230646,0.9866693044732849,0.9841397753884438,0.9815967158021738,0.9790370402000201,0.9764577067102179,0.9738557363337041,0.9712281983143157,0.9685721892113258,0.9658848721003102,0.9631634554476353,0.9604051790620458,0.9576073396569003,0.9547672636449599,0.9518823260372055,0.948949955958946,0.9459675969304265]
    factorsListG = [15.554027660472974,16.145850929054056,8.40529983108108,5.8480873451576585,4.585726351351352,3.8405141469594595,3.353220896677928,3.0127367881274134,2.7635168127111487,2.5746996996997,2.427771326013514,2.3109427787162162,2.2163613809121623,2.1385886337058215,2.0737417802847493,2.018968186936937,1.9721349767736487,1.931604916037361,1.8961104659346846,1.864646075969061,1.8364099451013516,1.8107529962998714,1.787142966830467,1.7651407351645125,1.7443803666948199,1.7245550042229731,1.7054034766437112,1.6867052599474475,1.6682703909266412,1.6499341980719944,1.6315557256475226,1.6130109286453793,1.5941920924831081,1.575341676904177,1.5567916118094198,1.5385749728523166,1.5207215271912538,1.5032571105734114,1.486205186477596,1.4695868118719682,1.4534209380278718,1.4377243454391893,1.4225128448761262,1.4078001625353551,1.3935990767045454,1.3799212298235737,1.3667772519462398,1.3541768684409143,1.3421287192954674,1.3306412778371484,1.3197218116554055,1.3093772770932697,1.2996140953904627,1.2904382031648394,1.2818548528997749,1.273869634904791,1.2664865618967183,1.2597105226114274,1.253545613568849,1.2479952062099178,1.243063107052365,1.238752440324546,1.2350665543946164,1.2320083755630633,1.22958044103674,1.227498050935551,1.225487161522318,1.2235658437121824,1.2217514935661764,1.2200595423888563,1.2185054823238417,1.2171035609773508,1.2158670511331644,1.2148088598551463,1.2139410181930241,1.2132747395833334,1.2128209945657005,1.2125898410078098,1.212591159368503,1.2128341627822443,1.2133276037267737,1.214079802458709,1.2150985124320204,1.2163914314352002,1.2179657335907337,1.219828255415342,1.2219855154482244,1.2244437325256292,1.2272086928458998,1.2302863673891589,1.2336820218656157,1.2374006905256905,1.2414476190694772,1.245827401872639,1.2505445781968805,1.2556034961770983,1.261008322775901,1.2670657630084983,1.2740114257273856,1.2817454794993859,1.2901723500844597,1.2992001176996923,1.3087405966398384,1.3187088977630546,1.3290235237867074,1.3396059564028313,1.350380515760454,1.3612748444998737,1.3722187152973286,1.3831447806572341,1.3939880820984336,1.4046859425409364,1.4151779822861368,1.4254059589698935,1.4353136738197902,1.4448468254259694,1.453953041723701,1.462581797542735,1.470684112674645,1.4782127642019647,1.4851221582911038,1.4913680992782556,1.4969078946229786,1.5017001865146395,1.5057050044783948,1.508883709881757,1.511198733610843,1.5126138976544212,1.5128008868243243,1.5119429939254159,1.5105542591583714,1.5086677919929874,1.5063156069015444,1.5035288119421895,1.5003375201373248,1.4967710316086422,1.4928577909998273,1.4886253706576824,1.4841005732154142,1.4793094590824083,1.474277325967091,1.4690287589663829,1.4635876554821867,1.4579772490996856,1.4522201552306617,1.4463383244920864,1.4403531326487522,1.4342854000339549,1.4281553659036028,1.4219827298001126,1.415786669423718,1.409585857798331,1.4033984797642312,1.3972422478281854,1.391134459970303,1.3850918648892283,1.3791309106491545,1.373267524502598,1.3675173160151604,1.3618954220333614,1.3562763771875526,1.3505322746248853,1.3446741194259348,1.3387127086058526,1.332658537443694,1.3265218880695926,1.320312756823768,1.3140409216764197,1.3077159291665001,1.3013471012085156,1.2949435416604929,1.2885141234814486,1.2820675526162906,1.2756122969514505,1.269156649674228,1.2627087154903929,1.2562764159485227,1.2498674945848676,1.2434895034644893,1.2371498634865334,1.230855795097152,1.2246143781788315,1.2184325378625296,1.2123170487328785,1.2062745388970053,1.2003114761844758,1.19443420771833,1.1886489631253594,1.1829618052762585,1.1773786867665363,1.1719054355300165,1.1665477580852337,1.1612579426900995,1.1559860301768425,1.1507341476091477,1.1455044291391598,1.1402989320915935,1.1351196722290473,1.129968657954044,1.1248478080130913,1.1197590522104428,1.1147042331384216,1.109685205838728,1.1047037566346218,1.0997616369942733,1.0948605803922855,1.0900022868061676,1.0851884076600264,1.0804205785574001,1.0757003882370095,1.0710294109553127,1.0664091912658162,1.0618412137379458,1.0573269814425992,1.0528679387963544,1.0484655187413976,1.044121112602558,1.0398361013097028,1.0356118405702364,1.0314496314496315,1.027350796250153,1.0233166037262982,1.0193482998746364,1.0154471378989203,1.0116209177927928,1.007873578950909,1.004200590751131,1.0005975165260863,0.997059968290821,0.9935836487175015,0.9901643420320179,0.9867978980356805,0.9834802377778462,0.9802073520335239,0.9769752928002804,0.9737801929706289,0.9706182437443872,0.9674857003348214,0.9643788806294527,0.9612941707576718,0.9582279962956992,0.9551768623507128,0.952137324770517,0.9491059958644288,0.9460795499840561,0.9430547021452188,0.9400282272403984,0.9369969521799395,0.9339577548475151,0.9309075696790541,0.9278433733919895,0.9247621776003124,0.9216610672458372,0.9185371601878393,0.9153876130266296,0.9122096396781303]
    factorsListB = [14.693148226351353,15.130621832770272,7.802114125844595,5.370996973536037,4.1639635240709465,3.446357685810811,2.973294094876126,2.6398181105212357,2.3934623099662162,2.2050634618993996,2.0571368243243247,1.9385509444103197,1.8418826541385138,1.7619928371881497,1.6952163519546333,1.6388601492117119,1.5909060916385136,1.549809345190779,1.5143713048986487,1.4836443145448082,1.4568689294763515,1.4334316180019306,1.412830399646806,1.3946517424353702,1.3785488369228605,1.3642303631756758,1.3514523575558732,1.3400045553365867,1.329708143550917,1.3204076079042406,1.3119694890202704,1.3042771223844813,1.2972280141469594,1.2909540399774775,1.2855847575516695,1.2810339496862935,1.2772249788851353,1.274088422776662,1.2715635557432434,1.2695952036772349,1.2681333799619934,1.2671336184698418,1.2665553737331081,1.2663621788576367,1.2665202822673527,1.2669992257882883,1.267771773556845,1.2688118845241518,1.2700965125281531,1.2716044927261447,1.2733158255912163,1.2752125977080022,1.2772780198317308,1.279496320834396,1.2818536309747248,1.2843363693949634,1.2869321609555986,1.2896297304706021,1.292418352822111,1.2952878063444802,1.2982292106559685,1.3012338350132922,1.3042930862440063,1.3073999641382454,1.310546875,1.3138988597972974,1.3175951608568797,1.3215933765505246,1.3258534053929851,1.3303372793649628,1.3350093885738417,1.3398365010587172,1.3447863146349475,1.349829200990374,1.3549365983382031,1.3600818201013514,1.3652390633334814,1.3703845510486135,1.3754950488348927,1.3805491668983065,1.3855260900548987,1.390406031031031,1.3951706505953363,1.3998018573449202,1.4042828926862132,1.4085974761526234,1.4127303914106695,1.416666970041162,1.4203930604077089,1.423895295181066,1.4271610477665164,1.4301779565451442,1.4329343408030992,1.4354191641238012,1.4376215789426396,1.4395311944345663,1.4411384651252817,1.442596001889454,1.4440551690481935,1.445504853219697,1.446934253589527,1.4483330624289203,1.4496912468534713,1.4509992917295331,1.4522480478901376,1.4534285890242922,1.454532512409963,1.455551606111076,1.4564779623373374,1.4573040240283288,1.4580224489404179,1.45862621886033,1.4591084483967784,1.459462671067777,1.4596825315241229,1.4597618954722387,1.459694897028629,1.4594758708528242,1.459099175893982,1.4585596379599137,1.4578520353849944,1.456971428185029,1.4559130383425176,1.4546721359316634,1.4532443032435158,1.4516251055743243,1.4498103537410179,1.4477959385474304,1.4431744153310289,1.4406116509387994,1.4378981703405458,1.4350421477496673,1.4320515611505538,1.428934150378807,1.4256973770645647,1.4223485318958664,1.4188946445304793,1.415342636496891,1.4116991352019737,1.4079705786981178,1.404163315992189,1.400283377843072,1.3963368108875922,1.3923292646894943,1.3882664604933597,1.384153804616635,1.3799966011531304,1.3758000331346445,1.3715691444511835,1.3673088004997185,1.3630237814905137,1.358718741838827,1.3543981711490904,1.3500665066827175,1.3457279860505666,1.3413868439503205,1.3370471231332846,1.33271276400263,1.3283876908305714,1.324075647302576,1.319748521631589,1.315377633492868,1.3109657516568045,1.3065155371286874,1.3020296263948608,1.2975105924118773,1.2929609267529132,1.288383081306055,1.2837794304046557,1.2791523119224464,1.2745039897524992,1.269836675139211,1.2651525663409526,1.260453754198703,1.2557423194679056,1.2510202956141068,1.2462896515092954,1.241552330315964,1.2368101949114356,1.2320651217623875,1.227318909411397,1.2225733168726334,1.2178301007686734,1.213090925743381,1.2083574382818207,1.2036313026736416,1.1989140593948728,1.1942072687922298,1.1895124756452882,1.1848311227551565,1.1801647090736433,1.1755146335911106,1.1708775140911638,1.166248354482664,1.1616262540334807,1.1570102630632066,1.152399484668679,1.147793023403375,1.1431900183985808,1.138589609506968,1.1339909701124866,1.1293932899677215,1.124795750412416,1.1201975811835503,1.115597994860333,1.1109962433349803,1.1063915929558974,1.1017833083186477,1.0971706680935198,1.0925529882561134,1.0879295821133077,1.08329976814733,1.078662885383458,1.0740182852016371,1.069365338721716,1.0647034210724398,1.06003191129908,1.0553502149745073,1.0506577409962938,1.0459539015111525,1.0412381342341706,1.0365098795810697,1.0317685806076538,1.0270137124079997,1.0222105283994933,1.0173302764272154,1.0123812855673853,1.007371753242243,1.002309697670173,0.9972030478274642,0.9920595454042721,0.9868868341650345,0.9816924124911192,0.9764836505864338,0.9712677932046077,0.9660519692966603,0.9608431735730985,0.955648303979531,0.9504741154064302,0.9453272776560742,0.9402143361390112,0.9351417280771862,0.9301157847300425,0.9251427470871871,0.9202287138461804,0.915379738184259,0.9106017485373468,0.9059005644182174,0.9012819516028642,0.8967515308277028,0.8923148726883009,0.8879774462660205,0.8837446472148409,0.8796217602398781,0.8756140130249735,0.8717265257964264]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def nineteen77FilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [69.99701752533784,70.36757020692568,35.3876953125,23.739631721565317,17.9241283519848,14.441327069256758,12.124617293074325,10.474017404681467,9.239539893897804,8.282298411692942,7.518966427364866,6.896514367705774,6.379590283643019,5.943719748895531,5.571421973033302,5.249875070382883,4.969465925886825,4.722840228785771,4.504280892220346,4.309272342860953,4.134202781883446,3.976148372144466,3.8327174831081083,3.701932698663337,3.582147821649775,3.4719800464527033,3.370257784076144,3.2759849693443446,3.1883059468508685,3.106484902871622,3.0298823726069823,2.9579431056560592,2.890179608319257,2.8264038185913187,2.7664839558078302,2.7100936595077223,2.6569428315033785,2.606773805583455,2.5593546491598507,2.5144785711191964,2.471958469700169,2.4316258188447595,2.393328142595721,2.3569271488057826,2.3222971173410625,2.289323503190691,2.257901721779524,2.227936089347326,2.1993391707136825,2.1720298602971595,2.1459345967060814,2.1209848117878907,2.097117211863306,2.0742740271226414,2.0524010338463463,2.0314481917997544,2.01136927070765,1.9921205899567331,1.9736623915132805,1.955956718105818,1.9389690227336713,1.9226663747507755,1.907018180920336,1.8919959999061562,1.8775725493559967,1.8637411073934513,1.8504893609874078,1.8377854446097217,1.8255993671750796,1.8139028762118097,1.802669145149614,1.791873230514846,1.7814913912936374,1.7715008257936875,1.7618806781866325,1.7526108530405407,1.7436719652938302,1.7350461510617763,1.726716293366684,1.718666141913274,1.7108802589210306,1.7033438060456292,1.69604299063736,1.688964366757571,1.6820954429597008,1.6754240051172498,1.668938560653677,1.662628145386766,1.656482218524455,1.6504909354359627,1.6446445957676425,1.6389340705746958,1.6333506278229657,1.6278859110496586,1.622531989581836,1.617280988842461,1.612125706028294,1.60718684968393,1.6025694285843561,1.5982438404313406,1.594181469066723,1.5903549623068305,1.5867380406026432,1.5833053809080624,1.5800326341403002,1.576896504484395,1.5738743884657063,1.5709445892665448,1.5680863358475663,1.565279498337931,1.5625046788621009,1.559743238012083,1.556977143158784,1.5541890583891416,1.551362198187085,1.5484803608805817,1.5455280172413792,1.5424899997653905,1.5393517669384162,1.536099266036651,1.5327188027871623,1.5291972992168303,1.525521997968127,1.521680556556938,1.5176610838566642,1.5134520164695946,1.5090422104582262,1.5044208209193446,1.4945448150730674,1.489370442031575,1.4840653287471632,1.478640244692491,1.4731056354463017,1.4674716840207747,1.4617481250782034,1.4559445525201211,1.4500701838072105,1.4441340648562966,1.4381448863291126,1.432111137714165,1.426041091061973,1.4199427157061881,1.4138238272759758,1.4076919555664062,1.4015544909133273,1.3954185985803869,1.3892912264145523,1.3831791567750182,1.3770889678019569,1.3710271062077704,1.364999804233041,1.3590131518172675,1.3530730581224606,1.347185300249265,1.3413555274970033,1.3355891808650597,1.3298916047566276,1.3242680082735525,1.3187234694710925,1.313262939453125,1.3078485616645859,1.302440135447948,1.2970390288198477,1.2916465160794848,1.2862638806242324,1.2808923550515408,1.2755331226798936,1.2701873975677689,1.2648563259947725,1.259541007862182,1.2542425366361427,1.2489620187161181,1.2437004777085612,1.2384589326496487,1.233238398135859,1.2280398469592197,1.2228642112882215,1.2177124579482046,1.2125854768656577,1.2074841748486769,1.2024094022101781,1.1973620268298004,1.1923428976171357,1.1873528091663759,1.182392556724799,1.1774629361752125,1.1725647087334243,1.1676986194191616,1.1628653974845382,1.15806577419319,1.1533004482210452,1.148570086504962,1.1438537520731953,1.1391320450454079,1.1344078735436158,1.1296841536709703,1.1249636920788175,1.1202492720437056,1.115543604318043,1.110849328943201,1.1061690498363335,1.1015053520172013,1.0968607208126,1.0922375928174268,1.0876384053642056,1.0830655004120475,1.078521190602967,1.0740077599666225,1.0695274172479148,1.065082360541345,1.0606747149993596,1.0563065968016956,1.0519800668984345,1.0476971477172268,1.043459824059161,1.039270043969751,1.035129734789513,1.0310407430931148,1.0270049419871499,1.0230241405290235,1.0191001001045235,1.0152345652240078,1.0114292786953856,1.0076858932907518,1.0040070881428302,1.0003919621969177,0.9968368542990609,0.9933381819962438,0.9898924254110484,0.9864960971926411,0.9831458275061791,0.9798382335140232,0.9765700612512325,0.9733380559796576,0.9701390464392252,0.9669699290996836,0.963827604088711,0.9607090652192043,0.9576113497147285,0.9545315373051275,0.9514667561894591,0.9484141752180416,0.94537103699837,0.9423345955378407,0.9393021631424953,0.9362711092320884,0.9332388324697896,0.9302027668242052,0.9271604007351195,0.9241092562288852,0.9210469013935811,0.9179709298270089,0.9148789862131618,0.9117687523276229,0.9086379333722511,0.9054842768488705]
    factorsListG = [51.85214315878379,51.88788006756757,25.95698506123311,17.31056007179054,12.985572608741554,10.389408255912162,8.657866606841216,7.420576058759653,6.492349160684122,5.770305461711712,5.192716691300676,4.720300023034398,4.326869105433559,3.9942908653846154,3.7096178209459465,3.4633525126689193,3.248371845967061,3.059229524791336,2.891689541103604,2.7424069834637272,2.6087065825591216,2.488422644184363,2.379782636862715,2.2813222954612224,2.1918230486345722,2.1102586570945947,2.035762794795998,1.9675965027527529,1.9051268588622106,1.8478082406220877,1.7951673353040543,1.7467923284928075,1.7023224701752535,1.6612555826423014,1.623119457347973,1.5876594926399614,1.5546475430508633,1.5238811974981739,1.4951793513291252,1.4683784595893972,1.4433326514991554,1.4199093219553396,1.3979894375402189,1.3774638101037084,1.358234077472359,1.340210620777027,1.3233110403202115,1.3074605107101782,1.2925901670713682,1.2786364968284611,1.2655418602195947,1.2532523619667462,1.2417187601513775,1.2308950312340643,1.2207390495964716,1.2112117533015971,1.2022761635798747,1.1938988227536749,1.1860478979787978,1.1786941619188045,1.1718101157798424,1.1653700639676563,1.1593501815197256,1.153727737223831,1.14848162676837,1.1437187337577963,1.139526467163186,1.1358578071424972,1.132668887867647,1.1299180039414416,1.127566398708977,1.1255767555077085,1.123914380689283,1.12254612007127,1.1214411465942296,1.1205695734797299,1.119903781505601,1.1194169006669008,1.1190839464765245,1.1188811994846906,1.1187856313344595,1.118776002565065,1.1188316269775873,1.1189328152983555,1.1190614442567568,1.1191993119038155,1.1193298301480987,1.1194365668200528,1.119504586484567,1.1195187352907683,1.1194654126783035,1.1193307457955897,1.119102182175382,1.1187674254395525,1.1183145620687178,1.117732457992532,1.1170101681271116,1.116209849104904,1.1154018934431882,1.1145879988653427,1.1137700591216215,1.1129495009783918,1.1121280833912957,1.1113073688828392,1.1104888598785083,1.1096738758848135,1.108863935611614,1.1080603776600784,1.1072642466685436,1.1064770332258864,1.1056996938344594,1.1049336260880813,1.104179706352558,1.1034391303291677,1.1027129360034378,1.1020020105023502,1.1013073241277378,1.1006299268018018,1.0999706091817454,1.0993302462454575,1.0987095738316441,1.0981096306469176,1.0975309886602793,1.096974523113052,1.0964408681615083,1.0959307432432432,1.0954449496929966,1.0949839518714088,1.0941357759467316,1.0937415743568086,1.0933646738639882,1.0930043813344594,1.092659677196581,1.0923295230719292,1.0920131068568568,1.091709591815506,1.0914180693153235,1.0911377048753919,1.0908677829695703,1.0906074199897442,1.0903559445832136,1.0901126113734776,1.0898767419763515,1.0896475393850882,1.089424456110205,1.08920673368949,1.0889937689602869,1.0887850196453845,1.0885797808872213,1.0883774985923425,1.0881775896472838,1.087979573104663,1.087782808083819,1.08758679889051,1.0873911051928944,1.0871951287600703,1.0869984126866716,1.086800511634558,1.0866009084703807,1.0863992227090373,1.086225534297885,1.0861060034644021,1.086034289957615,1.0860042081668178,1.0860097224355039,1.086044982294041,1.0861041588697604,1.0861816799011623,1.0862721050145931,1.0863700442170112,1.0864702721841908,1.0865676851110742,1.0866572971996564,1.086734275189791,1.0867938208856178,1.086831320122946,1.0868421884543442,1.086821981523307,1.0867663911511023,1.086671168238551,1.0865321211339967,1.0863451865649132,1.08610642613028,1.0858119511856457,1.0854579393318573,1.0850406858471375,1.0845565123267904,1.0840019063746675,1.0833733251946143,1.0826674047608464,1.0818807651319513,1.0810101483319257,1.080085663581125,1.0791386869764819,1.0781679572451057,1.077172205189086,1.0761502041282243,1.0751007355011262,1.0740226383978593,1.072914742134713,1.0717758993251647,1.0706050179685411,1.0694010113292172,1.0681627978075732,1.0668893169083717,1.0655795607595613,1.0642325250267253,1.0628471929665169,1.0614226146516956,1.059957842538409,1.0584519314097125,1.056903969445197,1.0553130619478412,1.053678330943933,1.0519988841039443,1.0502739067192193,1.0485025382840718,1.0466839946176467,1.0448174305378797,1.0429020762150645,1.040937160824569,1.038921919999867,1.036855610482347,1.0347374875573119,1.0325709987331082,1.03036091003199,1.028108495291478,1.0258149915309018,1.0234816357727303,1.0211096220094926,1.018700137840763,1.0162543361695815,1.0137733642663083,1.011258349789844,1.0087103871657561,1.0061305592598524,1.003519944582389,1.0008795757930495,0.9982104958768588,0.9955137098157729,0.9927902196011656,0.9900410038460465,0.9872670250545685,0.9844692367127791,0.9816485632734935,0.978805927569147,0.9759422308089815,0.9730583596666065,0.9701551931967737,0.9672335831925676,0.9642943875890021,0.9613384277919801,0.9583665285211332,0.9553794950138993,0.9523781231110477,0.9493631929964633]
    factorsListB = [62.21584670608109,62.282978779560814,31.17450775971284,20.804837063626128,15.620001715582772,12.509211359797298,10.43553587767455,8.95457664695946,7.844134356524494,6.980764944632132,6.290400654560811,5.72590985872236,5.255869272592906,4.85852634485447,4.51834165359556,4.223920502533784,3.9667160446579395,3.7401947846283785,3.5392721823385886,3.359936210881935,3.1989759290540545,3.0537932603362297,2.922260706196253,2.8026230629406585,2.69341601122607,2.593410050675676,2.5015643272479213,2.41699316504004,2.3389369419642856,2.2667399012698044,2.1998359199042796,2.137729368733653,2.0799882218644425,2.025880505860975,1.974782097699722,1.9264818110521236,1.8807933910472974,1.8375492917960192,1.7966006456703416,1.757813515137734,1.721066696579392,1.686251776738629,1.6532700390122266,1.622032563541012,1.592457914235258,1.564472187030781,1.5380079043037604,1.5130030504240943,1.4894010526639923,1.4671499564775234,1.4462016997466216,1.4265125074523053,1.4080414643158785,1.390750992000255,1.374606295748874,1.359575111332924,1.345627007797418,1.3327346157835467,1.3208715433510019,1.310013858866812,1.3001387862471847,1.291225259262849,1.2832535707960986,1.2762052649747961,1.2700628332189612,1.2648266956860708,1.2604604560170967,1.2568954215409438,1.2540677166136727,1.2519162122380534,1.2503838380791508,1.2494165531618766,1.248963502076295,1.2489764352323214,1.2494095327908146,1.2502201224662164,1.2513669096728308,1.2528112591589156,1.2545163477780665,1.256447383894971,1.2585711504961994,1.2608560709146648,1.2632722697449736,1.2657909933653535,1.2683851715834138,1.2710290080981717,1.273697599534491,1.276367490874495,1.2790162932374847,1.2816223274274978,1.2841650243993994,1.2866250092812592,1.2889833192567568,1.2912220909165215,1.2933240806048736,1.295272770714794,1.2970523318728886,1.2988947891996379,1.3010189268908579,1.3033904821014197,1.3059766944679054,1.30874597040574,1.3116682140550477,1.3147143702030306,1.317856247360642,1.3210672307351996,1.3243213363717492,1.3275936750126294,1.330860279224537,1.334097879505796,1.3372844124308967,1.340398312427715,1.343418901951617,1.3463262354064518,1.349101009160888,1.3517246483915983,1.3541792756691229,1.3564474555685495,1.3585124555335262,1.3603581054465705,1.3619687192074887,1.3633292383292384,1.3644249898752494,1.3652418317231103,1.3657660247350427,1.3659843222128378,1.3658838979883903,1.3654522779115237,1.3636778186707785,1.3625784193899428,1.3613772855632351,1.3600726803241452,1.358662670982778,1.3571455795084963,1.3555197287130882,1.3537834422197934,1.3519351407606284,1.3499733386579515,1.3478964505760258,1.3457030307372106,1.3433916743788337,1.340961062776575,1.3384097295230108,1.335736523877393,1.3329400538065006,1.3300191461929611,1.3269726149539207,1.323799216895316,1.320497919335548,1.3170675851632885,1.3135071073893638,1.3098154949768848,1.3059916534181242,1.302034688021016,1.2979435356160092,1.2937172871865257,1.2893550568756456,1.2848559186102142,1.2802190318635263,1.275443494642103,1.2704711934554411,1.2652573838486925,1.2598211041455087,1.254180847851949,1.248354720132064,1.2423603302568382,1.236214944741008,1.229935340439491,1.22353795568752,1.21703880322188,1.2104535212124132,1.2037974225133565,1.1970854468540073,1.190332171560704,1.1835518407637549,1.1767584310995567,1.1699655101506432,1.1631864332841444,1.1564342021294165,1.1497215293907188,1.1430608832837932,1.1364644217427422,1.129944036954475,1.1235114163713646,1.1171779234101078,1.1109547125880923,1.1048526821806348,1.0988825512316256,1.0930547421025938,1.087379492465327,1.0818668083168246,1.076526538745777,1.0713027892134768,1.0661324506086305,1.0610142951695687,1.055947103358341,1.0509297306407772,1.0459610056167674,1.0410397970108143,1.036164996172931,1.0313355165158162,1.0265503256340731,1.0218083302042422,1.0171085553758032,1.012449980945122,1.0078316065183432,1.0032524988473528,0.9987116791850069,0.994208250658703,0.9897413020581967,0.9853099238113633,0.9809132390700696,0.9765504184311954,0.9722205863272371,0.9679229295156349,0.9636566345398132,0.959420902937788,0.9552149660321876,0.951038039055751,0.9468893815024186,0.9427682364119635,0.9386738901855826,0.9346056124352352,0.9305627300012066,0.9265428661082958,0.9225444159591007,0.9185677941802968,0.9146133791840773,0.9106815715867683,0.906772765037456,0.9028873178043101,0.8990256246405013,0.8951880310433825,0.8913749048026393,0.8875865934085682,0.8838234524414511,0.8800858175595493,0.8763740187798092,0.8726884082042294,0.8690292770798143,0.8653969665780602,0.8617917849651693,0.8582140354330026,0.8546640297243645,0.8511420610262688,0.8476484311698322,0.8441834103840683,0.8407472911458902,0.8373403612337865,0.833962890625,0.8306151581385607,0.8272974119836913,0.8240099225259722,0.8207529558732577,0.8175267480831016,0.8143315701871305]
    def newBandR(intensity):
        iO = int( intensity * 0.9 * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()

def lofiFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [0,0.27785326086956524,0.29020040760869564,0.3022701539855072,0.3140625,0.3255740489130435,0.3368036684782609,0.34775329968944096,0.35842391304347826,0.3688141606280193,0.3789232336956522,0.38875216156126485,0.3983016304347826,0.4075708089464883,0.4165591032608696,0.4252672101449276,0.43369565217391304,0.44184382992327365,0.449711277173913,0.45729851973684216,0.4646059782608695,0.47163318452380953,0.4783797554347826,0.48484611294896035,0.4910326086956522,0.49693885869565224,0.5025645380434782,0.5079099989935588,0.5129755434782609,0.5177608461394303,0.522265625,0.5264901823281908,0.5304347826086957,0.5341392868906456,0.5376688379156009,0.5410563858695652,0.5443312198067632,0.5475199214159812,0.5506462743135012,0.5537311872909699,0.5567934782608696,0.5598505434782609,0.5629181224120083,0.5660100954246714,0.569139081027668,0.5723169535024154,0.575554554584121,0.5788614419518964,0.5822463768115942,0.5857177517746229,0.5892832880434783,0.5929497682225064,0.5967234531772575,0.6006104517022149,0.6046164200885669,0.6087462944664032,0.6130046583850932,0.6173960717009916,0.6219247797976012,0.626594452376566,0.6314085144927536,0.6363704450285104,0.6414834984221599,0.6467504528985507,0.6521739130434783,0.6576805497491639,0.6631973608366272,0.6687282000324465,0.6742766943734015,0.6798460144927536,0.6854391498447204,0.6910591606705451,0.6967089371980676,0.702390978633115,0.7081076490893067,0.7138614130434783,0.7196546052631579,0.725489218661773,0.7313671439520625,0.7372903910979637,0.7432608695652174,0.7492801848497047,0.7553498641304348,0.7614715656102672,0.7676468685300206,0.7738770780051151,0.7801634384479272,0.7865073322713643,0.7929100790513833,0.7993727482291159,0.8058963617149759,0.812482083134257,0.8191310255198488,0.8258440714118747,0.8326220657955596,0.839465996853547,0.8463768115942029,0.8534532930860601,0.8607739019520853,0.8683096247804128,0.8760326086956521,0.8839161039065863,0.8919344096334186,0.9000628231848881,0.9082775919732442,0.9165558682712216,0.9248756665299426,0.9332158230902072,0.9415559581320451,0.9498764397187874,0.9581583498023716,0.9663834520661966,0.9745341614906833,0.9825935155348211,0.9905451468344776,0.9983732573251418,1.0060625937031484,1.013598424145299,1.0209665162122328,1.0281531158659116,1.0351449275362319,1.0419290951760691,1.0484931842480398,1.0548251645899611,1.060913394109397,1.0667466032608695,1.0723138802622498,1.0776046570095856,1.087446086640546,1.0922392349498329,1.0969817639188517,1.101667490118577,1.1062904160877738,1.1108447233939,1.1153247660024155,1.119725063938619,1.1240402972270709,1.128265300094518,1.1323950554230529,1.136424689440994,1.1403494666396854,1.1441647849050827,1.1478661708536029,1.151449275362319,1.154909869284108,1.158243839338892,1.1614471841725822,1.164516010575793,1.1674465298548293,1.1702350543478262,1.1728779940793261,1.1753718535469106,1.1777132286338448,1.1798988036420102,1.1819253484396914,1.1837897157190636,1.185488838358488,1.1870197268849754,1.1883794670324037,1.1895652173913045,1.1906072778827976,1.1915391841116478,1.1923629634569217,1.1930805938494167,1.1936940052700922,1.1942050811943425,1.1946156599843791,1.194927536231884,1.1951424620529971,1.1952621483375958,1.195288265954742,1.1952224469160768,1.1950662854988692,1.1948213393303349,1.1944891304347827,1.1940711462450593,1.1935688405797102,1.192983634587201,1.1923169176584891,1.1915700483091787,1.1907443550324286,1.1898411371237458,1.188861665478736,1.1878071833648394,1.1866789071680377,1.1854780157017004,1.184205696622152,1.182863078439379,1.1814512882447665,1.1799713958810067,1.1784244821306624,1.1768115942028985,1.1751160259208155,1.173323691730166,1.17143948796335,1.1694681785333019,1.1674144629531285,1.165282945796278,1.1630781070775071,1.1608043796705163,1.158466065984615,1.1560674252717391,1.1536125910259156,1.1511056573189737,1.1485505969147667,1.1459513466586642,1.1433117262983092,1.1406355229508518,1.1379264106218796,1.135188033773292,1.1324239325626546,1.1296375953730646,1.1268324550450348,1.1240118653732605,1.1211791226933772,1.1183374622977682,1.1154900598420907,1.1126400278439121,1.1097904365119986,1.1069442809334857,1.1041045211981113,1.1012740449348806,1.0984557022567754,1.0956522876431483,1.0928538647342996,1.0900482682642363,1.0872349196753497,1.0844132459045457,1.0815826954867869,1.0787427173174622,1.0758927721324758,1.0730323299653883,1.0701608676700411,1.0672778755791876,1.064382852700769,1.061475299787416,1.0585547327361093,1.0556206733500126,1.0526726514355842,1.0497102046358413,1.0467328782677758,1.0437402251638015,1.040731805517115,1.0377071856432785,1.0346659421878466,1.0316076559833354,1.0285319141132105,1.025438312460965,1.022326451270435,1.0191959398352581,1.016046390768025,1.0128774246731818,1.009688667760188,1.0064797518637767,1.0032503147889484,1]
    factorsListG = [0,0.19833559782608695,0.20529891304347828,0.21219429347826088,0.2190217391304348,0.22578125,0.23247282608695652,0.23909646739130436,0.24565217391304348,0.2521399456521739,0.25855978260869567,0.26491168478260874,0.27119565217391306,0.2774116847826087,0.28355978260869563,0.2896399456521739,0.2956521739130435,0.30159646739130436,0.30747282608695653,0.31328125,0.31902173913043474,0.32469429347826084,0.33029891304347825,0.33583559782608696,0.34130434782608693,0.34670516304347826,0.3520380434782609,0.3573029891304348,0.3625,0.3676290760869565,0.37269021739130437,0.37768342391304344,0.3826086956521739,0.38736052783267455,0.3918668078644501,0.396174301242236,0.40032457729468596,0.40435425235017625,0.4082960883867277,0.41217992265886283,0.4160326086956522,0.41987796593319193,0.4237375452898551,0.42763128791708793,0.4315773221343873,0.4355917874396136,0.4396894198960302,0.44388406278908416,0.44818840579710145,0.45261375610026616,0.4571705163043478,0.46186860613810743,0.4667171822742475,0.4717243898687449,0.47689777073268924,0.48224462697628456,0.48777173913043476,0.4934851139397407,0.4993903438905547,0.5054929301768607,0.5117980072463768,0.5183100944404847,0.5250334195301543,0.5319722114389235,0.5391304347826087,0.5463409280936454,0.5534497488471674,0.5604794471933809,0.5674512468030691,0.5743848948487713,0.5812990100931678,0.5882114015615432,0.5951388888888889,0.6020971374329959,0.6091009657755582,0.6161646286231884,0.6233016304347826,0.6305245535714286,0.6378453351449276,0.6452755228398459,0.6528260869565218,0.6605072463768116,0.6683287215005302,0.6762999688973285,0.6844299948240166,0.6927271819053709,0.7011995228766431,0.709854838205897,0.7187005928853755,0.7277437255740107,0.7369908665458936,0.7464485412685141,0.7561229914933838,0.7660200078892005,0.7761451347132284,0.7865038615560641,0.7971014492753623,0.8081747604773645,0.8199045446983141,0.8322141249451033,0.8450298913043478,0.858280980951356,0.8718993099957374,0.8858196034719291,0.8999790969899665,0.9143172554347826,0.9287758280352748,0.9432989003453881,0.9578326288244766,0.9723249900279218,0.9867258522727272,1.000987043429299,1.0150621118012422,1.0289060997018085,1.0424756269069413,1.0557289697542533,1.0686258433283358,1.0811271948160535,1.0931952952284452,1.1047938264979904,1.1158876811594203,1.1264427719637082,1.13642612927655,1.1458059937256981,1.1545516304347825,1.162633152173913,1.1700216205141478,1.1766891422030126,1.1879561899646107,1.1929360890468228,1.1975639416694324,1.201854825428195,1.205823492154299,1.2094842533257624,1.2128508705716587,1.2159367007672635,1.2187548347746748,1.221317984010712,1.2236383719111668,1.2257278726708074,1.227598144079556,1.2292605155388856,1.230725880776832,1.2320048309178744,1.2331077820464769,1.2340448648749256,1.2348258189145223,1.2354601204465334,1.2359571053399476,1.2363258605072465,1.2365750915544917,1.236713386727689,1.2367490819923983,1.2366902967955957,1.2365449410501403,1.2363207218506131,1.236025149932498,1.235665545886076,1.2352490461358354,1.2347826086956522,1.2342162921111262,1.2335006541867954,1.2326431319185116,1.2316509809119829,1.2305312808794466,1.2292909409376638,1.227936704715569,1.226475155279503,1.2249127198835863,1.2232556745524297,1.221510148503051,1.2196821284125379,1.2177774625376978,1.2158018646926536,1.2137609180900621,1.2116600790513834,1.209504680591378,1.2072999358817782,1.2050509415988584,1.2027626811594203,1.2004400278495075,1.198087747849976,1.1957105031628654,1.193312854442344,1.1908992637338425,1.1884740971248247,1.1860416273105092,1.1836060360777059,1.1811714167098,1.1787417763157895,1.1763210380861597,1.173913043478261,1.171487498944019,1.1690136850067234,1.166494695861204,1.163933562555457,1.161333254593357,1.1586966814888011,1.1560266942729953,1.1533260869565216,1.1505975979477612,1.1478439114291865,1.1450676586929749,1.1422714194373402,1.1394577230249205,1.1366290497045166,1.1337878317974166,1.1309364548494985,1.12807725875026,1.125212538819876,1.122344546865341,1.119475492206727,1.1166075426745254,1.113742825579033,1.1108834286526794,1.1080314009661836,1.1051887538193748,1.1023574616074991,1.099539462663788,1.0967366600790514,1.0939509224990163,1.0911840849001175,1.088437949344414,1.0857142857142859,1.0830200030193238,1.0803584311273566,1.0777259953792377,1.075119183829138,1.072534545875261,1.069968690926276,1.0674182871023905,1.064880059970015,1.0623507913090129,1.0598273179115572,1.057306530411656,1.0547853721444362,1.0522608380343057,1.0497299735111436,1.0471898734537022,1.0446376811594205,1.042070587339888,1.0394858291412146,1.0368806891885847,1.0342524946543121,1.0315986163487134,1.0289164678331566,1.0262035045546558,1.0234572230014025,1.020675159878645,1.0178548913043477,1.0149940320240776,1.0120902346445826,1.0091411888855475,1.0061446208490243,1.003098292306053,1]
    factorsListB = [0,0.3605298913043478,0.37717391304347825,0.39341032608695653,0.4092391304347826,0.42466032608695653,0.4396739130434783,0.4542798913043478,0.46847826086956523,0.4822690217391304,0.49565217391304345,0.5086277173913044,0.5211956521739131,0.5333559782608696,0.5451086956521739,0.5564538043478261,0.5673913043478261,0.5779211956521739,0.5880434782608696,0.597758152173913,0.6070652173913044,0.6159646739130435,0.6244565217391305,0.6325407608695652,0.6402173913043478,0.6474864130434783,0.6543478260869565,0.6608016304347827,0.6668478260869566,0.6724864130434782,0.6777173913043478,0.6825407608695652,0.6869565217391305,0.691108777997365,0.6951556505754476,0.6991173330745342,0.7030117753623188,0.7068545277614572,0.7106595037185355,0.7144396251393534,0.7182065217391305,0.721970274390244,0.7257400038819876,0.7295243775278059,0.7333312747035573,0.7371674969806763,0.7410392544896031,0.7449525901942646,0.7489130434782609,0.7529253549245786,0.7569938858695652,0.761122988597613,0.7653166806020066,0.7695783557219033,0.7739111564009662,0.7783183053359684,0.782802795031056,0.7873671100305111,0.7920135635307347,0.7967445997605012,0.8015625,0.8064691175160371,0.8114661860098177,0.8165555986887508,0.8217391304347826,0.8270061663879599,0.8323400444664032,0.8377342229072031,0.8431825447570332,0.8486787177063642,0.8542168090062111,0.8597916985609307,0.8653985507246378,0.871032329511614,0.8766882711515864,0.8823623188405797,0.8880506292906178,0.8937491177300959,0.8994539088628764,0.9051617535773253,0.9108695652173914,0.9165739902039721,0.9222718385471899,0.9279604832372971,0.9336374223602485,0.9392998721227622,0.9449451782103134,0.9505711987756121,0.9561758893280633,0.9617569156082071,0.9673120471014494,0.972839524605829,0.9783376654064272,0.9838044939223937,0.989238118640148,0.9946370852402746,1,1.005403266472434,1.010914277395741,1.0165175875603865,1.0221983695652175,1.027942551388291,1.0337366128516623,1.0395673939425918,1.0454222408026757,1.051289143374741,1.0571565448113207,1.0630131615704999,1.0688481280193238,1.0746511330773834,1.0804122406126482,1.0861217195456325,1.0917701863354037,1.0973487398999615,1.1028487914759726,1.1082619033553875,1.1135799287856072,1.1187951446952804,1.1239000898120854,1.128887410942638,1.13375,1.1384811242364357,1.1430742716500357,1.147523003932485,1.151821090462833,1.1559626358695652,1.1599419319358177,1.1637533165011982,1.1709599869396699,1.1745586852006689,1.1781756917938933,1.1817996541501976,1.1854194334341288,1.189024223312784,1.1926036634460548,1.1961476982097188,1.1996464416058394,1.2030902941871455,1.2064700549343135,1.2097767857142858,1.2130016815063214,1.2161361853184323,1.2191720982821526,1.2221014492753624,1.22491636994003,1.2276092074895772,1.2301726329118603,1.2325995152761458,1.2348828011015465,1.237015625,1.2389914440415348,1.2408037757437071,1.2424463348518755,1.2439129993647657,1.2451978052682329,1.2462949414715718,1.2471987449373443,1.2479036959961476,1.2484044138381871,1.2486956521739132,1.2488137257797731,1.2488010768921094,1.2486616743631636,1.2483993902439026,1.2480180027173913,1.2475211989261394,1.2469125776978651,1.246195652173913,1.2453738523443532,1.2444505274936062,1.2434289485602594,1.2423123104145601,1.241103734056924,1.2398062687406297,1.2384228940217392,1.2369565217391305,1.2354099979274134,1.233786104665364,1.2320875618623999,1.2303170289855072,1.2284771067289215,1.2265703386287625,1.2245992126247327,1.2225661625708886,1.220473569697415,1.2183237640252456,1.216119025735294,1.213861586493987,1.211553630736715,1.2091972969107552,1.2067946786791486,1.2043478260869567,1.2018262532735413,1.1992024666629315,1.1964828725961538,1.193673746672582,1.190781237068252,1.1878113677536233,1.1847700416143216,1.181663043478261,1.1784960430524012,1.1752745977722774,1.1720041555673055,1.1686900575447572,1.1653375405951751,1.1619517399219081,1.158537691497322,1.1551003344481605,1.1516445133724256,1.148174980590062,1.1446963983296414,1.1412133408531584,1.1377302965209737,1.1342516697988623,1.1307817832090497,1.1273248792270532,1.123885122126077,1.1204665997706422,1.117073325361078,1.1137092391304348,1.1103782099953277,1.1070840371621622,1.1038304516901443,1.1006211180124224,1.0974441991243962,1.0942843100711812,1.0911397668370522,1.0880089149504195,1.0848901288387602,1.081781811200378,1.0786823923924806,1.0755903298350824,1.0725041074302575,1.0694222349962839,1.066343247716235,1.0632657056005894,1.0601881929634471,1.0571093179119475,1.0540277118485082,1.0509420289855074,1.0478509458720457,1.044753160932447,1.041647394016148,1.03853238595866,1.0354068981532831,1.0322697121332627,1.0291196291640996,1.0259554698457223,1.0227760737242448,1.0195802989130436,1.016367021722891,1.0131351363008971,1.0098835542780118,1.0066112044248545,1.0033170323156437,1]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()

def hudsonFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [34.78260869565217,35.03012907608696,17.647163722826086,11.858338994565218,8.968002717391304,7.237027853260869,6.085705389492754,5.265586180124224,4.652445652173913,4.177272041062802,3.798658288043478,3.4902529026679843,3.234488224637681,3.0192033340301,2.83571185947205,2.6776426630434784,2.5402173913043478,2.41978300831202,2.313498263888889,2.219119171910755,2.1348505434782608,2.059239939182195,1.991098999505929,1.9294452977315688,1.8734601449275363,1.8224565217391304,1.7758531040969898,1.7331540609903382,1.6939343944099379,1.657828312406297,1.6245187952898552,1.5937291812762973,1.565217391304348,1.5389168519433465,1.5147568334398978,1.49253299689441,1.4720637077294687,1.4531865085193891,1.4357560426201375,1.4196422972408027,1.4047282608695653,1.3909079235153765,1.3780853713768115,1.3661740078361981,1.3550951086956522,1.3447765700483092,1.3351525578922496,1.3261632024745607,1.3177536231884057,1.3098730728704526,1.3024748641304347,1.295516304347826,1.288957984949833,1.2827631511484825,1.2768977707326894,1.2713305953557315,1.2660326086956524,1.2609765327040428,1.2561369705772114,1.2514905351879146,1.2470153985507246,1.242690885602281,1.2384976551542777,1.2344178636128365,1.2304347826086957,1.226511810200669,1.2226330904150198,1.2188121045587281,1.2150615409207162,1.2113935983774418,1.207819778726708,1.204350696570729,1.2009963768115943,1.1977667603484217,1.194670562206228,1.191716259057971,1.1889125518449657,1.1862665866741953,1.1837860141443701,1.1814776675151348,1.1793480383831523,1.177403507447665,1.1756501441542948,1.1740935208224201,1.172738944422878,1.1715918718030691,1.1706569135490394,1.1699386634807596,1.169442085597826,1.1691709666585248,1.1691296799516908,1.1693220332656473,1.1697516688327032,1.1704222548503973,1.1713373034227568,1.1725,1.1739133973052536,1.1757005336732407,1.1779492707409052,1.1806116532169522,1.1836416440217392,1.1869950293263023,1.1906293291773231,1.1945037133284087,1.1985788402748747,1.2028171098602485,1.207182100466571,1.2116388313947584,1.2161536175271739,1.2206940098972876,1.2252287395009882,1.2297275876419898,1.2341616423233697,1.2385027895344363,1.2427239762109077,1.2467990902646504,1.2507029200243627,1.2544110431763285,1.2579000811763081,1.2611472272332847,1.2641305055480072,1.2668286667939275,1.2692211583437276,1.2712880269088018,1.2730101683029453,1.2743688858695652,1.2753461438923395,1.2759244747090037,1.2759391062099763,1.2756033131270903,1.275087835525224,1.274400938735178,1.273550384112455,1.2725439548183,1.2713889517914654,1.2700927109974425,1.2686621062757855,1.2671040583648394,1.2654250444752893,1.263631599378882,1.2617298315602836,1.2597259166411514,1.2576256199642748,1.2554347826086958,1.2531588502623687,1.2508033520696844,1.2483734356514347,1.245874339012926,1.2433109600689378,1.240688179347826,1.2380107199737258,1.235283180778032,1.2325100403612532,1.229695660996612,1.2268442923825387,1.2239600752508362,1.2210470448369566,1.218109134218492,1.2151501775276867,1.2121739130434783,1.2091093001029571,1.2058920843397747,1.2025358585206054,1.1990538838812301,1.195459100172925,1.1917641353457307,1.1879813148838194,1.1841226708074533,1.180199950355351,1.1762246243606138,1.1722078953327613,1.1681607052578362,1.1640937431279845,1.1600174522113944,1.1559420370729814,1.1518774703557313,1.1478334993321666,1.1438196522349782,1.1398452443754554,1.1359193840579709,1.1320509782984025,1.1282487383540374,1.1245211850721668,1.1208766540642723,1.1173233007123973,1.1138691050140253,1.1105218762715066,1.1072892576318223,1.104178730482229,1.101197618707094,1.0983530928110061,1.0956521739130436,1.0930571004167606,1.0905241483639623,1.088051316889632,1.085636645962733,1.0832782153498124,1.080974143610013,1.0787225871203847,1.076521739130435,1.074369828844906,1.0722651205337925,1.0702059126686658,1.068190537084399,1.0662173581654295,1.0642847720557198,1.0623912058916194,1.0605351170568562,1.058714992458914,1.0569293478260868,1.055176727024521,1.0534557013945858,1.05176486910594,1.0501028545306785,1.0484683076339736,1.0468599033816426,1.0452763411640953,1.0437163442361388,1.0421786591721263,1.0406620553359682,1.039165324365532,1.0376872796709753,1.0362267559465783,1.0347826086956522,1.0334154400664253,1.032178091333205,1.0310579607893604,1.0300426678108314,1.0291200480290015,1.0282781486294896,1.0275052237730566,1.0267897301349325,1.026120322559013,1.0254858498234858,1.0248753505145698,1.0242780490051584,1.0236833515352688,1.0230808423913045,1.0224602801812352,1.0218115942028987,1.0211248809027151,1.0203904004222062,1.0195985732297819,1.018739976835353,1.0178053425854037,1.016785552536232,1.0156716364031422,1.0144547685834502,1.0131262652512223,1.0116775815217391,1.0101003086837432,1.0083861714975846,1.006527025557441,1.004514854715851,1.0023417685688407,1]
    factorsListG = [0,0.665132472826087,0.7029211956521739,0.7394531249999999,0.7747282608695653,0.8087466032608696,0.8415081521739131,0.8730129076086957,0.9032608695652175,0.9322520380434782,0.9599864130434783,0.9864639945652175,1.0116847826086957,1.0356487771739131,1.0583559782608696,1.079806385869565,1.1,1.118936820652174,1.136616847826087,1.1530400815217392,1.1682065217391304,1.1821161684782608,1.1947690217391305,1.206165081521739,1.2163043478260869,1.2251868206521739,1.2328125,1.2391813858695653,1.2442934782608697,1.248148777173913,1.2507472826086956,1.2520889945652174,1.2521739130434784,1.2515069169960473,1.2506224024936063,1.249561820652174,1.2483620169082126,1.2470553943889542,1.2456709453661328,1.2442351240245262,1.242771739130435,1.2413018624072112,1.239844558747412,1.2384175145348837,1.2370368083003953,1.2357167119565218,1.234470256379962,1.2333097247918594,1.232246376811594,1.2312902062999114,1.2304504076086957,1.2297357869778347,1.229154473244147,1.228713661300246,1.228420013083736,1.2282800148221344,1.2282996894409937,1.2284843392448512,1.2288389008620688,1.2293682640935888,1.2300769927536233,1.2309690729686387,1.2320482336956522,1.233318236714976,1.2347826086956522,1.236369408444816,1.2380043642951253,1.2396868409312136,1.241416240409207,1.2431919994486451,1.2450135869565218,1.2468805017605633,1.248792270531401,1.2507484458755211,1.2527486045828438,1.2547923460144927,1.256879290617849,1.2590090785573123,1.2611813684503903,1.26339583619978,1.2656521739130435,1.2679500889023083,1.270289302757158,1.2726695504845469,1.2750905797101448,1.2775521499360614,1.280054031850354,1.282596006684158,1.2851778656126482,1.2877994091963851,1.2904604468599035,1.2931607964046823,1.295900283553875,1.2986787415264143,1.301496010638298,1.3043519379290618,1.3072463768115943,1.3103702095472882,1.3138805318322981,1.3177284049736497,1.3218668478260869,1.3262505717283684,1.3308360640451833,1.3355816668425495,1.3404473244147157,1.3453943452380952,1.3503854978465957,1.3553851013307598,1.3603587962962962,1.3652733284303948,1.370096652667984,1.3747980317273796,1.3793478260869565,1.3837172951135053,1.3878787066170863,1.3918054406899811,1.395471795352324,1.3988528021646227,1.401924339075166,1.4046632375776398,1.4070471014492754,1.4090541344771828,1.4106632550784035,1.4118542053287382,1.4126073807854138,1.412903668478261,1.4127245621980675,1.4120522723382403,1.4092252406681833,1.407197428929766,1.4048124144332892,1.4020956851119895,1.3990719623447205,1.3957652295587282,1.3921987595611918,1.3883951406649617,1.3843763016701047,1.3801635357592943,1.3757775233617453,1.371238354037267,1.366565547429078,1.361778073331292,1.3568943709144117,1.3519323671497583,1.3469094944715143,1.3418427077129242,1.3367485003512276,1.3316429200940072,1.3265415838379049,1.3214596920289854,1.3164120424524905,1.311413043478261,1.3064767267867292,1.3016167595990966,1.2968464564340814,1.292178790412486,1.2876264041297425,1.2832016201155751,1.278916450898961,1.2747826086956522,1.2707070280853363,1.266592860976919,1.262445818885036,1.2582714740190881,1.2540752635046113,1.2498624934520692,1.2456383428794584,1.241407867494824,1.2371760033444816,1.2329475703324808,1.2287272756165777,1.2245197168857431,1.220329385524001,1.2161606696651674,1.2120178571428573,1.2079051383399209,1.2038266089412921,1.19978627259404,1.1957880434782608,1.1918357487922706,1.1879331311554167,1.1840838509316771,1.180291488477073,1.1765595463137997,1.1728914512338426,1.1692905563347358,1.1657601429900024,1.1623034227567068,1.1589235392224522,1.1556235697940505,1.1524065274300022,1.1492753623188405,1.1462213257138434,1.1432315595584939,1.1403028650188127,1.13743207604883,1.134616123217143,1.131851999101065,1.1291367247241644,1.1264674231487772,1.1238412324417315,1.12125538938065,1.118707143359124,1.116193839330909,1.1137128326318928,1.1112615711732272,1.1088375111583701,1.106438198536136,1.1040611855919753,1.1017041116718427,1.0993646206277046,1.0970404408230363,1.094729303413324,1.0924290216438948,1.090137409946916,1.0878523527136172,1.0855717733326238,1.0832936040804497,1.0810158440819189,1.0787365288414033,1.0764537006012689,1.0741654655674697,1.07186995439535,1.069565331121409,1.0672896286231885,1.0650777267097922,1.0629231708484965,1.0608196150883749,1.0587608382306697,1.056740708810846,1.0547532199175371,1.0527924499054184,1.0508525924554488,1.048927935965661,1.0470128660528446,1.0451018634928266,1.043189504452308,1.0412704495648464,1.0393394554877946,1.0373913640561312,1.0354211027175322,1.033423682763514,1.0313941976042504,1.029327821085815,1.0272198047654864,1.0250654806472168,1.0228602531069162,1.0205996027835456,1.0182790797190118,1.0158943094004755,1.0134409833280669,1.0109148640234442,1.0083117799550771,1.0056276250236535,1.0028583577343875,1]
    factorsListB = [0,0.7027173913043478,0.7391474184782609,0.7744961503623188,0.8087635869565217,0.8419531250000001,0.8740658967391304,0.9050999611801241,0.935054347826087,0.9639304045893721,0.9917289402173914,1.0184489253952569,1.0440896739130434,1.0686520171404683,1.0921365489130435,1.114542572463768,1.1358695652173914,1.1561181265984655,1.1752887228260869,1.1933808280892448,1.2103940217391305,1.2263287719979297,1.2411854619565217,1.2549636696597353,1.267663043478261,1.2792839673913043,1.289826766304348,1.299291087962963,1.3076766304347827,1.314983719077961,1.3212126358695653,1.3263630785413745,1.3304347826086957,1.3339395998023715,1.3373951007033247,1.3408108501552796,1.344195350241546,1.3475557248824912,1.3508983481121282,1.354229375696767,1.357554347826087,1.3608778499469778,1.3642040307971015,1.3675370481547018,1.3708806818181818,1.3742379981884059,1.3776117970226844,1.3810050011563366,1.3844202898550726,1.3878597770629992,1.3913254076086958,1.3948193067988064,1.3983434364548495,1.4018992898892535,1.4054882497987118,1.4091119071146245,1.4127717391304349,1.4164688215102974,1.4202041557346328,1.4239789632461313,1.427794384057971,1.4316512050071277,1.4355501621669005,1.439492214458247,1.4434782608695653,1.4476335179765887,1.4520560564888012,1.4567077993186242,1.4615529092071613,1.4665573802772527,1.4716891498447204,1.4769182007807717,1.4822161835748793,1.4875560694609888,1.4929122906874266,1.4982608695652175,1.503579090389016,1.5088451969226426,1.5140385486343366,1.519139765066043,1.5241304347826088,1.5289928458803006,1.5337101504506894,1.538266517155579,1.5426468685300208,1.5468366368286444,1.550821931875632,1.5545896973388307,1.5581274703557313,1.5614231573644357,1.5644652022946859,1.567242743669374,1.5697453922495275,1.5719630230247779,1.573885941836263,1.5755050414759726,1.5768115942028986,1.5779835275661138,1.579192546583851,1.580421058410189,1.5816521739130434,1.582869672836849,1.5840579710144926,1.585202089489236,1.5862876254180602,1.5873007246376811,1.5882280557834292,1.589056785859407,1.5897745571658615,1.5903694654966096,1.5908300395256918,1.5911452213082649,1.591304347826087,1.5912971335128896,1.5911136536994661,1.5907443289224954,1.5901799100449776,1.589411464139725,1.5884303610906412,1.5872282608695651,1.5857971014492755,1.5841290873158462,1.5822166785459728,1.5800525804171084,1.5776297335203366,1.5749413043478262,1.5719806763285025,1.5687414412872305,1.5614036629486856,1.5573126567725752,1.5529637521262032,1.5483757411067194,1.54356685063542,1.5385547635463983,1.5333566387379227,1.5279891304347826,1.5224684066070295,1.5168101665879017,1.5110296579312639,1.5051416925465837,1.4991606621473172,1.4931005530465402,1.4869749603317879,1.4807971014492756,1.474579829226012,1.4683356443567601,1.4620767073813221,1.4558148501762633,1.449561586983878,1.443328125,1.4371253745411028,1.4309639588100687,1.4248542232789856,1.4188062447063805,1.4128298398053998,1.4069345735785954,1.4011297673341871,1.3954245063979087,1.3898276475338394,1.3843478260869566,1.3789220733189307,1.3734836285560923,1.3680352260602826,1.3625795334040298,1.357119153491436,1.3516566265060241,1.3461944317885968,1.3407349770113548,1.3352806505458903,1.3298337471027812,1.3243965201301486,1.3189711706703426,1.3135598488745601,1.3081646554652362,1.302787643148292,1.297430805914958,1.2920961286769221,1.2867855159608572,1.281500841594304,1.2762439377641908,1.271016596167127,1.265820569121775,1.2606575706447494,1.2555292774914342,1.2504373301630434,1.2453833452949683,1.2403688708839515,1.2353954558676863,1.2304646051695134,1.2255777920301774,1.2207364699521968,1.2159420289855072,1.2111528761404595,1.2063309023595081,1.2014826113085284,1.1966143739255213,1.1917324641187101,1.186842996884607,1.1819519749733722,1.1770652704653533,1.172188670269576,1.167327815173671,1.162488245274684,1.157675392040308,1.1528945809583775,1.148151034109197,1.143449872663306,1.1387961295137439,1.1341947107570989,1.1296504593685301,1.1251681164518081,1.1207523236419452,1.116407665307971,1.1121386103686255,1.1079495544742164,1.1038448118741195,1.0998286124007588,1.0959051180133128,1.0920784098064944,1.0883524946732954,1.0847313069837572,1.0812187102183706,1.077818493797524,1.074534388950893,1.0713905495169083,1.0684009324499808,1.0655540678195627,1.062838696233195,1.0602437503337407,1.0577583552398393,1.0553718243797643,1.0530736554330256,1.0508535218207689,1.0487012825593414,1.0466069692775786,1.0445607690663574,1.0425530480717415,1.0405743298933023,1.038615296731456,1.0366667860832768,1.0347197875205778,1.0327654395478687,1.0307950265378982,1.0287999735673836,1.026771853293797,1.0247023656959036,1.0225833505376336,1.0204067791996296,1.0181647488391066,1.015849487835428,1.0134533447181044,1.0109687899950868,1.0083884145287965,1.005704924685626,1.0029111421524919,1]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()

def redtealFilterFunction( targetImage, inputPathPy, outputPathPy, colorFactor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('G') # use data from green channel for blue here
    temp_img = Image.merge('RGBA',(R,G,B,A))
    temp_img = ImageEnhance.Color(temp_img)
    temp_img = temp_img.enhance(colorFactor)
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def nashvilleFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [0,0.06754117398648649,0.0673828125,0.06737401463963964,0.06752797719594594,0.06783150337837837,0.06829778997747749,0.06892118122586872,0.0697021484375,0.07063802083333333,0.07173511402027027,0.07299024877149878,0.07440130560247749,0.07596884745322247,0.0776970469353282,0.0795801661036036,0.08162214949324324,0.0838229083863275,0.08618090746996998,0.0886949346550498,0.09136797930743243,0.09419869087837839,0.09718716408169534,0.10033347715922444,0.1036376953125,0.10709881756756758,0.11071802722193348,0.1144943771896897,0.11842894093870657,0.12252173374883504,0.12677188907657658,0.1311795035963383,0.13574466189822637,0.1398195958742834,0.14289329540937998,0.14515640082046333,0.146776903856982,0.14790534833820307,0.1486764313655761,0.14921103495322247,0.14961729307432434,0.14999407753790375,0.15042958695302447,0.15100442921118795,0.15179188421375922,0.15285813156906908,0.1542647436839013,0.1560674911946521,0.15831639745213966,0.16105955684638723,0.16433910472972976,0.1681954242845787,0.17266528472583162,0.17778168424910762,0.18357713181931934,0.19008033246314499,0.19731794084821427,0.20531566722972974,0.21409653861835973,0.2236829155691709,0.23409478814752255,0.24535083559481613,0.25746938344594594,0.2704671747640498,0.28435949377111486,0.2992431133056133,0.31512216229013107,0.33187879752420335,0.3494028840421304,0.3675891414512339,0.38633981358590735,0.40556190818899884,0.42516723266234985,0.4450735115466495,0.4652022033646823,0.4854786036036037,0.5058328077769382,0.526198028639435,0.5465109039327789,0.5667116137102293,0.5867426691828548,0.6065502351309644,0.6260826196337343,0.6452904629497721,0.6641273842201577,0.6825485641891893,0.7005114216687618,0.7179757882882883,0.734902571694564,0.7512550296082601,0.7669977594782283,0.7820970599290913,0.7965206948626616,0.8102375308776519,0.8232181805725273,0.8354342160828593,0.8468583940385699,0.8578019969873224,0.8685890530198567,0.8792132420062108,0.8896682326858109,0.8999479445410759,0.9100467942666932,0.9199592872605615,0.929679886466996,0.9392036428169241,0.9485256695005738,0.9576411390581587,0.9665455250172047,0.9752344670143195,0.9837037632447789,0.991949244430241,0.9999668901951617,1.007753172835446,1.0153042253808087,1.0226165448736781,1.0296868629135603,1.0365116844609032,1.043087968463697,1.049412554295367,1.0554824966568133,1.0612948385498102,1.0668469362677226,1.0721361247871348,1.0771596122016676,1.081915012668919,1.0863999113510832,1.0906118655565014,1.0982394663013306,1.101720455431393,1.1049994076555087,1.1080840639556462,1.110981734054308,1.113699509473326,1.1162443693693693,1.118623039112182,1.1208420958738163,1.1229078305547395,1.124826447963251,1.1266039284960183,1.128246082893066,1.1297585582116008,1.1311468435491874,1.132416367172837,1.1335722255795666,1.134619511219803,1.1355631779738922,1.1364079566660201,1.1371585396874433,1.137819406320383,1.1383950482845222,1.1388896654544143,1.1393075204110361,1.139652679325531,1.139929060865301,1.1401406101113132,1.1402910035209373,1.1403839915246536,1.1404231057044665,1.1404118718327703,1.1403197524970623,1.1401179011042293,1.139812223434132,1.139408561691455,1.138912496480856,1.1383295136839588,1.1376650072953756,1.1369241643289496,1.136112205204002,1.1352339946219197,1.1342944764254386,1.1332984027586817,1.1322504540306204,1.1311551272109934,1.130016854186776,1.128840041102004,1.1276288826896281,1.1263875164885744,1.1251200244413408,1.1238303611228415,1.1225223937140698,1.1211999406579485,1.1198666828489607,1.1185262570229877,1.1171822034502832,1.1158380217414996,1.1144970837210038,1.1131627245700655,1.1118381914280353,1.1105266978018316,1.1092313380799403,1.107955176551063,1.1066874189046965,1.1054147213871812,1.1041363648053102,1.102851610978006,1.1015597199654446,1.1002600167639232,1.098951790201005,1.0976343763196792,1.0963071079620899,1.094969331181429,1.0936204211687441,1.092259749193702,1.090886698793878,1.0895006814925134,1.0881010883080773,1.0866873536932742,1.0852589229246816,1.0838152204241072,1.082355728432817,1.0808798844932235,1.0793871754333009,1.077877089964618,1.0763491186385332,1.0748027690776714,1.0732375503789,1.07165298821345,1.070048616916092,1.0684239717900608,1.0667785965493917,1.06511205799074,1.063423908489312,1.0617137305064552,1.060008687887106,1.0583329090117497,1.0566814725548614,1.0550495290597959,1.0534323209800618,1.0518251878534446,1.050223528495013,1.0486228317161197,1.0470186673133284,1.0454066702388236,1.0437825567630463,1.0421421192569358,1.0404812071856024,1.0387957570987645,1.037081759749502,1.035335283021669,1.0335524515064494,1.0317294589637618,1.0298625601105664,1.0279480727520673,1.0259823714444076,1.0239618930468792,1.0218831321214585,1.0197426347807375,1.0175370100744512,1.0152629147091428,1.0129170636000129,1.010496220533452,1.0079972016838115,1.0054168737703346,1.0027521520552967,1]
    factorsListG = [0,0.047112542229729736,0.02783203125,0.010038358671171171,-0.006294869087837838,-0.02114125844594595,-0.03451840512387388,-0.0464187680984556,-0.05684187605574325,-0.06579039977477479,-0.07326330236486486,-0.07925752457002457,-0.08377982474662161,-0.0868227001039501,-0.08839210304054054,-0.08848536036036037,-0.08710211676520271,-0.08424210055643878,-0.07990803303303304,-0.07409789518136559,-0.0668113914695946,-0.058048282657657664,-0.04781077242014742,-0.036096090995887196,-0.022906329180743243,-0.008240076013513514,0.007900816982848233,0.02551868274524525,0.0446117504222973,0.06518122378844361,0.08722638654279279,0.11074746621621623,0.13574383709881757,0.16222134776822278,0.1900027325119237,0.21884200048262548,0.24851902683933938,0.27883748402118336,0.30962171052631576,0.3407140614171864,0.37197397592905407,0.40327267530487804,0.4344942738497426,0.46553427973758643,0.4962971005451475,0.5266962274774775,0.5566521004700353,0.5860919305276021,0.6149489944045609,0.6431625542953668,0.6706762035472974,0.6974379595588235,0.7234003459589398,0.7485189715068843,0.772752977586962,0.7960642371775185,0.8184175822725628,0.839780081273708,0.8601213012581548,0.8794128725521073,0.8976280968468469,0.9147424592240806,0.9307323878187664,0.9455762263379451,0.959253672006968,0.9723486632666322,0.9854319429514743,0.9984660208249294,1.0114160000993642,1.0242486244736584,1.0369325380067569,1.0494385230300725,1.0617386185013138,1.0738065762680489,1.0856173886618883,1.097147557713964,1.1083748221906116,1.1192779058989997,1.1298367929227306,1.140032480809528,1.149846752269848,1.1592624525567234,1.168263263740112,1.176833654296239,1.184958518088401,1.1926239256259936,1.1998164418506443,1.206522946033318,1.2127315136958694,1.2184300148990284,1.2236075919669671,1.2282534294253045,1.2323571820376764,1.2359090914250945,1.2388998144587406,1.2413202624911097,1.24316186303491,1.2444295938980219,1.2451620296556123,1.2454001853415917,1.245183567356419,1.2445497255067568,1.2435352545790277,1.2421749438303595,1.2405024982539632,1.2385499617921494,1.2363486671739548,1.2339285291424604,1.2313181101022896,1.2285454085823209,1.225637045070639,1.222618918538471,1.2195156495083255,1.2163514541228175,1.2131494673127075,1.2099317898061106,1.2067203290642474,1.2035355668168168,1.200397849683635,1.1973265076723258,1.1943404464034346,1.1914577283895464,1.188695932100133,1.1860721179926115,1.1836027961870643,1.1813037901182433,1.179190577994289,1.177278098564854,1.1740269975644249,1.1725321494120322,1.1710912516762948,1.169699579062372,1.1683524491655661,1.1670452701126968,1.165773781594094,1.1645336060152525,1.1633206862485206,1.1621309393207746,1.1609605896363993,1.1598057338169643,1.1586627196095696,1.1575280441092501,1.1563981178238991,1.1552696342582818,1.1541393326246505,1.1530039510829324,1.1518604063246922,1.1507056537904037,1.1495368192227462,1.1483509730433559,1.147145350674557,1.1459172168802232,1.1446639510604355,1.1433830006828054,1.142071793946164,1.140727909587773,1.1393489460051214,1.137932645919753,1.1364767258414075,1.1349789181271115,1.1334812330163044,1.1320229734943277,1.1305980299701544,1.1292005223354071,1.127824593058968,1.1264646450031546,1.1251151755821127,1.1237707346716137,1.1224261573194867,1.1210762836595787,1.1197161131114668,1.1183407230245326,1.1169453808486955,1.1155253490626942,1.1140761492519304,1.1125932548204278,1.111072353305371,1.1095091550139502,1.1078995029749548,1.1062393325943132,1.104524632648014,1.1027515707081137,1.1009162899451705,1.0990150711651274,1.0970442755889336,1.0950003249532294,1.0928797351778166,1.0906790787629386,1.0883950356606606,1.0860243209903984,1.0835637013915913,1.0810100795986417,1.0783598242378956,1.0756156370811856,1.0727838358941875,1.069870626341225,1.0668820378416963,1.063824011333777,1.0607023683397987,1.057522813951647,1.0542909068992032,1.0510121448364749,1.0476918845849006,1.044335377930205,1.0409478063715392,1.0375342187653749,1.03409956640574,1.0306487212309967,1.0271864619366675,1.0237174761955037,1.020246331542406,1.016777540456878,1.0133155461662147,1.0098646625962997,1.0064291694492458,1.0030132213512342,0.9996209419565015,0.9962563338541022,0.9929233867857584,0.9896259429706696,0.9863678347995904,0.9831528107499392,0.9799845372672631,0.9768666153248674,0.973784883516329,0.9707219275068764,0.9676764236488348,0.9646471293970781,0.9616327662824192,0.9586321067585929,0.9556439445355462,0.9526670941213304,0.9497003762161438,0.9467426457782904,0.943792763217007,0.94084963621593,0.9379121769737498,0.9349792882471823,0.9320499187651957,0.9291230485245988,0.9261976333828643,0.9232726873551624,0.9203472271099226,0.9174202583931589,0.9144908570480558,0.911558046887875,0.9086209343199475,0.9056785869515244,0.9027301271174224,0.8997746779983108,0.896811350459648,0.8938392956642469,0.8908576912355785,0.887865701769991,0.8848625179062335,0.8818473300418339]
    factorsListB = [65.67601879222973,65.9923194679054,33.172422666807435,22.24392507742117,16.78782200168919,13.520309860641893,11.346789660754505,9.798147547659267,8.639826594172298,7.741517396302553,7.025034311655406,6.440621640816953,5.955111116976352,5.545537048466736,5.195499140323359,4.892966990427928,4.62892027158995,4.396460310264309,4.190220005161411,4.005965643892248,3.840306297508446,3.6904994419642856,3.554300594095516,3.4298550418625147,3.315618291631475,3.2102919130067566,3.112777741683992,3.0221403043668666,2.937577295487452,2.8583984375,2.784003730292793,2.7138714445292065,2.647545067039696,2.5848905546171173,2.525829224215024,2.4700598757239383,2.4173151422907284,2.3673558482468957,2.3199683415940613,2.274960883359321,2.232160908467061,2.1914126874588007,2.152575322253057,2.115520714664519,2.0801333115786242,2.046306364958709,2.0139441305265864,1.9829573277566133,1.9532654908326297,1.924793914609763,1.8974743982263516,1.8712433136261262,1.8460426885719854,1.821818926090005,1.7985216661974475,1.7761046913390666,1.7545255565275097,1.733743869280465,1.713722477865797,1.694426972987288,1.6758247994087838,1.6578857530045414,1.6405817911535527,1.623886023300086,1.6077740643475507,1.5922461749610188,1.5772946019528051,1.5628858583980436,1.5489874568387323,1.5355693669212693,1.5226032743122588,1.5100620881114388,1.4979205890460774,1.4861549397213996,1.4747420562454345,1.463660789695946,1.4528907569679055,1.4424126338188838,1.4322082561828655,1.422260045597417,1.4125516324429899,1.4030672925529697,1.3937922297297298,1.3847120428504558,1.3758133307693856,1.36708316772655,1.3585093826111723,1.350080212216527,1.341784278063575,1.3336110096226845,1.3255503061655407,1.3175923659322097,1.3097276698828586,1.301947534101642,1.2942432230268832,1.2866066467371977,1.2790299149246904,1.2715031498154081,1.2640246871552676,1.256599728279416,1.2492327385979731,1.241928398657011,1.234691076071476,1.2275247125918394,1.220433605931653,1.213421513030888,1.2064921735562213,1.1996490640392146,1.1928956544435059,1.1862354084660924,1.1796714239097053,1.1732068058345506,1.1668445484058279,1.160587423014829,1.1544383353336891,1.1483998604582843,1.1424745984535183,1.1366650604931856,1.1309736726265462,1.1254027793549854,1.119954537056588,1.1146311398885975,1.1094347100686752,1.104367408090255,1.0994310054762424,1.0946274282094597,1.0899586458668489,1.085426462079698,1.0767672650848525,1.072616558114605,1.0685745532030122,1.0646359805295351,1.0607954310925118,1.0570478543200383,1.0533880560247748,1.0498113829304947,1.0463131249691755,1.0428886129675872,1.0395335019990766,1.036243382752172,1.0330142049879003,1.0298418466882375,1.0267223011363635,1.0236518103797156,1.020626583614865,1.0176429790904988,1.0146974990376219,1.0117866956377832,1.0089072136314168,1.006055787232545,1.0032292808640595,1.0004245546430477,0.9976385939018062,0.9948685051224114,0.9921114694583698,0.9893646134490862,0.9866253049551343,0.9838908531875429,0.9811587180488271,0.9784263817039696,0.9756999135077431,0.9729874731502336,0.9702898144741752,0.9676075924676584,0.96494140625,0.962291999501384,0.9596599005325498,0.9570457429038972,0.9544501451803135,0.951873672558128,0.9493169155998104,0.9467804127710561,0.9442646900874865,0.9417703373160338,0.93929777992278,0.9368475836676521,0.9344202642459727,0.9320162145554965,0.9296360030268572,0.9272800388278905,0.9249487949944939,0.9226426979112525,0.9203622006996751,0.9181076749091143,0.9158796267234296,0.9136783740645888,0.9115043339106988,0.9093579143679917,0.9072394799933863,0.9051494223973151,0.903088090442373,0.9010558257231841,0.8990484156740128,0.8970612584132941,0.8950940085217429,0.8931464286252931,0.8912182526752641,0.8893091866724679,0.8874190088427781,0.8855474688555743,0.8836942885341031,0.881859260540708,0.8800421166143824,0.878242626099215,0.8764605950271919,0.8746957691345777,0.8729478990709459,0.8712168354502339,0.8695023370316339,0.8678041985903315,0.8661222187920297,0.8644562001011921,0.8628059177134882,0.8611712126937833,0.8595518983736644,0.8579477609934153,0.8563586515482937,0.8547843632318529,0.8532247231445915,0.8516795915233416,0.8501487714206005,0.8486320991599708,0.8471294140009544,0.8456405580734195,0.8441998932526277,0.8428366769874134,0.8415432873333135,0.8403121203028687,0.8391357911712204,0.8380070149548325,0.836918661381552,0.8358636946735933,0.8348351998390557,0.833826408289299,0.8328305824108684,0.8318412385836579,0.8308518634090974,0.8298561638549001,0.8288478693864497,0.8278208689646679,0.8267690982200432,0.8256866748188659,0.8245677317942943,0.8234065254018748,0.8221974460709116,0.820934908386378,0.8196134708136147,0.8182277529782177,0.8167724609375,0.8152423986486487,0.8136324397300999,0.8119375522634801,0.8101527838864372,0.8082732342486434,0.8062941057440712,0.8042106628417969]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def hefeFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [0,0.4079993206521739,0.4284646739130435,0.4483525815217391,0.4676630434782609,0.4863960597826087,0.5045516304347827,0.5221297554347826,0.5391304347826087,0.5555536684782608,0.5713994565217392,0.5866677989130434,0.6013586956521739,0.6154721467391304,0.629008152173913,0.6419667119565218,0.6543478260869565,0.6661514945652174,0.6773777173913044,0.6880264945652174,0.6980978260869566,0.7075917119565217,0.7165081521739131,0.7248471467391304,0.7326086956521739,0.7397927989130434,0.7463994565217391,0.7524286684782608,0.7578804347826088,0.7627547554347827,0.7670516304347826,0.7707710597826086,0.7739130434782608,0.7767066040843215,0.7793947810102302,0.7819977678571428,0.7845335144927535,0.787017571239718,0.7894638515446225,0.7918852773132665,0.7942934782608695,0.7966985352598092,0.799109569099379,0.8015352470930232,0.8039834486166008,0.8064609752415459,0.8089740370982987,0.8115286771507864,0.8141304347826087,0.8167840505767524,0.8194938858695652,0.8222642929454391,0.8250992892976589,0.8280022687653814,0.8309763737922706,0.8340248270750987,0.8371506211180124,0.8403562404652937,0.8436439983133434,0.8470163388909359,0.8504755434782609,0.854023465342124,0.8576618381837308,0.8613925552104901,0.8652173913043478,0.8690426421404682,0.8727843997035573,0.8764583164341336,0.8800791240409208,0.8836604540800252,0.8872151591614906,0.890755607011635,0.8942934782608697,0.8978395808516973,0.9014041385135135,0.9049970561594203,0.9086277173913043,0.9123047977837381,0.9160365280100334,0.9198309369840396,0.9236956521739131,0.9276377147074611,0.9316638222428419,0.9357805542823469,0.9399941770186336,0.9443104619565217,0.9487349121587462,0.9532729728885557,0.9579298418972332,0.9627102925012214,0.9676188858695653,0.9726601693143813,0.9778384924385634,0.9831578351449276,0.9886220079787235,0.9942348398169336,1,1.0060496974450919,1.0124833629103815,1.019256422924901,1.0263260869565218,1.0336512591476539,1.0411924552429668,1.0489117243562684,1.0567725752508361,1.0647399068322982,1.072779942575882,1.0808601686306378,1.088949275362319,1.0970171021140807,1.1050345849802372,1.1129737074030552,1.120807453416149,1.1285097633705272,1.1360554919908468,1.1434203686200377,1.1505809595202399,1.1575146321070235,1.164199521002211,1.1706144957983193,1.1767391304347825,1.1825536740927058,1.1880390235210265,1.1931766967126192,1.1979488078541376,1.202338043478261,1.2063276397515528,1.2099013608353302,1.2158726459807887,1.2185213733277591,1.2209947000497843,1.2232975131752306,1.2254346804511278,1.2274109243186244,1.229230701489533,1.230898337595908,1.232418155942558,1.233794354521109,1.235030888332812,1.236131599378882,1.237100341119334,1.2379408584660134,1.2386566728108848,1.2392512077294686,1.2397279094827585,1.240090129913639,1.2403410141230407,1.2404836222091657,1.2405210746005981,1.240456295289855,1.2402921589313993,1.2400314645308925,1.239676937917377,1.2392312341191418,1.2386969396476157,1.2380765746934226,1.2373725952385075,1.2365873950880573,1.2357233078257452,1.2347826086956522,1.2337402739332972,1.2325743089103596,1.231291365197386,1.2298979321314951,1.2284003417325429,1.2268047734415923,1.2251172586891435,1.223343685300207,1.2214898017429894,1.2195612212276215,1.217563425661073,1.215501769464105,1.2133814832558432,1.2112076774112943,1.2089853454968944,1.206719367588933,1.204414513479489,1.202075445774304,1.1997067228868108,1.197312801932367,1.1948980415265433,1.192466704491161,1.1900229604716084,1.187570888468809,1.1851144792890715,1.1826576379149136,1.1802041744470761,1.177757851797381,1.175322330774097,1.1729011727688787,1.1704978979342135,1.1681159420289855,1.1657342500422394,1.1633302751008516,1.16090515476937,1.1584599709024235,1.1559958157174188,1.1535137593667655,1.1510148184878195,1.1485000318444294,1.1459703752805268,1.1434268473552518,1.14087038511994,1.138301948879076,1.1357224387758484,1.133132778697499,1.1305338336549569,1.1279264928505173,1.1253115878373987,1.1226899747670809,1.12006245331496,1.1174298481241027,1.1147929284834917,1.1121524889844068,1.1095092699380689,1.1068640323460774,1.1042175036158837,1.1015703978080127,1.0989234304816236,1.096277284886055,1.0936326511164667,1.0909901877080885,1.0883505556638722,1.0857143994443905,1.083092655495169,1.0804938122234513,1.077914873527581,1.0753528912134702,1.0728049824897357,1.0702682962399575,1.0677400490983202,1.0652174873866778,1.062697918367466,1.060178690796579,1.0576572008159402,1.0551308819539598,1.0525972177732583,1.0500537318995193,1.0474979894040215,1.0449275959401891,1.0423401969016384,1.0397334766010993,1.037105157469611,1.0344529981878257,1.031774797278796,1.0290683858257252,1.0263316311103488,1.0235624358831248,1.020758733388036,1.0179184941830843,1.0150397174675956,1.0121204370955421,1.0091587159084197,1.0061526485601135,1.003100358746749,1]
    factorsListG = [0,0.22523777173913043,0.23301630434782608,0.24072690217391304,0.2483695652173913,0.25594429347826086,0.26345108695652175,0.27088994565217395,0.2782608695652174,0.2855638586956522,0.29279891304347827,0.29996603260869564,0.3070652173913044,0.31409646739130437,0.32105978260869567,0.32795516304347827,0.3347826086956522,0.34154211956521735,0.3482336956521739,0.3548573369565218,0.36141304347826086,0.3679008152173913,0.3743206521739131,0.3806725543478261,0.3869565217391304,0.3931725543478261,0.39932065217391305,0.4054008152173913,0.4114130434782609,0.4173573369565217,0.4232336956521739,0.4290421195652174,0.43478260869565216,0.4404690587944664,0.44612072410485937,0.45174398291925466,0.4573445048309179,0.46292780552291424,0.4684988200800915,0.4740615419453735,0.4796195652173913,0.48517654758748674,0.4907357983954451,0.4962999241658241,0.5018712944664032,0.507452445652174,0.5130456935255199,0.5186527954440333,0.5242753623188406,0.5299152201641526,0.5355740489130435,0.5412530637254902,0.5469533862876255,0.5526763740771125,0.5584232840177134,0.564194972826087,0.5699922360248447,0.575816111270023,0.5816675646551724,0.5875472089167281,0.593455615942029,0.5993935985388453,0.6053619170757364,0.6113610140614217,0.6173913043478261,0.623456835284281,0.6295583209815546,0.6356913631570409,0.6418518222506393,0.6480360448172653,0.6542405861801243,0.6604619565217391,0.6666968599033817,0.6729424136390709,0.6791958908636897,0.6854544836956522,0.6917155320366133,0.6979767345426312,0.7042359078874024,0.710490764309301,0.7167391304347827,0.7229791498926463,0.7292090568663839,0.7354269660162388,0.7416310817805384,0.7478198929028133,0.7539919584175935,0.7601457083958022,0.7662796442687747,0.7723925256472888,0.7784831672705314,0.7845502493430483,0.7905925094517958,0.7966089221014494,0.8025985054347827,0.8085601401601831,0.8144927536231884,0.8205047484311968,0.8266883179902397,0.8330195638449714,0.8394755434782608,0.8460340548321137,0.8526737665174765,0.8593743404390038,0.8661162207357859,0.8728804347826087,0.879648725902379,0.8864036786367331,0.8931285225442834,0.899806946798963,0.9064232336956521,0.9129623849392872,0.9194099378881988,0.925751791554444,0.9319743397215866,0.9380645971172022,0.9440100262368816,0.9497983730490525,0.9554177989130435,0.9608570058458166,0.9661050724637682,0.971151298059648,0.9759853327690663,0.9805973013874161,0.9849776472650771,0.9891169836956522,0.9930062219634231,0.9966366933413214,1.003157914138861,1.006181281354515,1.009074868279124,1.0118432971014493,1.0144911786940178,1.0170229862913691,1.0194429347826088,1.0217551150895139,1.0239636226594733,1.026072434231254,1.0280852899202377,1.0300058229813664,1.031837684050262,1.0335844209277403,1.0352493634083306,1.0368357487922706,1.0383468422038982,1.0397858193120906,1.041155653837622,1.0424592391304348,1.0436995048511817,1.044879302536232,1.046001295709761,1.0470680778032038,1.0480822854504122,1.0490464868012424,1.0499630741584853,1.050834378483835,1.0516627795278317,1.0524505967941662,1.0531999846185398,1.0539130434782609,1.0545824859066972,1.0552003656736446,1.0557679443684984,1.0562864528101803,1.0567570919795786,1.0571810339182819,1.0575594225950273,1.057893374741201,1.058183980656676,1.0584323049872122,1.058639387474574,1.0588062436804853,1.0589338656854737,1.0590232227636183,1.0590752620341615,1.059090909090909,1.0590710686102924,1.059016624938935,1.0589284426615253,1.0588073671497584,1.058654225093082,1.0584698250119446,1.0582549577542173,1.0580103969754253,1.0577368996034078,1.057435206287985,1.0571060418362008,1.0567501156336725,1.056368122052565,1.055960740846682,1.0555286375341453,1.055072463768116,1.0545818578931065,1.0540477224338862,1.0534725560897436,1.0528588065661046,1.0522088718687927,1.051525101559069,1.0508097979708324,1.0500652173913043,1.0492935712064677,1.048497027012484,1.04767770969426,1.0468377024722932,1.045979047918876,1.0451037489447024,1.0442137697568787,1.0433110367892977,1.0423974396063032,1.0414748317805385,1.0405450317458274,1.039609823625923,1.038670958039906,1.0377301528850063,1.0367890940975735,1.0358494363929147,1.0349128039846724,1.0339807912844037,1.0330549635819932,1.0321368577075098,1.0312279826750934,1.03032982030944,1.02944382585543,1.0285714285714287,1.0277544535024155,1.0270266208156984,1.0263773253447614,1.0257961479786424,1.0252728515995824,1.024797377126654,1.0243598396621494,1.0239505247376313,1.0235598846566525,1.0231785349312523,1.0227972508094356,1.0224069638909359,1.0219987588286552,1.0215638701132626,1.0210936789385119,1.0205797101449277,1.0200136292395814,1.0193872394897592,1.018692479088388,1.017921418389166,1.0170662572094056,1.0161193221986569,1.015073064271255,1.0139200561009818,1.0126529896760956,1.0112646739130435,1.009748032327213,1.0080961007591442,1.0063020251546657,1.0043590593974667,1.0022605631926684,1]
    factorsListB = [0,0.13755095108695653,0.14040421195652175,0.14335371376811593,0.14639945652173914,0.14953804347826088,0.15276834239130435,0.15609229425465837,0.1595108695652174,0.163022720410628,0.16662703804347828,0.17032485177865614,0.17411684782608697,0.17800219481605353,0.1819802989130435,0.18605185688405798,0.19021739130434784,0.19447630274936062,0.19882812500000002,0.2032733838672769,0.2078125,0.21244500517598344,0.21717051630434783,0.22198945534026465,0.2269021739130435,0.23190828804347827,0.23700747282608695,0.24220008051529793,0.24748641304347826,0.25286614505247373,0.25833899456521736,0.26390526384992985,0.26956521739130435,0.2752799736495389,0.2810082320971867,0.2867478649068323,0.2924969806763285,0.29825297444183313,0.30401351544622424,0.30977738294314383,0.3155434782608696,0.32130998144220574,0.3270752458592132,0.3328385679979778,0.33859930830039525,0.34435612922705316,0.35010780954631376,0.35585395467160036,0.36159420289855077,0.367327528837622,0.3730529891304348,0.3787703804347826,0.38447951505016725,0.3901795785479902,0.39586981682769723,0.4015501482213439,0.4072204968944099,0.41288019641495044,0.41852862631184407,0.4241657838983051,0.4297916666666667,0.43540571543121886,0.44100740708274894,0.44659679089026916,0.45217391304347826,0.45771817516722413,0.46321434453227933,0.46866913732965604,0.4740888746803069,0.4794795112633901,0.48484666149068323,0.4901956234690753,0.49553140096618353,0.5008587235705777,0.5061820652173913,0.511505661231884,0.51683352402746,0.522169457580463,0.5275170707915273,0.5328797898321409,0.5382608695652175,0.5436634041196994,0.5490903366914104,0.5545444686354112,0.5600284679089027,0.5655448769181586,0.571096119817998,0.5766845093078461,0.5823122529644269,0.587981459147533,0.5936941425120773,0.5994522291567128,0.605257561436673,0.6111119024661056,0.617016940333025,0.6229742920480549,0.6289855072463768,0.6351229829672793,0.6414426436335403,0.6479223278985508,0.6545407608695651,0.6612773420684459,0.6681122788789429,0.6750268771105953,0.682002508361204,0.6890220626293996,0.6960685949036095,0.7031256349045103,0.7101777941324477,0.7172099371759074,0.7242074790019764,0.7311565131707795,0.7380436299010092,0.7448557437956906,0.7515802285945843,0.7582051925803404,0.7647185684501498,0.7711094272575252,0.7773667787398674,0.7834798593350383,0.7894386888586956,0.7952333363277039,0.8008541963649324,0.8062921140420644,0.8115382297510518,0.8165838315217392,0.8214204839544513,0.8260401510612804,0.8346813648045164,0.8388597408026756,0.8429692685861268,0.8470090682641633,0.8509781587119974,0.8548755880921479,0.8587005585748793,0.8624522333559783,0.8661298620477627,0.8697325314075299,0.873259598842665,0.876710197496118,0.8800836657801419,0.883379360743264,0.8865964792680145,0.8897344174592392,0.8927925880809596,0.8957702454958308,0.8986668376589766,0.9014818274456521,0.9042145211737672,0.9068644134963768,0.9094310124532106,0.9119136714280606,0.9143119272165389,0.9166253286455393,0.9188532718267883,0.9209953316610926,0.9230510938798118,0.9250199934645019,0.9269016932424118,0.928695652173913,0.9304079357109102,0.9320463466183575,0.9336131822652708,0.9351106839872747,0.936541038784585,0.9379063809586171,0.9392087936897944,0.9404503105590062,0.9416329170150503,0.9427585517902813,0.9438291082665903,0.9448464357937311,0.9458123409619251,0.9467285888305847,0.9475969041149069,0.9484189723320159,0.9491964409082535,0.949930920249145,0.9506239847735002,0.9512771739130435,0.9518919930789094,0.9524699145962734,0.9530123786083392,0.9535207939508507,0.9539965389982374,0.9544409624824685,0.9548553842856312,0.9552410962072155,0.9555993627070393,0.9559314216247139,0.9562384848765081,0.9565217391304347,0.9567691026976797,0.9569694433549978,0.9571251175794314,0.9572385204081633,0.957311976695266,0.9573477643280632,0.957348115407199,0.9573152173913044,0.9572512142074951,0.957158207328885,0.9570382568202506,0.9568933823529412,0.9567255641900848,0.9565367441430983,0.9563288265004727,0.9561036789297659,0.955863133353703,0.9556089868012423,0.9553430022344426,0.9550669093519277,0.9547824053697183,0.9544911557801706,0.9541947950897371,0.953894927536232,0.9535931277862653,0.9532909416134823,0.9529898865582193,0.95269145256917,0.9523971026276313,0.9521082733548767,0.9518263756031877,0.9515527950310558,0.9513346165458937,0.9512102010388611,0.951167984461789,0.9511966056445462,0.9512849018653883,0.951421904536862,0.9515968350037644,0.9517991004497751,0.952018289909498,0.9522441703827574,0.9524666830481037,0.9526759395725866,0.9528622185149515,0.9530159618195104,0.9531277713980354,0.9531884057971015,0.9531887769484034,0.9531199469996408,0.9529731252236536,0.9527396650035638,0.952411060891748,0.9519789457405443,0.951435087902658,0.9507713884992988,0.949979878754147,0.9490527173913044,0.9479821880954443,0.9467606970324363,0.9453807704287678,0.9438350522081479,0.942116301683717,0.9402173913043478]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def sierraFilterFunction( targetImage, inputPathPy, outputPathPy ):
    factorsListR = [0,0.9768512228260869,1.0343410326086957,1.0898324275362319,1.143342391304348,1.1948607336956523,1.2443953804347825,1.2919400232919254,1.3375,1.381070727657005,1.42265625,1.4622529644268774,1.4998641304347826,1.535486778846154,1.569123641304348,1.6007721920289855,1.6304347826086956,1.6581092151534527,1.683797554347826,1.7074978546910755,1.729211956521739,1.748938114648033,1.766677989130435,1.782429997637051,1.796195652173913,1.8079735054347827,1.817764945652174,1.8255686392914654,1.8313858695652174,1.8352154001124439,1.8370584239130434,1.836913788569425,1.8347826086956522,1.831721426218709,1.828772378516624,1.8259142080745343,1.8231280193236716,1.8203969594594593,1.8177059496567507,1.815041457636566,1.8123913043478261,1.809744913176034,1.8070915016821947,1.8044224753538927,1.8017296350049408,1.7990055102657003,1.7962432803638944,1.7934367050185014,1.7905800639719203,1.7876681039263531,1.7846959918478262,1.7816592737638535,1.7785538383152175,1.7753762048810502,1.7721222071256038,1.7687889081027668,1.7653732773680126,1.761872497139588,1.7582839439655173,1.7546051722549743,1.7508338994565216,1.7469679926942268,1.7430054566970548,1.7389444228778468,1.7347831394361413,1.7305766617892977,1.7263782526350462,1.7221831146576898,1.7179872322570333,1.7137863303402647,1.7095768633540374,1.7053550070805266,1.7011175035854469,1.6968612734514592,1.6925830594521152,1.688280230978261,1.6839498489344966,1.679589457756917,1.6751967278079711,1.670769124931205,1.6663045601222826,1.6618010475375737,1.6572563875265112,1.652668793380042,1.648036563470497,1.6433577765345269,1.6386308968971184,1.6338544594890054,1.629026776340168,1.624146521586468,1.6192124282910627,1.614223005255614,1.6091771030245747,1.6040736215813465,1.5989112367021276,1.593689037471396,1.5884057971014494,1.5830711074069923,1.577696594942325,1.572284495772947,1.5668369565217393,1.5613560387968144,1.5558437233589089,1.5503019140460108,1.5447324414715717,1.539137066511387,1.5335174835931091,1.5278753238013003,1.522212157809984,1.5165294986537694,1.510828804347826,1.5051114803662358,1.4993788819875777,1.4936323165159675,1.487873045385202,1.4821022861531192,1.4763212143928037,1.4705309654868077,1.46473263633014,1.4589272869473877,1.4531159420289856,1.4472995923913043,1.4414791963649323,1.435655681115235,1.429829943899018,1.4240028532608697,1.4181752501725329,1.4123479491184525,1.4006461045458376,1.3946775710702342,1.3886272117698308,1.3825057641633727,1.3763236428367114,1.3700909514925372,1.3638174944645733,1.3575127877237851,1.3511860694025706,1.3448463098613737,1.3385022213207696,1.3321622670807454,1.325834670347672,1.3195274226883038,1.3132482921290667,1.3070048309178743,1.3008043829647677,1.294654090976772,1.288560903301538,1.282531580493537,1.2765727016158448,1.270690670289855,1.2648917205046069,1.2591819221967964,1.2535671866119635,1.2480532714568042,1.2426457858520337,1.2373501950947603,1.2321718252388534,1.227115867501376,1.2221873825027345,1.2173913043478262,1.2126932290963408,1.2080546749194847,1.2034743900456788,1.1989511532343586,1.1944837728507904,1.190071085974332,1.185711957538727,1.1814052795031056,1.1771499700524184,1.172944972826087,1.1687892561737223,1.1646818124368048,1.1606216572552777,1.156607828898051,1.1526393876164596,1.1487154150197627,1.1448350134718128,1.1409973055080607,1.1372014332721034,1.1334465579710147,1.1297318593487269,1.1260565351767797,1.1224198007617605,1.1188208884688091,1.115259047260576,1.111733542251052,1.1082436542737155,1.1047886794634598,1.1013679288517944,1.0979807279748284,1.0946264164935693,1.0913043478260869,1.0880002930347488,1.0847022425481847,1.0814128475125417,1.078134704968944,1.074870359226716,1.0716223031949934,1.068392979674186,1.0651847826086958,1.0620000583022389,1.0588411065970726,1.0557101820183659,1.0526094948849105,1.0495412123873278,1.046507459634867,1.0435103206718652,1.040551839464883,1.037634020861504,1.034758831521739,1.0319282008229447,1.0291440217391306,1.026408151695499,1.0237224133990248,1.0210885956458544,1.0185084541062803,1.0159837120880084,1.0135160612784204,1.0111071624664978,1.0087586462450593,1.0064721136939307,1.0042491370446534,1.0020912603273056,1,0.9980175875603865,0.9961770151981532,0.9944660834849646,0.9928728070175439,0.9913854097446364,0.9899923204158789,0.9886821681488801,0.9874437781109445,0.9862661673119986,0.9851385405053884,0.9840502861933396,0.9829909727339721,0.9819503445468721,0.9809183184143222,0.9798849798753866,0.9788405797101449,0.9777755305114559,0.9766804033417176,0.9755459244721775,0.9743629722024234,0.9731225737577639,0.9718159022622835,0.9704342737854251,0.9689691444600281,0.9674121076698098,0.9657548913043479,0.9639893550796812,0.9621074879227054,0.9601014054175976,0.9579633473125643,0.9556856750852515,0.9532608695652174]
    factorsListG = [0,1.1979789402173913,1.2796705163043478,1.358129528985507,1.4333559782608696,1.5053464673913044,1.574099864130435,1.6396181094720497,1.7019021739130435,1.7609507095410628,1.8167629076086957,1.86933979743083,1.9186820652173913,1.9647888795986623,2.0076596467391306,2.047295063405797,2.083695652173913,2.1168608136189255,2.146790081521739,2.173483981693364,2.1969429347826086,2.2171664725672877,2.234154211956522,2.247906574905482,2.2584239130434782,2.2657058423913043,2.2697520380434786,2.2705628522544283,2.2681385869565216,2.262478916791604,2.253583559782609,2.241452818197756,2.226086956521739,2.208688446969697,2.190561061381074,2.1718429736024842,2.152657004830918,2.1331126982961224,2.1133080663615558,2.0933310688405795,2.0732608695652175,2.0531684948303286,2.033119419642857,2.013171843402427,1.993379060647233,1.9737896286231884,1.9544478822069944,1.9353943830943572,1.9166663128396741,1.8982978177684118,1.8803203124999999,1.862762414748508,1.84565152069398,1.8290119975389663,1.812866722020934,1.7972369071146246,1.7821422505822981,1.7676010678871092,1.7536304113568215,1.740246177229182,1.7274632019927538,1.7152953492516039,1.7037555881837307,1.6928560645272603,1.6826081649116849,1.6728085806856186,1.6632380187747036,1.6538844500324466,1.644736552909207,1.635783416036547,1.6270148728649068,1.6184213296080834,1.6099936075256642,1.6017233798019654,1.5936024254553467,1.5856230751811595,1.5777780633223684,1.5700603913749294,1.5624637463419733,1.554981812396808,1.547608695652174,1.5403387932769728,1.5331667757489396,1.5260875703902566,1.5190962449857661,1.5121883991368286,1.50535954088726,1.4986054824150425,1.4919222262537055,1.485305859184172,1.478752924969807,1.4722598393454374,1.4658231738835068,1.4594399215462834,1.4531069322386678,1.4468211885011442,1.4405800639719202,1.4343920712404752,1.4282657220496895,1.4221985479797978,1.416187839673913,1.4102313313872148,1.4043265132139813,1.3984712200559308,1.3926633700877926,1.3869007181677018,1.381181424323216,1.3755033999136528,1.3698648695400564,1.364264122955724,1.3586992805088933,1.3531687597924011,1.3476709590935558,1.3422044085465563,1.3367674663901603,1.331358769494329,1.3259770017335082,1.3206206742382014,1.3152885645035004,1.309979491117099,1.3046920997509057,1.2994252913896873,1.2941780030514969,1.2889489992046659,1.2837372896213184,1.2785419157608697,1.273361747325742,1.2681959570780554,1.2578781966211663,1.252678720735786,1.2474512788333887,1.242201910408432,1.2369364733164432,1.23166065055159,1.2263799567230274,1.2210997442455243,1.2158252092589654,1.2105613972904852,1.2053132086721927,1.2000854037267081,1.1948826077320382,1.1897093156766687,1.1845698968151415,1.1794685990338165,1.174409553035982,1.169396776354973,1.16443417720349,1.1595255581668626,1.1546746197475926,1.1498849637681159,1.145160096638353,1.1405034324942793,1.135918296213413,1.1314079263128176,1.1269754777349228,1.1226240245261985,1.1183565624134588,1.1141760112823336,1.1100852175622093,1.106086956521739,1.102148912199568,1.0982380988325282,1.0943559949319819,1.0905040429480382,1.0866837532938076,1.0828965999869042,1.079143920040354,1.0754270186335404,1.0717472705492668,1.0681060182225064,1.0645044733663869,1.0609438195146614,1.057425311007791,1.0539501733508245,1.0505195069875777,1.0471343873517787,1.0437959615266519,1.0405053508182707,1.0372635328743625,1.0340715579710145,1.0309304297156499,1.0278411296583851,1.02480461789469,1.0218218336483933,1.0188936958357815,1.0160211036115006,1.0132049368969425,1.0104460568917668,1.0077453065691857,1.0051035111556064,1.0025214785952083,1,0.9975345041816851,0.995118850851636,0.9927514893394649,0.9904309006211179,0.9881555965156699,0.9859241189064558,0.9837350389856893,0.9815869565217392,0.9794784991482803,0.9774083216745588,0.975375105416042,0.9733775575447571,0.9714144104586426,0.9694844211692697,0.9675863707073094,0.9657190635451506,0.9638813270360932,0.9620720108695653,0.9602899865418298,0.9585341468416735,0.9568034053505817,0.955096695956928,0.9534129723837209,0.9517512077294685,0.9501103940217392,0.9484895417830076,0.9468876796083979,0.9453038537549407,0.9437371277419832,0.9421865819623972,0.9406513133042504,0.9391304347826087,0.9376724411231884,0.9363195580030782,0.9350616425852327,0.9338887299771168,0.9327910293454529,0.9317589201323252,0.9307829483695652,0.9298538230884559,0.9289624128218884,0.9280997421962096,0.9272569886100833,0.9264254789977893,0.9255966866744634,0.9247622282608696,0.9239138606853738,0.9230434782608695,0.9221431098344759,0.9212049160079051,0.9202211864264627,0.9191843371347114,0.9180869079968944,0.9169215601802757,0.9156810736996127,0.914358345021038,0.9129463847236774,0.9114383152173913,0.9098273685150701,0.908106884057971,0.9062703065926276,0.9043111840979117,0.9022231657608696,0.9]
    factorsListB = [30.330434782608695,31.038943614130435,15.915574048913044,10.900894474637681,8.412296195652175,6.933260869565217,5.958282382246377,5.270712829968944,4.762228260869565,4.372650588768116,4.065872961956521,3.8189167490118576,3.6164628623188406,3.4479070861204018,3.3056749805900623,3.1842108242753624,3.0793478260869565,2.987900615409207,2.907391681763285,2.83586420194508,2.7717527173913044,2.713790760869565,2.6609421319169964,2.612350100425331,2.5673007246376813,2.525194972826087,2.4855259719899667,2.4478613123993562,2.411830357142857,2.377114177286357,2.343436367753623,2.3105556407784014,2.2782608695652176,2.2470854948945984,2.2175851182864452,2.189618594720497,2.1630585748792273,2.137793313014101,2.1137210383295195,2.0907521599777037,2.068804347826087,2.047804960896076,2.0276866589026916,2.0083899456521737,1.9898591897233202,1.9720452143719807,1.9549016422495273,1.9383874884366328,1.922463768115942,1.9070960653283053,1.892251358695652,1.877900548806479,1.8640154682274248,1.8505713571575062,1.8375440318035428,1.8249123023715415,1.8126552795031057,1.8007547315980168,1.7891925131184407,1.7779528601694916,1.767019927536232,1.7563800227191733,1.7460192408835904,1.7359256383712904,1.7260869565217392,1.716494303929766,1.707137784090909,1.6980054297128488,1.6890864769820972,1.680370293793321,1.6718472195263974,1.6635081378214942,1.65534408495622,1.6473469373511018,1.6395090105390717,1.6318226902173913,1.624281098040618,1.616877712979955,1.609606021808807,1.6024601635594387,1.5954345703125,1.5885236345947398,1.581722333145546,1.5750258847891567,1.5684294327445651,1.5619286484974426,1.5555194048597067,1.5491974715767116,1.5429591966711955,1.536800710643625,1.5307185990338164,1.5247095974677496,1.5187703065926277,1.5128978385051426,1.5070890668362629,1.5013413544050345,1.495651820086051,1.490057622002465,1.4845902423469388,1.4792391475900306,1.4739942255434784,1.4688457645017219,1.4637844336104007,1.4588012643784296,1.453887714909072,1.4490353260869564,1.4442361983439296,1.4394826480597318,1.434767276192633,1.4300829552253689,1.4254228168231227,1.4207803166617705,1.4161489166828416,1.4115225357108503,1.4068952314549963,1.4022612683128544,1.3976151084613944,1.3929514759847639,1.3882650579172808,1.3835509339605407,1.3788042770606883,1.3740204197358965,1.369194847536529,1.3643232618637329,1.3594012973352034,1.3544249320652175,1.3493902044513457,1.344293277666039,1.3338947168857431,1.3285866952341139,1.3232141838491538,1.317784502635046,1.3123050067423994,1.3067825782770928,1.3012241470410628,1.2956361892583121,1.2900252400031738,1.2843973987870196,1.2787588339654365,1.2731152950310558,1.2674726092738207,1.261836200627679,1.2562115788423533,1.2506038647342994,1.2450182721139431,1.2394596392942228,1.2339329040039928,1.228442641010576,1.2229935302378174,1.2175899003623187,1.2122361903433632,1.206936498855835,1.201695039428815,1.1965156955815923,1.1914024697580645,1.1863590440356744,1.1813891959896843,1.1764965000687948,1.1716844675023927,1.1669565217391304,1.1622841171853902,1.1576367921363393,1.1530150227560683,1.14841927359491,1.14384999794137,1.139307638161341,1.1347926260251238,1.1303053830227743,1.1258463206682532,1.121415840792839,1.1170143358282483,1.1126421890798786,1.1082997749905754,1.1039874593953023,1.0997055997670808,1.0954545454545455,1.0912346379114468,1.0870462109184171,1.0828895907973037,1.0787650966183575,1.0746730404005524,1.0706137273053034,1.06658745582383,1.0625945179584122,1.0586351993977674,1.0547097796867695,1.050818532390723,1.0469617252543941,1.0431396203559926,1.039352474256293,1.0356005381430684,1.0318840579710145,1.0281920987975894,1.024514301322277,1.0208517541109254,1.0172055235137534,1.0135766542291988,1.0099661698506808,1.0063750733968757,1.0028043478260869,0.9992549565352585,0.995727843844167,0.9922239354653031,0.9887441389599319,0.985289344180806,0.9818604237019839,0.9784582332361899,0.9750836120401338,0.9717373833081964,0.9684203545548654,0.9651333179862971,0.9618770508613619,0.9586523158425189,0.955459861336855,0.9523004218276037,0.9491747181964573,0.9460834580369666,0.9430273359593139,0.9400070338867381,0.9370232213438735,0.9340765557372614,0.9311676826282805,0.9282972359987327,0.9254658385093169,0.9226895191727053,0.9199804912947287,0.9173337131595959,0.9147442315026697,0.9122071795792197,0.9097177752835538,0.9072713193170054,0.9048631934032983,0.9024888585498694,0.9001438533537719,0.8978237923508327,0.8955243644067796,0.8932413311491011,0.8909705254384362,0.8887078498783427,0.8864492753623189,0.8841908396569998,0.8819286460204815,0.8796588618547594,0.8773777173913043,0.8750815044088287,0.872766574982326,0.8704293402624979,0.8680662692847124,0.8656738878066614,0.863248777173913,0.8607875732125844,0.8582869651483782,0.8557436945512544,0.8531545543050325,0.8505163876012362,0.8478260869565217]
    def newBandR(intensity):
        iO = int( intensity * factorsListR[intensity])
        return iO
    def newBandG(intensity):
        iO = int( intensity * factorsListG[intensity])
        return iO
    def newBandB(intensity):
        iO = int( intensity * factorsListB[intensity])
        return iO
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    R = img.getchannel('R')
    G = img.getchannel('G')
    B = img.getchannel('B')
    # apply new channel curves
    R2 = R.point(newBandR)
    G2 = G.point(newBandG)
    B2 = B.point(newBandB)
    temp_img = Image.merge('RGBA',(R2,G2,B2,A))
    output_img = temp_img
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()


def fishEyeFunction ( targetImage, inputPathPy, outputPathPy, back_color ) :
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGBA")
    img2 = img.copy()
    pixdata1 = img.load()
    pixdata2 = img2.load()
    w,h = img.size
    w2 = w / 2
    h2 = h / 2
    for y in range(h):
        # Normalize every pixels along y axis
        # when y = 0 --> ny = -1
        # when y = h --> ny = +1
        ny = ((2 * y) / h) - 1
        # ny * ny pre calculated
        ny2 = ny ** 2
        for x in range(w):
            # Normalize every pixels along x axis
            # when x = 0 --> nx = -1
            # when x = w --> nx = +1
            nx = ((2 * x) / w) - 1
            # pre calculated nx * nx
            nx2 = nx ** 2
            # calculate distance from center (0, 0)
            r = math.sqrt(nx2 + ny2)
            # discard pixel if r below 0.0 or above 1.0
            if 0.0 <= r <= 1.0:
                nr = (r + 1 - math.sqrt(1 - r ** 2)) / 2
                if nr <= 1.0:
                    theta = math.atan2(ny, nx)
                    nxn = nr * math.cos(theta)
                    nyn = nr * math.sin(theta)
                    x2 = int(nxn * w2 + w2)
                    y2 = int(nyn * h2 + h2)

                    if 0 <= int(y2 * w + x2) < w * h:
                        r, g, b, a = pixdata1[x2, y2]
                        pixdata2[x, y] = (r, g, b, a)
            else:
                #pixdata2[x, y] = (0, 0, 0, 0)
                pixdata2[x, y] = ImageColor.getrgb( argb2rgba(back_color) )
    output_img = img2
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    img2.close()
    output_img.close()

















def apply3dLUTcubeMiddleStepFunction( cubeFilePath, lut3dType ):
    pyotherside.send('startApply3dLUTcubeFileFromPy', cubeFilePath, lut3dType )
def apply3dLUTcubeFile ( targetImage, inputPathPy, cubeFilePath, lut3dType, outputPathPy ):
    def load_cube_file(lines, target_mode=None, cls=ImageFilter.Color3DLUT):
        """
        Loads 3D lookup table from .cube file format.
        :param lines: Filename or iterable list of strings with file content.
        :param target_mode: Image mode which should be after color transformation.
                            The default is None, which means mode doesn't change.
        :param cls: A class which handles the parsed file.
                    Default is ``ImageFilter.Color3DLUT``.
        """
        name, size = None, None
        channels = 3
        file = lines = open(lines, 'rt')
        try:
            iterator = iter(lines)
            for i, line in enumerate(iterator, 1):
                line = line.strip()
                if line.startswith('TITLE "'):
                    name = line.split('"')[1]
                    continue
                if line.startswith('LUT_3D_SIZE '):
                    size = [int(x) for x in line.split()[1:]]
                    if len(size) == 1:
                        size = size[0]
                    continue
                if line.startswith('CHANNELS '):
                    channels = int(line.split()[1])
                if line.startswith('LUT_1D_SIZE '):
                    raise ValueError("1D LUT cube files aren't supported")

                try:
                    float(line.partition(' ')[0])
                except ValueError:
                    pass
                else:
                    # Data starts
                    break
            if size is None:
                raise ValueError('No size found in the file')
            table = []
            for i, line in enumerate(chain([line], iterator), i):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    pixel = [float(x) for x in line.split()]
                except ValueError:
                    raise ValueError("Not a number on line {}".format(i))
                if len(pixel) != channels:
                    raise ValueError(
                        "Wrong number of colors on line {}".format(i))
                table.extend(pixel)
        finally:
            if file is not None:
                file.close()
        instance = cls(size, table, channels=channels,
                       target_mode=target_mode, _copy_table=False)
        if name is not None:
            instance.name = name
        return instance

    def load_hald_image(image, target_mode=None, cls=ImageFilter.Color3DLUT):
        if not isinstance(image, Image.Image):
            image = Image.open(image)
        if image.size[0] != image.size[1]:
            raise ValueError("Hald image should be a square")
        channels = len(image.getbands())
        for i in range(2, 9):
            if image.size[0] == i**3:
                size = i**2
                break
        else:
            raise ValueError("Can't detect hald size")
        table = []
        for color in zip(*[
            ImageMath.eval("a/255.0", a=im.convert('F')).im
            for im in image.split()
        ]):
            table.extend(color)
        return cls(size, table, target_mode=target_mode, _copy_table=False)

    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    A = img.getchannel('A')
    rgb_img = img.convert('RGB')
    temp_img = rgb_img
    if "cubeFile" in lut3dType:
        lut = load_cube_file( cubeFilePath )
        temp_img = rgb_img.filter(lut)
    elif "imageFile" in lut3dType:
        allowApplication = "yes"
        haldImage = Image.open( cubeFilePath )
        if haldImage.size[0] != haldImage.size[1]:
            allowApplication = "no"
        for i in range(2, 9):
            if haldImage.size[0] == i**3:
                size = i**2
                break
        else:
            allowApplication = "no"
        if "yes" in allowApplication:
            lut = load_hald_image( cubeFilePath )
            temp_img = rgb_img.filter(lut)
    R = temp_img.getchannel('R')
    G = temp_img.getchannel('G')
    B = temp_img.getchannel('B')
    output_img = Image.merge('RGBA',(R,G,B,A))
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    img.close()
    temp_img.close()
    output_img.close()









def paintBlurRegionFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, blurRadius ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    cropped_img = img.crop(area)
    blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(blurRadius))
    img.paste(blurred_img,(area))
    output_img = img
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img.close()
    output_img.close()
    cropped_img.close()
    blurred_img.close()


def paintRectangleRegionFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, paintColor, solidTypeTool ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    TINT_COLOR = (ImageColor.getrgb(argb2rgb(paintColor)) )
    OPACITY = argb2alpha(paintColor)
    overlay = Image.new( 'RGBA', (img.size), TINT_COLOR+(0,) )
    draw = ImageDraw.Draw(overlay)
    if "circle" in solidTypeTool:
        draw.ellipse( (area), fill=TINT_COLOR+(OPACITY,) )
    else:
        draw.rectangle( (area), fill=TINT_COLOR+(OPACITY,) )
    output_img = Image.alpha_composite(img, overlay)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img.close()
    output_img.close()


def paintFrameRegionFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, paintColor, frameThickness, frameTypeTool ):
    def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):
        mask = Image.new(
            size=[int(dim * antialias) for dim in image.size],
            mode='L', color='black')
        draw = ImageDraw.Draw(mask)
        for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
            left, top = [(value + offset) * antialias for value in bounds[:2]]
            right, bottom = [(value - offset) * antialias for value in bounds[2:]]
            draw.ellipse([left, top, right, bottom], fill=fill)
        mask = mask.resize(image.size, Image.LANCZOS)
        image.paste(outline, mask=mask)
        mask.close()

    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = math.ceil(rectWidth * scaleFactor) - 1 # why?
    rectHeight_real = math.ceil(rectHeight * scaleFactor) - 1 # why?
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    TINT_COLOR = (ImageColor.getrgb(argb2rgb(paintColor)) )
    OPACITY = argb2alpha(paintColor)
    overlay = Image.new( 'RGBA', (img.size), TINT_COLOR+(0,) )
    draw = ImageDraw.Draw(overlay)
    if "circle" in frameTypeTool:
        #draw.ellipse( (area), fill = None, outline = TINT_COLOR+(OPACITY,), width = int(frameThickness) ) # pixels between the lines!!!
        area2 = (rectX_real + int(frameThickness)/2, rectY_real + int(frameThickness)/2, rectX_real+rectWidth_real - int(frameThickness)/2, rectY_real+rectHeight_real - int(frameThickness)/2)
        draw_ellipse(overlay, area2, width=int(frameThickness), outline = TINT_COLOR+(OPACITY,), )
    else:
        draw.rectangle( (area), fill = None, outline = TINT_COLOR+(OPACITY,), width = int(frameThickness) )
    output_img = Image.alpha_composite(img, overlay)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img.close()
    output_img.close()


def paintLineRegionFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, paintColor, lineThickness ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectWidth_real, rectHeight_real)
    TINT_COLOR = (ImageColor.getrgb(argb2rgb(paintColor)) )
    OPACITY = argb2alpha(paintColor)
    overlay = Image.new( 'RGBA', (img.size), TINT_COLOR+(0,) )
    draw = ImageDraw.Draw(overlay)
    draw.line( (area), fill = TINT_COLOR+(OPACITY,), width = int(lineThickness))
    output_img = Image.alpha_composite(img, overlay)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img.close()
    output_img.close()


def paintTextRegionFunction ( inputPathPy, outputPathPy, rectX_center, rectY_center, scaleFactor, paintColor, paintBackColor, paintText, paintTextSize, paintTextFontNr, fontPath, paintTextFontStyleNr, paintTextAngle, customFontFilePath ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    rectX_real = int(rectX_center * scaleFactor)
    rectY_real = int(rectY_center * scaleFactor)
    if int(paintTextAngle) < -90 :
        paintTextAngle = -90
    if 90 < int(paintTextAngle) :
        paintTextAngle = 90

    if int(paintTextFontNr) == 0 :
        ftn = ImageFont.truetype("/usr/share/fonts/sail-sans-pro/SailSansPro-Light.ttf", int(paintTextSize), encoding="unic")
    if int(paintTextFontNr) == 1 :
        if not customFontFilePath:
            customFontFilePath = "/usr/share/fonts/sail-sans-pro/SailSansPro-Light.ttf"
        if "Sailfish" in customFontFilePath:
            customFontFilePath = "/usr/share/fonts/sail-sans-pro/SailSansPro-Light.ttf"
        ftn = ImageFont.truetype( customFontFilePath, int(paintTextSize), encoding="unic" )
    if int(paintTextFontNr) == 2:
        if int(paintTextFontStyleNr) == 0:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", int(paintTextSize), encoding="unic")
        if int(paintTextFontStyleNr) == 1:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Bold.ttf", int(paintTextSize), encoding="unic")
        if int(paintTextFontStyleNr) == 2:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Italic.ttf", int(paintTextSize), encoding="unic")
    if int(paintTextFontNr) == 3:
        if int(paintTextFontStyleNr) == 0:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSerif-Regular.ttf", int(paintTextSize), encoding="unic")
        if int(paintTextFontStyleNr) == 1:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSerif-Bold.ttf", int(paintTextSize), encoding="unic")
        if int(paintTextFontStyleNr) == 2:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSerif-Italic.ttf", int(paintTextSize), encoding="unic")
    if int(paintTextFontNr) == 4:
        if int(paintTextFontStyleNr) == 0:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationMono-Regular.ttf", int(paintTextSize), encoding="unic")
        if int(paintTextFontStyleNr) == 1:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationMono-Bold.ttf", int(paintTextSize), encoding="unic")
        if int(paintTextFontStyleNr) == 2:
            ftn = ImageFont.truetype("/usr/share/fonts/liberation/LiberationMono-Italic.ttf", int(paintTextSize), encoding="unic")
    if int(paintTextFontNr) == 5:
        ftn = ImageFont.truetype( fontPath, int(paintTextSize), encoding="unic" )

    # english alphabet: 2 letters (h,p) form max distance from top to bottom -> baseline without descenders: "h"
    fageWidth, fakeHeight = ftn.getsize("hp")
    textWidth, textHeight = ftn.getsize(paintText)
    img_txt = Image.new('RGBA', (int(textWidth), int(fakeHeight*1.05)), argb2rgba(paintBackColor) )
    img_txt_oldWidth, img_txt_oldHeight = img_txt.size
    draw_text = ImageDraw.Draw(img_txt)
    draw_text.text( (0,0), paintText, font = ftn, fill = argb2rgba(paintColor) )
    img_txt_rotated = img_txt.rotate( int(paintTextAngle), expand=1)
    img_txt_rotatedWidth, img_txt_rotatedHeight = img_txt_rotated.size

    # correction for QML/Pillow handling of center
    fontMaxWidth, fontMaxHeight = draw_text.textsize("hp", ftn)
    correctionY_0_Degrees = ( fontMaxHeight - img_txt_oldHeight )
    correctionY = int( correctionY_0_Degrees * math.sin(math.radians( (90-abs(int(paintTextAngle))) ) ) )
    correctionX = int( correctionY_0_Degrees * math.cos(math.radians( (90-abs(int(paintTextAngle))) ) ) )

    # put it all together
    #adjustedX = int(rectX_real - img_txt_rotatedWidth/2)
    #adjustedY = int(rectY_real - img_txt_rotatedHeight/2 - correctionY_0_Degrees/2)
    adjustedX = int(rectX_real - img_txt_rotatedWidth/2 - correctionX/2)
    adjustedY = int(rectY_real - img_txt_rotatedHeight/2 - correctionY/2)
    img.paste(img_txt_rotated, (adjustedX, adjustedY), img_txt_rotated)

    output_img = img
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img.close()
    img_txt.close()
    img_txt_rotated.close()
    output_img.close()


def paintCanvasFunction( inputPathPy, outputPathPy, freeDrawPolyCoordinates, scaleFactor, paintColor, paintCanvasThickness, drawType ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    TINT_COLOR = (ImageColor.getrgb(argb2rgb(paintColor)) )
    OPACITY = argb2alpha(paintColor)
    overlay = Image.new( 'RGBA', (img.size), TINT_COLOR+(0,) )
    draw = ImageDraw.Draw(overlay)
    strokesList = list( freeDrawPolyCoordinates.split("/") )
    for i in range (0, len(strokesList)-1) :
        coordinatesList = list( strokesList[i].split(";") )
        del coordinatesList[-1] # remove last comma
        coordinatesList = list(map(float, coordinatesList))
        coordinatesList = [i * float(scaleFactor) for i in coordinatesList]
        pairSublist = []
        fullPairsList = []
        for i in range(0, len(coordinatesList)-1, 2):
            pairSublist.append ( coordinatesList[i] )
            pairSublist.append ( coordinatesList[i+1] )
            fullPairsList.append ( tuple(pairSublist) )
            pairSublist.clear()
        coordinatesTuples = tuple(fullPairsList)
        if "polyline" in drawType:
            draw.line( (coordinatesTuples), fill = TINT_COLOR+(OPACITY,), width = int(paintCanvasThickness), joint = 'curve')
        else:
            if not 0 < len(coordinatesTuples) < 2:
                draw.polygon( (coordinatesTuples), fill = TINT_COLOR+(OPACITY,), )
    output_img = Image.alpha_composite(img, overlay)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    pyotherside.send('clearDrawCanvas', )
    img.close()
    output_img.close()


def paintPointRegionFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, paintColor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectWidth_real, rectHeight_real)

    TINT_COLOR = (ImageColor.getrgb(argb2rgb(paintColor)) )
    OPACITY = argb2alpha(paintColor)
    overlay = Image.new( 'RGBA', (img.size), TINT_COLOR+(0,) )
    draw = ImageDraw.Draw(overlay)
    draw.ellipse( (area), fill = TINT_COLOR+(OPACITY,), outline = None)

    output_img = Image.alpha_composite(img, overlay)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img.close()
    output_img.close()


def paintCopyFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGBA'):
        img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    output_img = img.crop(area)
    copyPasteImageWidth, copyPasteImageHeight = output_img.size
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('finishedCopyFromPainting', outputPathPy, copyPasteImageWidth, copyPasteImageHeight)
    img.close()
    output_img.close()


def paintPasteRegionFunction ( inputPathPy, copyPastePath, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor ):
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = math.ceil(rectWidth * scaleFactor) #all pixels to right edge
    rectHeight_real = math.ceil(rectHeight * scaleFactor) #all pixels to lower edge
    img1 = Image.open(inputPathPy)
    img1 = ImageOps.exif_transpose(img1)
    if img1.mode not in ('RGBA'):
        img1 = img1.convert('RGBA')
    img2 = Image.open(copyPastePath)
    img2 = ImageOps.exif_transpose(img2)
    if img2.mode not in ('RGBA'):
        img2 = img2.convert('RGBA')
    scaled_img2 = img2.resize((rectWidth_real, rectHeight_real))
    scaled_img2 = scaled_img2.convert('RGBA')
    img1.paste(scaled_img2, (rectX_real, rectY_real), scaled_img2)
    output_img = img1
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img1.close()
    img2.close()
    scaled_img2.close()
    output_img.close()


def paintSprayFunction ( inputPathPy, outputPathPy, rectX, rectY, rectWidth, rectHeight, scaleFactor, paintColor, radiusScatter, amountScatter, gaussSigmaWidth ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    rectWidth_real = int(rectWidth * scaleFactor)
    rectHeight_real = int(rectHeight * scaleFactor)
    area = (rectX_real, rectY_real, rectX_real+rectWidth_real, rectY_real+rectHeight_real)
    radiusScatter = float(radiusScatter * scaleFactor)
    amountScatter = int(amountScatter)
    gaussSigmaWidth = float(gaussSigmaWidth)
    TINT_COLOR = (ImageColor.getrgb(argb2rgb(paintColor)) )
    OPACITY = argb2alpha(paintColor)
    valueXList = []
    valueYList = []
    frequencies = {}
    for i in range (amountScatter):
        valueX = gauss( int(rectX_real+rectWidth_real/2), int(rectWidth_real/gaussSigmaWidth) )
        if (rectX_real) < valueX < (rectX_real+rectWidth_real):
            frequencies[int(valueX)] = frequencies.get(int(valueX), 0) + 1
            valueXList.append(valueX)
        valueY = gauss( int(rectY_real+rectHeight_real/2), int(rectHeight_real/gaussSigmaWidth) )
        if (rectY_real) < valueY < (rectY_real+rectHeight_real):
            frequencies[int(valueY)] = frequencies.get(int(valueY), 0) + 1
            valueYList.append(valueY)
    overlay = Image.new( 'RGBA', (img.size), TINT_COLOR+(0,) )
    draw = ImageDraw.Draw(overlay)
    # use the shorter list to get random coordinates
    if (len(valueYList) >= len(valueXList)):
        for i,item in enumerate(valueXList):
            draw.ellipse(( item-radiusScatter, valueYList[i]-radiusScatter, item+radiusScatter, valueYList[i] + radiusScatter), fill=TINT_COLOR+(OPACITY,), outline = None )
    else:
        for i,item in enumerate(valueYList):
            draw.ellipse(( valueXList[i]-radiusScatter, item-radiusScatter, valueXList[i]+radiusScatter, item + radiusScatter), fill=TINT_COLOR+(OPACITY,), outline = None )
    output_img = Image.alpha_composite(img, overlay)
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img.close()
    output_img.close()


def paintSymbolFunction ( inputPathPy, symbolSourcePath, outputPathPy, rectX, rectY, scaleFactor, paintColor, objectThickness ):
    img1 = Image.open(inputPathPy)
    img1 = ImageOps.exif_transpose(img1)
    if img1.mode not in ('RGBA'):
        img1 = img1.convert('RGBA')
    rectX_real = int(rectX * scaleFactor)
    rectY_real = int(rectY * scaleFactor)
    img2 = Image.open(symbolSourcePath)
    img2 = ImageOps.exif_transpose(img2)
    if img2.mode not in ('RGBA'):
        img2 = img2.convert('RGBA')
    img2 = img2.resize((round(img2.size[0]*float(objectThickness*scaleFactor)), round(img2.size[1]*float(objectThickness*scaleFactor))))
    img2_width, img2_height = img2.size

    def tint_image(src):
        src.load()
        r, g, b, alpha = src.split()
        gray = ImageOps.grayscale(src)
        result = ImageOps.colorize( gray, (0, 0, 0, 0), argb2rgb(paintColor) )
        result.putalpha(alpha)
        return result
    img2 = tint_image(img2)

    offset =( int(rectX_real-(img2_width/2) ), int(rectY_real-img2_height/2) )
    img1.paste(img2, offset, img2)

    output_img = img1
    output_img.save(outputPathPy, compress_level=1)
    pyotherside.send('exchangeImageFromPainting', outputPathPy)
    img1.close()
    img2.close()
    output_img.close()


def paintGetColorPointFunction ( inputPathPy, center1X, center1Y, scaleFactor ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    widthImg, heightImg = img.size
    center1X_real = int(center1X * scaleFactor)
    center1Y_real = int(center1Y * scaleFactor)
    # Patch if outmost corners are too wide of because of calculation with scale factor and int
    if (center1X_real > (widthImg-1)):
        center1X_real = (widthImg-1)
    if (center1Y_real > (heightImg-1)):
        center1Y_real = (heightImg-1)
    r, g, b, a = img.getpixel((center1X_real, center1Y_real))
    #hexaColorRGB = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    hexaColorARGB = '#{:02x}{:02x}{:02x}{:02x}'.format(a, r, g, b)
    pyotherside.send('getPixelValuesRGBA', r, g, b, a, hexaColorARGB)
    img.close()


def getDominantColorFunction ( inputPathPy ):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGBA')
    img = img.resize((1,1))
    r, g, b, a = img.getpixel((0,0))
    hexaColorARGB = '#{:02x}{:02x}{:02x}{:02x}'.format(a, r, g, b)
    pyotherside.send('getPixelValuesRGBA', r, g, b, a, hexaColorARGB)
    img.close()


def paintConvertRGBAFunction ( r, g, b, a ):
    hexaColorARGB = '#{:02x}{:02x}{:02x}{:02x}'.format(int(a),int(r), int(g), int(b))
    pyotherside.send('getPixelValuesRGBA', r, g, b, a, hexaColorARGB)











def getHomePath ():
    homeDir = str(Path.home())
    pyotherside.send('homePathFolder', homeDir )

def createNewFunction ( savePath, newImageSizeX, newImageSizeY, newBackColor ):
    output_img = Image.new("RGBA", (int(newImageSizeX), int(newImageSizeY)), color = newBackColor )
    output_img.save(savePath)
    pyotherside.send('fileIsSaved', savePath)
    pyotherside.send('exchangeImage', savePath)
    pyotherside.send('finishedSavingRenaming', savePath)
    output_img.close()


def deleteNowFunction ( inputPathPy ):
    os.remove ( inputPathPy )
    pyotherside.send('deleteImage', )


def deleteLastTMPFunction ( inputPathPy ):
    if ".tmp" in inputPathPy :
        os.remove ( inputPathPy )
        pyotherside.send('deleteLastTMP', inputPathPy )
    else :
        pyotherside.send('deleteLastTMP', "none" )


def deleteAllTMPFunction ( tempImageFolderPath ):
    for i in os.listdir( "/" + tempImageFolderPath ) :
        if (i.find(".tmp") != -1):
            os.remove ("/" + tempImageFolderPath+i)
            pyotherside.send('tempFilesDeleted', i )


def deleteCopyPasteFunction ( inputPathPy, tempImageFolderPath ):
    for i in os.listdir( "/" + tempImageFolderPath ) :
        if (i.find("copyPaste") != -1):
            os.remove ( inputPathPy )
            pyotherside.send('copyPasteImageDeleted', inputPathPy )


def saveNowFunction ( inputPathPy, savePath, tempImageFolderPath, pdfResolution, fileTargetType):
    img = Image.open(inputPathPy)
    img = ImageOps.exif_transpose(img)
    if ".jpg" in fileTargetType :
        img.convert('RGB').save("/" + savePath)
    elif ".pdf" in fileTargetType :
        wanted_dpi = int(pdfResolution)
        img = img.convert('RGB')
        img.save("/" + savePath, "PDF", resolution = wanted_dpi )
    else :
        img.save("/" + savePath)
    for i in os.listdir( "/" + tempImageFolderPath ) :
        if (i.find(".tmp") != -1):
            os.remove ("/" + tempImageFolderPath+i)
            pyotherside.send('tempFilesDeleted', i )
    new_imagePath = savePath
    pyotherside.send('fileIsSaved', )
    if ".pdf" not in fileTargetType :
        pyotherside.send('exchangeImage', new_imagePath)
        pyotherside.send('finishedSavingRenaming', new_imagePath)


def getImageSizeFunction ( inputPathPy ):
    estimatedSize = os.stat(inputPathPy).st_size
    pyotherside.send('estimatedFileSize', estimatedSize)


def renameOriginalFunction ( inputPathPy, new_imagePath) :
    os.rename("/" + inputPathPy, "/" + new_imagePath)
    pyotherside.send('exchangeImage', new_imagePath)
    pyotherside.send('finishedSavingRenaming', new_imagePath)


def getImageMetaDataFunction ( inputPathPy ) :
    img = Image.open( inputPathPy )
    imgFormat =  img.format
    imgMode = img.mode
    imgPalette = str(img.palette)
    imgWidth = img.width
    imgHeight = img.height
    if (".jpg" or ".jpeg" or ".tif" or ".tiff") in inputPathPy :
        ret = {}
        img_exif = img._getexif()
        if img_exif is None:
            imgExifFull = "This file contains no EXIF tags."
        else:
            for tag, value in img_exif.items():
                decoded = TAGS.get(tag, tag)
                if len(str(value)) > 64:
                    value = str(value)[:65] + "..."
                ret[decoded] = value
            imgExifFull = str(ret)
            imgExifFull = imgExifFull.replace("{", "")
            imgExifFull = imgExifFull.replace("}", "")
            imgExifFull = imgExifFull.replace(", '", "\n")
            imgExifFull = imgExifFull.replace("'", "")
    else:
        imgExifFull = "Filetype does not support EXIF tags."
    pyotherside.send('metaDataReceived', imgFormat, imgMode, imgPalette, imgWidth, imgHeight, imgExifFull )
    img.close()


def createCollageMiddleStepFunction ( currentCollageType, targetWidth, selectedPaths, shuffle, targetBackColor, targetColumns, targetSpacing, targetBlur, randomAngleList, ratioWanted, targetFrameSetup ):
    pyotherside.send('startCollageFunctionFromPy', currentCollageType, targetWidth, selectedPaths, shuffle, targetBackColor, targetColumns, targetSpacing, targetBlur, randomAngleList, ratioWanted, targetFrameSetup )


def createCollageMosaic ( outputPathPy, inputPathPy, targetWidth, selectedPaths, shuffle, targetBackColor, targetColumns, targetSpacing, targetBlur, targetImage, targetFrameSetup ):
    maxWidth = int( (targetWidth - ( (int(targetColumns)+1) * int(targetSpacing) )  )  / int(targetColumns) )
    allImagesList = list( selectedPaths.split(",") )
    targetFrameColor = (targetFrameSetup.split(","))[0]
    targetFrameWidth = int( (targetFrameSetup.split(","))[1] )
    if "yes" in shuffle:
        random.shuffle(allImagesList)
    thumbnailImageList = []
    maxHeight = int(maxWidth)
    for i in range ( 0, len(allImagesList) ) :
        img = Image.open( "/" + allImagesList[i] )
        img = img.convert('RGBA')
        img = ImageOps.exif_transpose(img)
        imageWidth, imageHeight = img.size
        imageRatio = imageWidth/imageHeight
        if (imageRatio > 1): #landscape
            new_Width = int( maxHeight * imageRatio )
            size = ( new_Width, maxHeight ) #keep height
            resized_img = img.resize(size)
            diffHorizontal = int( (new_Width - maxWidth)/2 ) #center horizontally
            area = ( diffHorizontal, 0, (diffHorizontal + maxWidth), maxHeight )
        else: #portrait
            new_Height = int( int(maxWidth / imageRatio) )
            size = ( maxWidth, new_Height ) #keep width
            resized_img = img.resize(size)
            diffVertical = int( (new_Height - maxHeight)/2 ) #center vertically
            area = ( 0, diffVertical, maxWidth, (diffVertical + maxHeight) )
        cropped_img = resized_img.crop(area)
        if "none" not in targetFrameColor:
            frameImg = Image.new('RGBA', ( cropped_img.size[0], cropped_img.size[1]), argb2rgba(targetFrameColor))
            innerImage = cropped_img.resize(( cropped_img.size[0] - 2*targetFrameWidth, cropped_img.size[1] - 2*targetFrameWidth ) )
            frameImg.paste( innerImage, (targetFrameWidth, targetFrameWidth), innerImage )
            cropped_img = frameImg
        thumbnailImageList.append (cropped_img)

    # generate main mosaic collage image
    cols = int(targetColumns)
    rows = math.ceil( len(allImagesList) / cols )
    out_height = int( rows * (maxHeight+int(targetSpacing)) + int(targetSpacing) )
    if "image" in targetBackColor:
        output_img = Image.open( "/" + inputPathPy )
        #output_img = ImageOps.exif_transpose(output_img)
        output_img = output_img.convert('RGBA')
        # Type A) crop to fit
        output_imgRatio = output_img.size[0] / output_img.size[1]
        collage_ratio = int(targetWidth) / out_height
        if (output_imgRatio < collage_ratio):
            #pyotherside.send('debugPythonLogs', "crop verticals" )
            targetSize = ( int(targetWidth), int(int(targetWidth)/output_imgRatio))
            output_img = output_img.resize(targetSize)
            diffVertical = (output_img.size[1] - out_height) / 2 #center vertically
            area = ( 0, diffVertical, output_img.size[0], (diffVertical + out_height) )
            output_img = output_img.crop(area)
        else:
            #pyotherside.send('debugPythonLogs', "crop horizontals" )
            targetSize = (int(out_height*output_imgRatio), out_height)
            output_img = output_img.resize(targetSize)
            diffHorizontal = (output_img.size[0] - targetWidth) / 2 #center horizontally
            area = ( diffHorizontal, 0, (diffHorizontal + targetWidth), out_height )
            output_img = output_img.crop(area)
        # Type B) scale to fit
        #targetsize = (int(targetWidth), out_height)
        #output_img = output_img.resize(targetsize)
        output_img = output_img.filter(ImageFilter.GaussianBlur(int(targetBlur)))
    else:
        output_img = Image.new('RGBA', (int(targetWidth), out_height), argb2rgba(targetBackColor))
    i = 0
    x = 0 + int(targetSpacing)
    y = 0 + int(targetSpacing)
    for row in range(rows):
        for col in range(cols):
            if ( i < len(thumbnailImageList) ):
                output_img.paste( thumbnailImageList[i], (x, y), thumbnailImageList[i] )
            i += 1
            x += int(maxWidth) + int(targetSpacing)
        x = 0 + int(targetSpacing)
        y += int(maxHeight) + int(targetSpacing)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy, allImagesList, 0)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    output_img.close()
    thumbnailImageList.clear()


def createCollageLines ( outputPathPy, inputPathPy, targetWidth, selectedPaths, shuffle, targetBackColor, targetColumns, targetSpacing, targetBlur, targetImage, targetFrameSetup ):
    def get_index_positions(list_of_elems, element):
        index_pos_list = []
        for i in range(len(list_of_elems)):
            if list_of_elems[i] == element:
                index_pos_list.append(i)
        return index_pos_list
    init_height = int( targetWidth / targetColumns )
    out_height = targetSpacing
    allImagesList = list( selectedPaths.split(",") )
    targetFrameColor = (targetFrameSetup.split(","))[0]
    targetFrameWidth = int( (targetFrameSetup.split(","))[1] )
    if "yes" in shuffle:
        random.shuffle(allImagesList)
    targetWidth = int(targetWidth)
    targetSpacing = int(targetSpacing)

    # create images list and list where to place
    thumbnailImageList = []
    putLineList = []
    posXonLine = targetSpacing
    currentLine = 0
    for i in range ( 0, len(allImagesList) ) :
        img = Image.open( "/" + allImagesList[i] ).convert('RGBA')
        img = ImageOps.exif_transpose(img)
        img.thumbnail((targetWidth-2*targetSpacing, init_height))
        if (posXonLine + img.size[0] + targetSpacing) <= targetWidth :
            posXonLine += img.size[0] + targetSpacing
            currentLine = currentLine
        else:
            posXonLine = targetSpacing
            currentLine += 1
        thumbnailImageList.append(img)
        putLineList.append(currentLine)

    # cycle trough list and adjust image sizes
    for i in range(max(putLineList)+1):
        index_pos_list = get_index_positions(putLineList, i)
        imgPerRow = len(index_pos_list)
        sumImgWidth = 0
        # cycle through each image in this line - get scaling factor
        for j in range(imgPerRow):
            sumImgWidth += thumbnailImageList[index_pos_list[j]].size[0]
        scalingFactor = ( sumImgWidth / (targetWidth - (imgPerRow+1) * targetSpacing) )
        # cycle again to rescale images of this line
        for j in range(imgPerRow):
            tmpImg = thumbnailImageList[index_pos_list[j]]
            cropped_img = ImageOps.scale(tmpImg, 1/scalingFactor)
            if "none" not in targetFrameColor:
                frameImg = Image.new('RGBA', ( cropped_img.size[0], cropped_img.size[1]), argb2rgba(targetFrameColor))
                innerImage = cropped_img.resize(( cropped_img.size[0] - 2*targetFrameWidth, cropped_img.size[1] - 2*targetFrameWidth ) )
                frameImg.paste( innerImage, (targetFrameWidth, targetFrameWidth), innerImage )
                cropped_img = frameImg
            thumbnailImageList[index_pos_list[j]] = cropped_img
        out_height += thumbnailImageList[index_pos_list[0]].size[1] + targetSpacing

    # create background image
    if "image" in targetBackColor:
        output_img = Image.open( "/" + inputPathPy ).convert('RGBA')
        #output_img = ImageOps.exif_transpose(output_img)
        # Type A) crop to fit
        output_imgRatio = output_img.size[0] / output_img.size[1]
        collage_ratio = int(targetWidth) / int(out_height)
        #pyotherside.send('debugPythonLogs', collage_ratio )
        if (output_imgRatio < collage_ratio):
            #pyotherside.send('debugPythonLogs', "crop verticals" )
            targetSize = ( targetWidth, int(targetWidth/output_imgRatio))
            output_img = output_img.resize(targetSize)
            diffVertical = (output_img.size[1] - int(out_height)) / 2 #center vertically
            area = ( 0, diffVertical, output_img.size[0], (diffVertical + int(out_height)) )
            output_img = output_img.crop(area)
        else:
            #pyotherside.send('debugPythonLogs', "crop horizontals" )
            targetSize = (int(out_height*output_imgRatio), int(out_height))
            output_img = output_img.resize(targetSize)
            diffHorizontal = (output_img.size[0] - targetWidth) / 2 #center horizontally
            area = ( diffHorizontal, 0, (diffHorizontal + targetWidth), int(out_height) )
            output_img = output_img.crop(area)
        # Type B) scale to fit
        #targetsize = (targetWidth, int(out_height))
        #output_img = output_img.resize(targetsize)
        output_img = output_img.filter(ImageFilter.GaussianBlur(int(targetBlur)))
    else:
        output_img = Image.new('RGBA', (targetWidth, int(out_height)), argb2rgba(targetBackColor) )

    # place images on collage
    x = targetSpacing
    y = targetSpacing
    for i in range(max(putLineList)+1):
        index_pos_list = get_index_positions(putLineList, i)
        imgPerRow = len(index_pos_list)
        for j in range(imgPerRow):
            output_img.paste( thumbnailImageList[index_pos_list[j]], (x, y), thumbnailImageList[index_pos_list[j]] )
            x += thumbnailImageList[index_pos_list[j]].size[0] + targetSpacing
        x = targetSpacing
        y += thumbnailImageList[index_pos_list[0]].size[1] + targetSpacing
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy, allImagesList, 0 )
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    output_img.close()
    thumbnailImageList.clear()
    putLineList.clear()


def createCollagePolaroids ( outputPathPy, inputPathPy, targetWidth, selectedPaths, shuffle, targetBackColor, targetColumns, targetSpacing, targetBlur, targetImage, targetFrameSetup, randomAngles, ratioWanted ):
    maxWidth = int( (targetWidth - ( (int(targetColumns)+1) * int(targetSpacing) )  )  / int(targetColumns) )
    allImagesList = list( selectedPaths.split(",") )
    thumbnailImageList = []
    randomAngleList = []
    ratioWanted = 1 / ratioWanted
    targetFrameColor = (targetFrameSetup.split(","))[0]
    targetFrameWidth = int( (targetFrameSetup.split(","))[1] )
    if "yes" in shuffle:
        random.shuffle(allImagesList)
        randomAngleList.clear()
    else:
        randomAngleList = list( randomAngles.split(",") )
    maxHeight = int(maxWidth * ratioWanted)

    lastImgWidthRow = []
    firstImgWidthRow = []
    firstImgHeightRow = []
    currentImgHeightRow = []
    lastImgHeightLine = [maxHeight]
    currentLine = 0
    counter = 0
    for i in range ( 0, len(allImagesList) ) :
        img = Image.open( "/" + allImagesList[i] ).convert('RGBA')
        img = ImageOps.exif_transpose(img)
        imageWidth, imageHeight = img.size
        imageRatio = imageWidth/imageHeight
        if (imageRatio > ratioWanted): #landscape
            new_Width = int( maxHeight * imageRatio )
            size = ( new_Width, maxHeight ) #keep height
            resized_img = img.resize(size)
            diffHorizontal = int( (new_Width - maxWidth)/2 ) #center horizontally
            area = ( diffHorizontal, 0, (diffHorizontal + maxWidth), maxHeight )
        else: #portrait
            new_Height = int( int(maxWidth / imageRatio) )
            size = ( maxWidth, new_Height ) #keep width
            resized_img = img.resize(size)
            diffVertical = int( (new_Height - maxHeight)/2 ) #center vertically
            area = ( 0, diffVertical, maxWidth, (diffVertical + maxHeight) )
        cropped_img = resized_img.crop(area)
        if "none" not in targetFrameColor:
            frameImg = Image.new('RGBA', ( cropped_img.size[0], cropped_img.size[1]), argb2rgba(targetFrameColor))
            innerImage = cropped_img.resize(( cropped_img.size[0] - 2*targetFrameWidth, cropped_img.size[1] - 2*targetFrameWidth ) )
            frameImg.paste( innerImage, (targetFrameWidth, targetFrameWidth), innerImage )
            cropped_img = frameImg
        if "yes" in shuffle:
            angle = int(gauss(0, 10)) #  use random angles: center, -mainOffset+
            randomAngleList.append(angle)
        else:
            angle = int(randomAngleList[i])
        cropped_img = cropped_img.rotate(angle, expand = True)
        thumbnailImageList.append (cropped_img)
        lastImgHeightLine.append( cropped_img.size[1] )

        if currentLine == 0: # patch: if there are less images than one row
            firstImgWidthRow.append(cropped_img.size[0])
            firstImgHeightRow.append(cropped_img.size[1])
            largestWidthFirstLine = max(firstImgWidthRow)
            largestHeightFirstLine = max(firstImgHeightRow)
        else:
            currentImgHeightRow.append(cropped_img.size[1])
            largestHeightLastLine= max(currentImgHeightRow)

        counter += 1
        if counter >= int(targetColumns):
            counter = 0
            currentLine += 1
            lastImgWidthRow.append( cropped_img.size[0] )
            largestHeightLastLine= max(lastImgHeightLine)
            lastImgHeightLine.clear()
            currentImgHeightRow.clear()

    # adjust out_height & targetWidth, since rotated images are larger
    cols = int(targetColumns)
    rows = math.ceil( len(allImagesList) / cols )
    out_height = int( rows * (maxHeight+int(targetSpacing)) + int(targetSpacing) )

    if len(firstImgWidthRow) < int(targetColumns): # patch: if there are less images than rows in first line
        out_height += largestHeightFirstLine - maxHeight
        targetWidth += largestWidthFirstLine - maxWidth
    else:
        targetWidth += max(lastImgWidthRow) - maxWidth
        out_height += largestHeightLastLine - maxHeight

    # generate main raster collage image
    if "image" in targetBackColor:
        output_img = Image.open( "/" + inputPathPy )
        #output_img = ImageOps.exif_transpose(output_img)
        output_img = output_img.convert('RGBA')
        # Type A) crop to fit
        output_imgRatio = output_img.size[0] / output_img.size[1]
        collage_ratio = int(targetWidth) / out_height
        if (output_imgRatio < collage_ratio):
            #pyotherside.send('debugPythonLogs', "crop verticals" )
            targetSize = ( int(targetWidth), int(int(targetWidth)/output_imgRatio))
            output_img = output_img.resize(targetSize)
            diffVertical = (output_img.size[1] - out_height) / 2 #center vertically
            area = ( 0, diffVertical, output_img.size[0], (diffVertical + out_height) )
            output_img = output_img.crop(area)
        else:
            #pyotherside.send('debugPythonLogs', "crop horizontals" )
            targetSize = (int(out_height*output_imgRatio), out_height)
            output_img = output_img.resize(targetSize)
            diffHorizontal = (output_img.size[0] - targetWidth) / 2 #center horizontally
            area = ( diffHorizontal, 0, (diffHorizontal + targetWidth), out_height )
            output_img = output_img.crop(area)
        # Type B) scale to fit
        #targetsize = (int(targetWidth), out_height)
        #output_img = output_img.resize(targetsize)
        output_img = output_img.filter(ImageFilter.GaussianBlur(int(targetBlur)))
    else:
        output_img = Image.new('RGBA', (int(targetWidth), out_height), argb2rgba(targetBackColor))
    i = 0
    x = 0 + int(targetSpacing)
    y = 0 + int(targetSpacing)
    for row in range(rows):
        for col in range(cols):
            if ( i < len(thumbnailImageList) ):
                output_img.paste( thumbnailImageList[i], (x, y), thumbnailImageList[i] )
            i += 1
            x += int(maxWidth) + int(targetSpacing)
        x = 0 + int(targetSpacing)
        y += int(maxHeight) + int(targetSpacing)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy, allImagesList, randomAngleList)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    output_img.close()
    thumbnailImageList.clear()
    randomAngleList.clear()
    lastImgWidthRow.clear()
    firstImgWidthRow.clear()
    firstImgHeightRow.clear()
    currentImgHeightRow.clear()
    lastImgHeightLine.clear()


def createCollageColumns ( outputPathPy, inputPathPy, targetWidth, selectedPaths, shuffle, targetBackColor, targetColumns, targetSpacing, targetBlur, targetImage, targetFrameSetup ):
    allImagesList = list( selectedPaths.split(",") )
    targetFrameColor = (targetFrameSetup.split(","))[0]
    targetFrameWidth = int( (targetFrameSetup.split(","))[1] )
    targetColumns = int(targetColumns)
    if "yes" in shuffle:
        random.shuffle(allImagesList)
    init_Width = int(int(targetWidth) / targetColumns)
    targetSpacing = int(targetSpacing)

    # first get images in lists, each list represents one column
    thumbnailImageList = [ [] for i in range(targetColumns) ]
    thumbnailHeightsList = [ [] for i in range(targetColumns) ]
    totalColumnHeightList = [ targetSpacing ] * targetColumns # total list height including pacings
    for i in range ( 0, len(allImagesList) ) :
        img = Image.open( "/" + allImagesList[i] ).convert('RGBA')
        img = ImageOps.exif_transpose(img)
        init_Ratio = img.size[0] / img.size[1]
        init_Height = int(init_Width / init_Ratio)
        img = img.resize( (init_Width, init_Height) )

        # get the lowest column and put image there, recalculate current column height
        putInColumn = totalColumnHeightList.index(min(totalColumnHeightList)) # gets first index only!!!
        thumbnailImageList[putInColumn].append(img)
        thumbnailHeightsList[putInColumn].append(img.size[1])
        totalColumnHeightList[putInColumn] = totalColumnHeightList[putInColumn] + img.size[1] + targetSpacing

    # rescale all images to match one common column height
    for i in range(len(thumbnailImageList)):
        columnScalingFactor = ( sum(thumbnailHeightsList[i]) + (len(thumbnailHeightsList[i])-1) * targetSpacing) / max(totalColumnHeightList)
        for j in range(len(thumbnailImageList[i])) :
            cropped_img = ImageOps.scale( thumbnailImageList[i][j], 1/columnScalingFactor )
            if "none" not in targetFrameColor:
                frameImg = Image.new('RGBA', ( cropped_img.size[0], cropped_img.size[1]), argb2rgba(targetFrameColor))
                innerImage = cropped_img.resize(( cropped_img.size[0] - 2*targetFrameWidth, cropped_img.size[1] - 2*targetFrameWidth ) )
                frameImg.paste( innerImage, (targetFrameWidth, targetFrameWidth), innerImage )
                cropped_img = frameImg
            thumbnailImageList[i][j] = cropped_img

    # create background image
    newColumnHeightsList = []
    out_width = targetSpacing
    for i in range(len(thumbnailImageList)): # how many columns
        totalColumnHeight = targetSpacing
        for j in range(len(thumbnailImageList[i])): # how many images)
            totalColumnHeight += thumbnailImageList[i][j].size[1] + targetSpacing
        newColumnHeightsList.append(totalColumnHeight)
        out_width += thumbnailImageList[i][0].size[0] + targetSpacing
    out_height = max(newColumnHeightsList)

    if "image" in targetBackColor:
        output_img = Image.open( "/" + inputPathPy )
        #output_img = ImageOps.exif_transpose(output_img)
        output_img = output_img.convert('RGBA')
        # Type A) crop to fit
        output_imgRatio = output_img.size[0] / output_img.size[1]
        collage_ratio = out_width / out_height
        if (output_imgRatio < collage_ratio):
            #pyotherside.send('debugPythonLogs', "crop verticals" )
            targetSize = ( out_width, int(out_width/output_imgRatio))
            output_img = output_img.resize(targetSize)
            diffVertical = (output_img.size[1] - out_height) / 2 #center vertically
            area = ( 0, diffVertical, output_img.size[0], (diffVertical + out_height) )
            output_img = output_img.crop(area)
        else:
            #pyotherside.send('debugPythonLogs', "crop horizontals" )
            targetSize = (int(out_height*output_imgRatio), out_height)
            output_img = output_img.resize(targetSize)
            diffHorizontal = (output_img.size[0] - out_width) / 2 #center horizontally
            area = ( diffHorizontal, 0, (diffHorizontal + out_width), out_height )
            output_img = output_img.crop(area)
        # Type B) scale to fit
        #targetsize = (int(out_width), out_height)
        #output_img = output_img.resize(targetsize)
        output_img = output_img.filter(ImageFilter.GaussianBlur(int(targetBlur)))
    else:
        output_img = Image.new('RGBA', (out_width, out_height), argb2rgba(targetBackColor))

    # place images on collage on this background image
    x = targetSpacing
    y = targetSpacing
    for i in range(len(thumbnailImageList)): # how many columns
        for j in range(len(thumbnailImageList[i])): # how many images
            output_img.paste( thumbnailImageList[i][j], (x, y), thumbnailImageList[i][j] )
            y += thumbnailImageList[i][j].size[1] + targetSpacing
        x += thumbnailImageList[i][j].size[0] + targetSpacing
        y = targetSpacing

    outputRatio = output_img.size[0] / output_img.size[1]
    output_img = output_img.resize( (int(targetWidth), int(targetWidth/outputRatio)) )
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy, allImagesList, 0 )
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    output_img.close()
    thumbnailImageList.clear()
    thumbnailHeightsList.clear()
    totalColumnHeightList.clear()
    newColumnHeightsList.clear()


def createCollageScattered ( outputPathPy, inputPathPy, targetWidth, selectedPaths, shuffle, targetBackColor, targetColumns, targetSpacing, targetBlur, targetImage, targetFrameSetup, randomAngles, ratioWanted ):
    maxWidth = int( (targetWidth - ( (int(targetColumns)+1) * int(targetSpacing) )  )  / int(targetColumns) )
    allImagesList = list( selectedPaths.split(",") )
    thumbnailImageList = []
    randomAngleList = []
    ratioWanted = 1 / ratioWanted
    targetFrameColor = (targetFrameSetup.split(","))[0]
    targetFrameWidth = int( (targetFrameSetup.split(","))[1] )
    if "yes" in shuffle:
        random.shuffle(allImagesList)
        randomAngleList.clear()
    else:
        randomAngleList = list( randomAngles.split(",") )
    maxHeight = int(maxWidth * ratioWanted)

    lastImgWidthRow = []
    firstImgWidthRow = []
    firstImgHeightRow = []
    currentImgHeightRow = []
    lastImgHeightLine = [maxHeight]
    currentLine = 0
    counter = 0
    for i in range ( 0, len(allImagesList) ) :
        img = Image.open( "/" + allImagesList[i] ).convert('RGBA')
        img = ImageOps.exif_transpose(img)
        img.thumbnail( (maxWidth, maxWidth) )
        cropped_img = img
        if "none" not in targetFrameColor:
            frameImg = Image.new('RGBA', ( cropped_img.size[0], cropped_img.size[1]), argb2rgba(targetFrameColor))
            innerImage = cropped_img.resize(( cropped_img.size[0] - 2*targetFrameWidth, cropped_img.size[1] - 2*targetFrameWidth ) )
            frameImg.paste( innerImage, (targetFrameWidth, targetFrameWidth), innerImage )
            cropped_img = frameImg
        if "yes" in shuffle:
            angle = int(gauss(0, 25)) #  use random angles: center, -mainOffset+ # standard: 10
            randomAngleList.append(angle)
        else:
            angle = int(randomAngleList[i])
        cropped_img = cropped_img.rotate(angle, expand = True)
        thumbnailImageList.append (cropped_img)
        lastImgHeightLine.append( cropped_img.size[1] )

        if currentLine == 0: # patch: if there are less images than one row
            firstImgWidthRow.append(cropped_img.size[0])
            firstImgHeightRow.append(cropped_img.size[1])
            largestWidthFirstLine = max(firstImgWidthRow)
            largestHeightFirstLine = max(firstImgHeightRow)
        else:
            currentImgHeightRow.append(cropped_img.size[1])
            largestHeightLastLine= max(currentImgHeightRow)

        counter += 1
        if counter >= int(targetColumns):
            counter = 0
            currentLine += 1
            lastImgWidthRow.append( cropped_img.size[0] )
            largestHeightLastLine= max(lastImgHeightLine)
            lastImgHeightLine.clear()
            currentImgHeightRow.clear()

    # adjust out_height & targetWidth, since rotated images are larger
    cols = int(targetColumns)
    rows = math.ceil( len(allImagesList) / cols )
    out_height = int( rows * (maxHeight+int(targetSpacing)) + int(targetSpacing) )

    if len(firstImgWidthRow) < int(targetColumns): # patch: if there are less images than rows in first line
        out_height += largestHeightFirstLine - maxHeight
        targetWidth += largestWidthFirstLine - maxWidth
    else:
        targetWidth += max(lastImgWidthRow) - maxWidth
        out_height += largestHeightLastLine - maxHeight

    # generate main raster collage image
    if "image" in targetBackColor:
        output_img = Image.open( "/" + inputPathPy )
        #output_img = ImageOps.exif_transpose(output_img)
        output_img = output_img.convert('RGBA')
        # Type A) crop to fit
        output_imgRatio = output_img.size[0] / output_img.size[1]
        collage_ratio = int(targetWidth) / out_height
        if (output_imgRatio < collage_ratio):
            #pyotherside.send('debugPythonLogs', "crop verticals" )
            targetSize = ( int(targetWidth), int(int(targetWidth)/output_imgRatio))
            output_img = output_img.resize(targetSize)
            diffVertical = (output_img.size[1] - out_height) / 2 #center vertically
            area = ( 0, diffVertical, output_img.size[0], (diffVertical + out_height) )
            output_img = output_img.crop(area)
        else:
            #pyotherside.send('debugPythonLogs', "crop horizontals" )
            targetSize = (int(out_height*output_imgRatio), out_height)
            output_img = output_img.resize(targetSize)
            diffHorizontal = (output_img.size[0] - targetWidth) / 2 #center horizontally
            area = ( diffHorizontal, 0, (diffHorizontal + targetWidth), out_height )
            output_img = output_img.crop(area)
        # Type B) scale to fit
        #targetsize = (int(targetWidth), out_height)
        #output_img = output_img.resize(targetsize)
        output_img = output_img.filter(ImageFilter.GaussianBlur(int(targetBlur)))
    else:
        output_img = Image.new('RGBA', (int(targetWidth), out_height), argb2rgba(targetBackColor))
    i = 0
    x = 0 + int(targetSpacing)
    y = 0 + int(targetSpacing)
    for row in range(rows):
        for col in range(cols):
            if ( i < len(thumbnailImageList) ):
                output_img.paste( thumbnailImageList[i], (x, y), thumbnailImageList[i] )
            i += 1
            x += int(maxWidth) + int(targetSpacing)
        x = 0 + int(targetSpacing)
        y += int(maxHeight) + int(targetSpacing)
    output_img.save(outputPathPy, compress_level=1)
    if "preview" in targetImage:
        pyotherside.send('previewImageCreated', outputPathPy, allImagesList, randomAngleList)
    else:
        pyotherside.send('exchangeImage', outputPathPy)
    output_img.close()
    thumbnailImageList.clear()
    randomAngleList.clear()
    lastImgWidthRow.clear()
    firstImgWidthRow.clear()
    firstImgHeightRow.clear()
    currentImgHeightRow.clear()
    lastImgHeightLine.clear()
















multiPagePDFImagesList = []
multiPagePDFSourceNames = ""
def gatherMultiPagePdfFunction ( inputPathPy, pageNumber, multiPdfPageNamesList ) :
    global multiPagePDFSourceNames
    global multiPagePDFImagesList
    multiPagePDFSourceNames = multiPdfPageNamesList
    img_multipdf = Image.open( "/" + inputPathPy)
    img_multipdf = ImageOps.exif_transpose(img_multipdf)
    img_multipdf = img_multipdf.convert("RGB")
    multiPagePDFImagesList.append(img_multipdf)
    pyotherside.send('fileMultiPagePdfIsAdded',)
    # img_multipdf can not be closed, otherwise no new images added

def getMultiPdfPagesFunction () :
    global multiPagePDFSourceNames
    global multiPagePDFImagesList
    pagesCounter = len(multiPagePDFImagesList)
    pyotherside.send('getPagesMultiPDF', pagesCounter, multiPagePDFSourceNames)

def deleteTempMultiPagePDF( tempImageFolderPath ) :
    global multiPagePDFSourceNames
    global multiPagePDFImagesList
    multiPagePDFSourceNames = ""
    multiPagePDFImagesList.clear()
    getMultiPdfPagesFunction()
    pyotherside.send('tempMultiPDFfilesDeleted',)

def createMultiPagePDFFunction( outputPathPy, tempImageFolderPath ) :
    global multiPagePDFSourceNames
    global multiPagePDFImagesList
    multiPagePDFImagesList[0].convert("RGB").save( outputPathPy, save_all = True, quality=100, append_images = multiPagePDFImagesList[1:] )
    pyotherside.send('fileIsSaved', )
    deleteTempMultiPagePDF( tempImageFolderPath )

    #pyotherside.send('debugPythonLogs', i)
