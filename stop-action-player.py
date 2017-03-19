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
DEFAULT_FPS = 10			# default frames per second
ESCAPE_KEY = 27				# ASCII value for the ESC key
LOWERCASE_F = 102 			# ASCII value for 'f'
READ_ONLY = 'r'				# read only parameter for opening files
BACKWARDS = 'backwards'     # text to use in messages about playback sequence
FORWARDS = 'forwards'		# text to use in messages about playback sequence
FIRST_FRAME_REPEAT = 0 		# number of times to repeat the frst frame on playback
LAST_FRAME_REPEAT = 0		# number of times to repeat the last frame on playback

# print debugging messages prefixed by the name of the program
def debug(programName, displayText):
	if printDebugMessages:
		print programName + ':', displayText
	return

# extract the parameters specified on the command line
parser = argparse.ArgumentParser(description='Stop action movie player')
parser.add_argument('moviename',  help='file name of the stop action movie')
parser.add_argument('-f', '--FPS', dest='framesPerSecond', default=DEFAULT_FPS, type=int, help='frames per second')
parser.add_argument('-s', '--suppressframenumbers', dest='suppressFrameText', action='store_true', help='suppress display of frame numbers')
parser.add_argument('-d', '--debug', dest='debugSwitch', action='store_true', help='display debugging messages')
parser.add_argument('-b', '--playbackwards', dest='playBackwards', action='store_true', help='play the movie backwards')
parser.add_argument('-a', '--firstframerepeat', dest='firstFrameRepeat', default=FIRST_FRAME_REPEAT, type=int, help='number of times to repeat the first frame on playback')
parser.add_argument('-z', '--lastframerepeat', dest='lastFrameRepeat', default=LAST_FRAME_REPEAT, type=int, help='number of times to repeat the last frame on playback')
args = parser.parse_args()

# save the values from the command parser
progName = parser.prog.rsplit( ".", 1 )[ 0 ]		# remove the .py from the program name
movieName = args.moviename
framesPerSecond = args.framesPerSecond
printDebugMessages = args.debugSwitch
suppressFrameText = args.suppressFrameText
playBackwards = args.playBackwards
firstFrameRepeat = args.firstFrameRepeat
lastFrameRepeat = args.lastFrameRepeat

# check for invalid frames per second setting
if framesPerSecond < 1:
	print "frames per second must be one or higher"
	sys.exit()

# determine how to play the movie
playSetting = BACKWARDS if playBackwards else FORWARDS

# calculate the delay in millseconds between frames
timeBetweenFrames = int(1000 / framesPerSecond)

# display the command parameters if debug is turned on
debug(progName, 'movie name is ' + movieName)
debug(progName, 'frames per second are ' + str(framesPerSecond))
debug(progName, 'time delay between frame is ' + str(timeBetweenFrames))
debug(progName, 'debug is set to ' + str(printDebugMessages))
debug(progName, 'movie will be played ' + playSetting)
debug(progName, 'first frame will be repeated ' + str(firstFrameRepeat) + ' times')
debug(progName, 'last frame will be repeated ' + str(lastFrameRepeat) + ' times')

# construct the file name for file containing the count of images in the movie
fn = movieName + COUNT_TYPE
debug(progName, 'count file name is ' + fn)

# verify the frame count file exists before trying to open it
if os.path.isfile(fn):
	f = open(fn, READ_ONLY)
	
	# read the number of frames in the moview
	count = int(f.read())
	debug(progName, 'frame count is ' + str(count))

	if count < 2:
		print "movie must contain at least two frames"
		sys.exit()

	# close the frame count file
	f.close()

	# loop reading and displaying all the frames until the ESC key is pressed
	keep_playing = True

	# create the sequence of frames to play
	playSequence = range(1, count + 1, 1)

	# if play backwards was specified, reverse the play sequence
	if playBackwards:
		playSequence.reverse()

	debug(progName, 'frame play sequence: ' + str(playSequence))

	firstFrame = playSequence[0]							# get the first frame in the sequence specified by the user
	lastFrame = playSequence[-1] 							# get the last frame in the sequence specified by the user

	debug(progName, 'first frame is ' + str(firstFrame))
	debug(progName, 'last frame is ' + str(lastFrame))
			
	while keep_playing:										# play the movie until the user presses the escape key		

		for i in playSequence:								# loop through all the image files
			sequence = str(i).zfill(3)						# construct the image number used in the file name
			fn = movieName + "." + sequence + FILE_TYPE		# construct the file name
			debug(progName, 'displaying ' + fn)

			# verify the frame image file exists before trying to read it
			if os.path.isfile(fn):

				# read the image from the file
				dispImage = cv2.imread(fn, 1)					

				# ensure c has a value since some paths do not call waitkey
				c = 0

				# if this is the first frame, repeat it according to what the user specified
				if i == firstFrame:

					# display the first frame the number of times specified
					for r in range(0, firstFrameRepeat):

						debug(progName, 're-displaying ' + fn + ' ' + str(r).zfill(3))

						# make a copy of the image so there's a clean copy used to add text each iteration
						dispTempImage = dispImage.copy()

						# check to see whether to suppress the display of frames per second, frame number, and repeat number
						if not suppressFrameText:
							frameText = 'FPS: ' + str(framesPerSecond) + ' Frame: ' + sequence + ' Repeat: ' + str(r).zfill(3)
							cv2.putText(dispTempImage, frameText, TEXT_ORIGIN, cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS)

						# display the frame
						cv2.imshow(movieName, dispTempImage)

						# delay between frames and check to see if a key was pressed
						c = cv2.waitKey(timeBetweenFrames)

						# if lower case f is pressed, toggle the display of the frame numbers
						if c == LOWERCASE_F:
							suppressFrameText = not suppressFrameText

						# if the escape key was pressed exit the loops
						if c == ESCAPE_KEY:
							keep_playing = False
							break

				# if this is the last frame, repeat it according to what the user specified
				elif i == lastFrame:

					# display the last frame the number of times specified					
					for r in range(0, lastFrameRepeat):
						debug(progName, 're-displaying ' + fn + ' ' + str(r).zfill(3))

						# make a copy of the image so there's a clean copy used to add text each iteration
						dispTempImage = dispImage.copy()

						# check to see whether to suppress the display of frames per second, frame number, and repeat number
						if not suppressFrameText:
							frameText = 'FPS: ' + str(framesPerSecond) + ' Frame: ' + sequence + ' Repeat: ' + str(r).zfill(3)
							cv2.putText(dispTempImage, frameText, TEXT_ORIGIN, cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS)

						# display the frame
						cv2.imshow(movieName, dispTempImage)

						# delay between frames and check to see if a key was pressed
						c = cv2.waitKey(timeBetweenFrames)

						# if lower case f is pressed, toggle the display of the frame numbers
						if c == LOWERCASE_F:
							suppressFrameText = not suppressFrameText

						# if the escape key was pressed exit the loops
						if c == ESCAPE_KEY:
							keep_playing = False
							break

				# this is not the first or last frame so just display it once
				else:

					# check to see whether to suppress the display of frames per second and the frame number
					if not suppressFrameText:
						frameText = 'FPS: ' + str(framesPerSecond) + ' Frame: ' + sequence
						cv2.putText(dispImage, frameText, TEXT_ORIGIN, cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS)

					# display the frame
					cv2.imshow(movieName, dispImage)

					# delay between frames and check to see if a key was pressed
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
