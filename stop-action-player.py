# plays stop action movies created by stop-action-record
# v2 adds command line support

import cv2
import sys
import time
import argparse
import os

RBG_GREEN = (0, 255, 0)		# green (red, green, blue)
FILE_TYPE = '.png'			# images will be saved as .png files
COUNT_TYPE = '.count'		# file type for the file containing the image count
TEXT_COLOR = RBG_GREEN		# frame number text color
TEXT_THICKNESS = 1			# frame number text thickness
TEXT_ORIGIN = (10, 25)		# location to place frame number text
TEXT_FONT_SCALE = 0.65		# font size for frame number textpress
DEFAULT_DELAY_MS = 100		# default delay between frames in milliseconds
ESCAPE_KEY = 27				# ASCII value for the ESC key
LOWERCASE_F = 102 			# ASCII value for 'f'
READ_ONLY = 'r'				# read only parameter for opening files

# print debugging messages prefixed by the name of the program
def debug(programName, displayText):
	if printDebugMessages:
		print programName + ':', displayText
	return

# extract the parameters specified on the command line
parser = argparse.ArgumentParser(description='Stop action movie player')
parser.add_argument('moviename',  help='file name of the stop action movie')
parser.add_argument('-t', '--timebetweenframes', dest='timeDelay', default=DEFAULT_DELAY_MS, type=int, help='time delay between displaying frames (milliseconds)')
parser.add_argument('-s', '--suppressframenumbers', dest='suppressFrameText', action='store_true', help='suppress display of frame numbers')
parser.add_argument('-d', '--debug', dest='debugSwitch', action='store_true', help='display debugging messages')
args = parser.parse_args()

# save the values from the command parser
progName = parser.prog.rsplit( ".", 1 )[ 0 ]		# remove the .py from the program name
movieName = args.moviename
timeBetweenFrames = args.timeDelay
printDebugMessages = args.debugSwitch
suppressFrameText = args.suppressFrameText

framesPerSecond = 1000.0 / timeBetweenFrames
print "FPS: ", framesPerSecond

# display the command parameters if debug is turned on
debug(progName, 'movie name is ' + movieName)
debug(progName, 'time delay between frame is ' + str(timeBetweenFrames))
debug(progName, 'debug is set to ' + str(printDebugMessages))

# construct the file name for file containing the count of images in the movie
fn = movieName + COUNT_TYPE
debug(progName, 'count file name is ' + fn)

# verify the frame count file exists before trying to open it
if os.path.isfile(fn):
	f = open(fn, READ_ONLY)
	
	# read the number of frames in the moview
	count = int(f.read())
	debug(progName, 'frame count is ' + str(count))

	# close the frame count file
	f.close()

	# loop reading and displaying all the frames until the ESC key is pressed
	keep_playing = True
	while keep_playing:										# play the movie until the user presses the escape key
		for i in range(count):								# loop through all the image files
			sequence = str(i+1).zfill(3)					# construct the image number used in the file name
			fn = movieName + "." + sequence + FILE_TYPE		# construct the file name
			debug(progName, 'displaying ' + fn)

			# verify the frame image file exists before trying to read it
			if os.path.isfile(fn):

				dispImage = cv2.imread(fn, 1)					# read the frame image file
			
				# add the frame number text to the image and then display the image
				if not suppressFrameText:
					frameText = 'FPS: ' + str(framesPerSecond) + ' Frame: ' + sequence
					cv2.putText(dispImage, frameText, TEXT_ORIGIN, cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS)

				# display the frame
				cv2.imshow(movieName, dispImage)

				# wait for the specified time between frames and then check the keyboard
				c = cv2.waitKey(timeBetweenFrames)

				# if lower case f is pressed, toggle the display of the frame numbers
				if c == LOWERCASE_F:
					suppressFrameText = not suppressFrameText

				# if the escape key was pressed exit the loops
				if c == ESCAPE_KEY:
					keep_playing = False
					break

			# the frame file does not exist: print an error and exit
			else:
				print "frame file " + fn + " does not exist"
				sys.exit()

	# clean everything up and exit
	cv2.destroyAllWindows()

# the frame count file does not exist: print an error message
else:
	print "can not open frame count file " + fn

debug(progName, 'exiting')
