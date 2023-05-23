#written by Joel Wildman (22984156)
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.textpath import TextPath
import tkinter as tk
import cv2
import tkinter.filedialog as filedialog
from PIL import ImageTk, Image
import skimage
import math
from skimage import filters, segmentation, measure, morphology, color, util

#import image
def load_image(filename):
	if (filename == ""):
		print('Please enter a valid file')
		exit()

	input_image = cv2.imread(filename)
	return input_image


#return the distance between two pixels
def distance(source, dest):
	xdist = abs(source[0] - dest[0])
	ydist = abs(source[1] - dest[1])
	euc_dist = math.sqrt(xdist**2 + ydist**2)
	return euc_dist


#remove all pixels too far from desired colours and return mask
def cull_by_colour(image):

	#colour boundaries in HSV space:
	blue_bounds = ([90,50,50], [150, 255, 255])
	green_bounds = ([30, 30, 30], [90, 255, 255])
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

		#cv2.imshow("Filtered Image", np.hstack([image,filtered]))
		#cv2.waitKey(0)

	return final_mask


#remove regions that are too small or too big
def cull_by_size(candidates, min_area, max_area):
	new_candidates = []
	for candidate in candidates:
		if candidate.area >= min_area and candidate.area <= max_area:
			new_candidates.append(candidate)

	return np.array(new_candidates)


#remove regions that are too far from round
def cull_by_roundness(candidates, axis_ratio):
	new_candidates = []
	for candidate in candidates:
		#make our division safe
		if (candidate.axis_major_length != 0 and candidate.axis_minor_length):
			#disregard regions that are too far from round by finding the ratio of their eigenvalues on the minor and major axes
			if (math.sqrt(candidate.inertia_tensor_eigvals[1])/math.sqrt(candidate.inertia_tensor_eigvals[0]) > axis_ratio):
				new_candidates.append(candidate)

	return np.array(new_candidates)



#remove regions that do not form an ellipse with neighbouring regions
def cull_by_neighbours(candidates, ellipse_threshold, coloured):
	new_candidates = []
	visited = []
	centroid_coords = []
	candidate_region =[]
	#find the closest 5 regions to main_region
	for i, main_region in enumerate(candidates):
		if main_region in visited: #Saves time i think lol
			continue
		main_centroid = main_region.centroid
		centroid_coords.append(main_centroid)
		distances = []

		for close_region in candidates:
			#list the distances to all nodes
			if close_region == 0:
				distances.append(9999)
				continue
			close_centroid = close_region.centroid
			distances.append(distance(main_centroid, close_centroid))
			

		#get indices of the closest 5 including itself
		neighbours = np.argsort(distances)[:6]
		#get their coordinates (and add the current region to complete the set)
		close_coords = []
		for region in neighbours:
			close_coords.append(candidates[region].centroid)
			

		#match elipse
		ellipse = measure.EllipseModel()
		if (ellipse.estimate(np.array(close_coords))):
			data_residuals = ellipse.residuals(np.array(close_coords))

		#Check if shape forms a hexagon with red and green colours
		hexagon, HexaString = checkHexagon(coloured, neighbours, candidates) 
		if not hexagon:
			continue
		#check if largest residual error value is above acceptable threshold
		if (max(data_residuals) < ellipse_threshold):
			# new_candidates.append(main_region)
			candidate_array = []
			for region in neighbours:
				new_candidates.append(candidates[region])
				visited.append(candidates[region])
				candidate_array.append(candidates[region])
			candidate_region.append(candidate_array)
		else: 
			candidates[i] = 0

	return np.array(new_candidates), candidate_region

#Preemptively running an extract from the function in TASK 2 to eliminate false detections
def checkHexagon(coloured, candidate_List, candidates ):
	hexagon = []
	for ind in candidate_List:
		hexagon.append(candidates[ind])
	deepestHex = sorted(hexagon, key=lambda x: x.centroid[0])
	totalHue = 0
	for x, y in  deepestHex[0].coords:
		totalHue += coloured[x,y][0]
	avgHue = totalHue / len( deepestHex[0].coords)
	if 85 < avgHue and avgHue < 151:
		top_region = deepestHex[0]
	else:
		return False, 1

	sorted_hexagon = [top_region]*6 
	sorted_hexagon[3] = deepestHex[5] #bottom
	finalString = "HexaTarget_"
	hex_string = [""]*5

	for ind in range(1,3):
		region = deepestHex[ind]
		if top_region.centroid[1]  < region.centroid[1]:
			sorted_hexagon[1] = region
		else:
			sorted_hexagon[5] = region
	for ind in range(3,5):
		region = deepestHex[ind]
		if top_region.centroid[1]  < region.centroid[1]:
			sorted_hexagon[2] = region
		else:
			sorted_hexagon[4] = region

	for ind, region in enumerate(sorted_hexagon):
		totalHue = 0
		for x, y in  region.coords:
			totalHue += coloured[x,y][0]
		avgHue = totalHue / len(region.coords)
		if 30 < avgHue and avgHue < 110: #Green
			hex_string[ind-1] = 'G'
		elif 140< avgHue and avgHue < 180: #Red
			hex_string[ind-1] = 'R'
		else:
			hex_string[ind-1] = '?'


	for c in hex_string: 
		finalString = finalString+ c

	if '?' in hex_string:
		return False, 1

	return sorted_hexagon, finalString


