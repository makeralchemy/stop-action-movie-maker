# creates a new set of frame files and .count file with the first frame repeated the specified number of times

import sys
import time
import argparse
import os
from shutil import copyfile

FILE_TYPE = '.png'			# images will be saved as .png files
COUNT_TYPE = '.count'		# file type for the file containing the image count
LAST_FRAME_REPEAT = 1 		# number of times to repeat the first frame on playback
READ_ONLY = 'r'				# read only parameter for opening files
WRITE_ONLY = 'w'			# write only parameter for creating and overwriting files
FIRST_FRAME = 1				# frame number of first file in the sequence
SUCCESS_CODE = 0			# successful processing
CMD_ERROR_CODE = 1			# error with command parameters
CNF_ERROR_CODE = 2			# error occurred in createNewFrameSet


# print debugging messages prefixed by the name of the program
def debug(programName, displayText):
	if printDebugMessages:
		print programName + ':', displayText
	return

def createNewFrameSet(inputMovieName, outputMovieName, lastFrameRepeat):

	if lastFrameRepeat < 1: 
		return CNF_ERROR_CODE, 'last frame repeat must be greater than zero'
	
	# construct the file name for input file containing the count of images in the movie
	inputCountFileName = inputMovieName + COUNT_TYPE
	debug(progName, 'input count file name is ' + inputCountFileName)

	# verify the frame count file exists before trying to open it
	if os.path.isfile(inputCountFileName):
		icf = open(inputCountFileName, READ_ONLY)
		
		# read the number of frames in the moview
		icfCount = int(icf.read())
		debug(progName, 'frame count is ' + str(icfCount))

		# close the frame count file
		icf.close()

		# loop through the input files and create new output files with the first frame repeat the number of time specified

		inputFramePlaySequence = range(1, icfCount + 1, 1)
		outputFrameSequenceCount = 0

		for i in inputFramePlaySequence:												# loop through all the image files
			inputFrameSequenceNum = str(i).zfill(3)										# construct the image number used in the file name
			inputFileName = inputMovieName + "." + inputFrameSequenceNum + FILE_TYPE	# construct the file name
			
			# verify the frame image file exists before trying to copying it
			if os.path.isfile(inputFileName):

				# if this is the last frame, add new frames				
				if i == inputFramePlaySequence[-1]:						
					for r in range(i, i + lastFrameRepeat + 1):
						outputFrameSequenceCount = r
						outputFrameSequenceNum = str(outputFrameSequenceCount).zfill(3)
						outputFileName = outputMovieName + "." + outputFrameSequenceNum + FILE_TYPE
						debug(progName, 'copying ' + inputFileName + ' to ' + outputFileName)	
						copyfile(inputFileName, outputFileName)			
				else:
					# display the frame
					outputFrameSequenceCount += 1
					outputFrameSequenceNum = str(outputFrameSequenceCount).zfill(3)
					outputFileName = outputMovieName + "." + outputFrameSequenceNum + FILE_TYPE
					debug(progName, 'copying ' + inputFileName + ' to ' + outputFileName)	
					copyfile(inputFileName, outputFileName)

			# the frame file does not exist: print an error and exit
			else:
				errorMessage = 'input frame file ' + inputFileName + ' does not exist: processing stopping'
				return CNF_ERROR_CODE, errorMessage

	# the frame count file does not exist: print an error message
	else:
		errorMessage = 'can not open input frame count file ' + inputFileName
		return CNF_ERROR_CODE, errorMessage

	# write the output count file

	outputCountFileName = outputMovieName + COUNT_TYPE
	debug(progName, 'output count file name is ' + outputCountFileName)

	ocf = open(outputCountFileName, WRITE_ONLY)
	ocf.write(str(outputFrameSequenceCount))
	ocf.close()

	debug(progName, "input .count = " + str(icfCount))
	debug(progName, "output .count = " + str(outputFrameSequenceCount))

	success_message = 'new frame set ' + outputMovieName + ' with last frame repeated ' + str(lastFrameRepeat) + ' times successfully created'
	return SUCCESS_CODE, success_message

##############################################################################################################################################

# command line execution starts here
if __name__ == "__main__":

	# extract the parameters specified on the command line
	parser = argparse.ArgumentParser(description='Create frame set with the last frame repeated')
	parser.add_argument('inputmoviename', help='file name of the input stop action movie')
	parser.add_argument('outputmoviename', help='file name of the output stop action movie')
	parser.add_argument('-r', '--lastframerepeat', dest='lastFrameRepeat', default=LAST_FRAME_REPEAT, type=int, help='number of times to repeat the last frame')
	parser.add_argument('-d', '--debug', dest='debugSwitch', action='store_true', help='display debugging messages')
	args = parser.parse_args()

	# save the values from the command parser
	progName = parser.prog.rsplit( ".", 1 )[ 0 ]		# remove the .py from the program name
	printDebugMessages = args.debugSwitch

	# display the command parameters if debug is turned on
	debug(progName, 'input movie name is ' + args.inputmoviename)
	debug(progName, 'output movie name is ' + args.outputmoviename)
	debug(progName, 'number of times to repeat the last frame is ' + str(args.lastFrameRepeat))
	debug(progName, 'debug is set to ' + str(printDebugMessages))

	# create the new frame set with the last frame repeated 
	returnCode, returnMessage = createNewFrameSet(args.inputmoviename, args.outputmoviename, args.lastFrameRepeat)
	print returnMessage
	
	sys.exit(returnCode)
