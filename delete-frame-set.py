# creates a new set of frame files and .count file with the first frame repeated the specified number of times

import sys
import time
import argparse
import os
from shutil import copyfile

FILE_TYPE = '.png'			# images will be saved as .png files
COUNT_TYPE = '.count'		# file type for the file containing the image count
READ_ONLY = 'r'				# open files in read only mode

SUCCESS_CODE = 0			# successful processing
CMD_ERROR_CODE = 1			# error with command parameters
DFS_ERROR_CODE = 2			# error occurred in deleteframeset


# print debugging messages prefixed by the name of the program
def debug(programName, displayText):
	if printDebugMessages:
		print programName + ':', displayText
	return

def deleteFrameSet(targetMovieName):

	# construct the file name for input file containing the count of images in the movie
	targetCountFileName = targetMovieName + COUNT_TYPE
	debug(progName, 'target count file name is ' + targetCountFileName)

	# verify the frame count file exists before trying to open it
	if os.path.isfile(targetCountFileName):
		tcf = open(targetCountFileName, READ_ONLY)
		
		# read the number of frames in the moview
		tcfCount = int(tcf.read())
		debug(progName, 'target frame count is ' + str(tcfCount))

		# close the frame count file
		tcf.close()

		# loop through the input files and create new output files with the first frame repeat the number of time specified

		targetFramePlaySequence = range(1, tcfCount + 1, 1)
		
		for i in targetFramePlaySequence:													# loop through all the image files
			targetFrameSequenceNum = str(i).zfill(3)										# construct the image number used in the file name
			targetFileName = targetMovieName + "." + targetFrameSequenceNum + FILE_TYPE		# construct the file name
			
			if os.path.isfile(targetFileName):
				debug(progName, "deleting " + targetFileName)
				os.remove(targetFileName)
			else:
				errorMessage = targetFileName + ' does not exist'
				return DFS_ERROR_CODE, errorMessage

	# the frame count file does not exist: print an error message
	else:
		errorMessage = 'can not open target frame count file ' + inputFileName
		return DFS_ERROR_CODE, errorMessage

	# delete the target count file

	debug(progName, "deleting " + targetCountFileName)
	os.remove(targetCountFileName)

	successMessage = 'frame set' + targetMovieName + ' deleted'
	return SUCCESS_CODE, successMessage

##############################################################################################################################################

# command line execution starts here
if __name__ == "__main__":

	# extract the parameters specified on the command line
	parser = argparse.ArgumentParser(description='Delete frame set')
	parser.add_argument('targetmoviename', help='file name of the stop action movie frame set to delete')
	parser.add_argument('-x', '--deletewithoutconfirmation', dest='deleteWithoutConfirmation', action='store_true', help='delete without asking for confirmation')
	parser.add_argument('-d', '--debug', dest='debugSwitch', action='store_true', help='display debugging messages')
	args = parser.parse_args()

	# save the values from the command parser
	progName = parser.prog.rsplit( ".", 1 )[ 0 ]		# remove the .py from the program name
	printDebugMessages = args.debugSwitch

	# display the command parameters if debug is turned on
	debug(progName, 'target movie name is ' + args.targetmoviename)
	debug(progName, 'delete without confirmation is set to ' + str(args.deleteWithoutConfirmation))
	debug(progName, 'debug is set to ' + str(printDebugMessages))

	if args.deleteWithoutConfirmation:
		deleteFiles = True
	else:
	# ask for confirmation to delete the files
		deleteConfirmation = raw_input('delete frame files for ' + args.targetmoviename + '? Type YES to confirm: ')
		if deleteConfirmation == 'YES':
			deleteFiles = True
		else:
			deleteFiles = False

	if deleteFiles:
		returnCode, returnMessage = deleteFrameSet(args.targetmoviename)
		print returnMessage
	else:
		print "files will not be deleted"
	
	# sys.exit(returnCode)
