# stop action movie program
# v3 is the base working version
# v4 adds display of grid lines
# v5 adds command line parsing
# v6 adds debug using actual program name
# v7 adds support for specifying the webcame number and grid spacing

import cv2
import time
import argparse
# import numpy as np

ESCAPE_KEY = 27
SPACE_BAR = 32
LOWERCASE_C = 99
LOWERCASE_G = 103
LOWERCASE_S = 115
OUTPUT_FILETYPE = ".png"
ALPHA = 0.65
GRID_LINE_COLOR = (50, 50, 50)   
GRID_LINE_WIDTH = 1
GRID_SPACING = 15
WEBCAM_0 = 0					# default webcam to use

def debug(programName, displayText):
	if printDebugMessages:
		print programName + ':', displayText
	return

parser = argparse.ArgumentParser(description='Stop action movie recorder')
parser.add_argument('moviename',  help='file name of the stop action movie')
parser.add_argument('-d', '--debug', dest='debugSwitch', action='store_true', help='display debugging messages')
parser.add_argument('-g', '--gridlines', dest='gridlinesSwitch', action='store_true', help='display grid lines')
parser.add_argument('-s', '--spacing', dest='gridSpacing', default=GRID_SPACING, type=int, help='grid spacing (pixels)' )
parser.add_argument('-w', '--webcam', dest='webcamNumber', default=WEBCAM_0, type=int, help='number of the webcam to use')
parser.add_argument('-r', '--reverseimages', dest='reverseImagesSwitch', action='store_true', help='reverses the foreground and background images')
args = parser.parse_args()

progName = parser.prog.rsplit( ".", 1 )[ 0 ]
outputFilename = args.moviename
printDebugMessages = args.debugSwitch
displayGrid = args.gridlinesSwitch
reverseImages = args.reverseImagesSwitch
webcamNumber = args.webcamNumber
gridSpacing = args.gridSpacing

debug(progName, 'movie name is ' + outputFilename)
debug(progName, 'debug is set to ' + str(printDebugMessages))
debug(progName, 'grid display is initially set to ' + str(displayGrid))
debug(progName, 'reverse images is set to ' + str(reverseImages))
debug(progName, 'webcam ' + str(webcamNumber) + ' will be used')

file_number = 0		# number of images written to disk

debug(progName, 'opening webcam. file name being used is ' + outputFilename)

cap = cv2.VideoCapture(webcamNumber)
if not cap.isOpened():
	raise IOError('cannot open webcam')

debug(progName, 'waiting for webcam to open')
time.sleep(2)  # wait two seconds for webcam to actually open

# capture the initial image
successfulCapture, prevImage = cap.read()
debug(progName, 'captured initial image')
height, width, channels = prevImage.shape
debug(progName, 'height=' + str(height) + ' width=' + str(width) + ' channels=' + str(channels))

if successfulCapture:
	# cv2.imshow('prevImage', prevImage)

	while True:
		# capture a new image
		successfulCapture, curImage = cap.read()
		if successfulCapture:
			
			dispImage = curImage.copy()  # make a copy of the current image that will be used for displaying
			
			# ghost image is the new image
			if reverseImages:
				# ghost image will be the new image
				cv2.addWeighted(prevImage, ALPHA, dispImage, 1 - ALPHA, 0, dispImage)  # add shadow of previous image to display
			else:
				# ghost image will be the previous image
				cv2.addWeighted(dispImage, ALPHA, prevImage, 1 - ALPHA, 0, dispImage)

			if displayGrid:
				for h in range(0, height + 1, gridSpacing):
					cv2.line(dispImage, (0, h), (width, h), GRID_LINE_COLOR, GRID_LINE_WIDTH)
				for w in range(0, width + 1, gridSpacing):
					cv2.line(dispImage, (w, 0), (w, height), GRID_LINE_COLOR, GRID_LINE_WIDTH)
			cv2.imshow('dispImage', dispImage)
			
			c = cv2.waitKey(1)
			# if the space bar is pressed, save the current image
			if c == SPACE_BAR:
				file_number = file_number + 1
				fn = outputFilename + "." + str(file_number).zfill(3) + OUTPUT_FILETYPE
				cv2.imwrite(fn, curImage)
				prevImage = curImage
				debug(progName, 'image saved as ' + fn)
			# if 'g' is pressed toggle the grid on or off
			if c == LOWERCASE_G:
				displayGrid = not displayGrid
				if displayGrid:
					debug(progName, 'grid lines are now ON')
				else:
					debug(progName, 'grid lines are now OFF')
			# if 'ESC' is pressed, write the number of images to a file and stop capturing images
			if c == ESCAPE_KEY:
				if file_number > 0:
					fn = outputFilename + ".count"
					f = open(fn, "w")
					f.write(str(file_number))
					f.close()
					debug(progName, 'count file written; total count is ' + str(file_number))
				break
		else:
			print "unable to read webcam image in loop"
			break
else:
	print "unable to read initial webcam image"

# release the camera and close the display windows
cap.release()
cv2.destroyAllWindows()
debug(progName, 'exiting stop action recorder')
