# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 11:57:41 2021

@author: aporal
"""

#this opens the GUI that allows the user to select a folder
from tkinter import filedialog
from tkinter import *
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

#this imports the images into a list
from PIL import Image
import os, os.path

imgs = []
path = folder_selected
valid_images = [".jpg",".gif",".png",".tif"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs.append(Image.open(os.path.join(path,f)))
    
os.chdir(path)
allfiles=os.listdir(os.getcwd())
imlist=[filename for filename in allfiles if filename[-4:] in [".jpg",".gif",".png",".tif"]]

# Assuming all images are the same size, get dimensions of first image
w,h=Image.open(imlist[0]).size

N=len(imlist)

# Create a numpy array of floats to store the average (assume RGB images)
import numpy as np
arr=np.empty((h,w),np.uint8)

# Build up average pixel intensities, casting each image as an array of floats
# This looks like mean rather than median though
count = 0
for im in imlist:
    imarr=np.array(Image.open(im).convert("L"),dtype=np.uint8)
    if count == 0:
        arr=imarr
        count += 1
    else:
        arr=np.append(arr,imarr, axis=0)
        count += 1

# Round values in array and cast as 8-bit integer
arr = np.array(np.round(arr),dtype=np.uint8)
arr = np.array_split(arr, N, axis=0)
arr = np.median(arr, axis=0)
arr = arr.astype("uint8")
# Generate, save and preview final image
out=Image.fromarray(arr,mode="L")
root = Tk()
root.withdraw()
output_folder = filedialog.askdirectory()
os.chdir(output_folder)
out.save("Average.tif")
out.show()