#written by Joel Wildman (22984156)

import numpy as np 
import matplotlib.pyplot as plt
import tkinter as tk
import cv2
import tkinter.filedialog as filedialog
from PIL import ImageTk, Image
import skimage


from skimage import filters, segmentation, measure, morphology, color, util



#import image

def load_image():
	filename = filedialog.askopenfilename()
	print(filename)
	if (filename == ""):
		print('Please enter a valid file')
		exit()

	input_image = cv2.imread(filename)
	return input_image

image = load_image()

#colour boundaries in HSV space:
blue_bounds = ([90,50,50], [150, 255, 255])
green_bounds = ([30, 50, 50], [90, 255, 255])
red_bounds = ([150, 50, 50], [180, 255, 255])

#here we can consider true blue to be 120, true green to be 60 and true red to be 180, with a diffcolour of 30

bounds = [blue_bounds, green_bounds, red_bounds]

#convert image to hsv to better colour match
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#variable to store final mask output
final_mask = np.zeros((image.shape[0], image.shape[1]), dtype="uint8")


for target in bounds:
	#convert to cv2 friendly types
	lower_bound = np.array(target[0], dtype="uint8")
	upper_bound = np.array(target[1], dtype="uint8")
	#create a mask of image using these values
	mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
	
	#apply this mask to the original image
	filtered = cv2.bitwise_and(image, image, mask=mask)

	#and record it for the final mask
	final_mask = cv2.bitwise_or(final_mask, mask)

	#remove blobs that are too big

	cv2.imshow("Filtered Image", np.hstack([image,filtered]))
	cv2.waitKey(0)


filtered = cv2.bitwise_and(image, image, mask=final_mask)
cv2.imshow("Filtered Image", np.hstack([image,filtered]))
cv2.waitKey(0)