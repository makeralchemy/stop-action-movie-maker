# makes a movie from a set of .png
# written for python 2.7.x

import argparse
import subprocess
import sys
import os

DEFAULT_FRAMES_PER_SECOND = 2    # default is 2 frames per specond
BACKWARDS = 'backwards'     	 # text to use in messages about playback sequence
FORWARDS = 'forwards'			 # text to use in messages about playback sequence

# setup the command line parser
parser = argparse.ArgumentParser(description='Stop action mpeg movie maker')
parser.add_argument('inputfile',  help='input file name')
parser.add_argument('outputfile', help='output file name')
parser.add_argument('-f', '--fps', default=DEFAULT_FRAMES_PER_SECOND, type=int, help='frames per second, default is ' + str(DEFAULT_FRAMES_PER_SECOND) + ' fps')
parser.add_argument('-s', '--silent', dest='silentSetting', action='store_true', help='if specified, do not display messages')
parser.add_argument('-b', '--playbackwards', dest='playBackwards', action='store_true', help='create the movie to play backwards')

# extract the input and output file names
args = parser.parse_args()
inputFileName = args.inputfile
outputFileName = args.outputfile
fps = args.fps
silent = args.silentSetting
playBackwards = args.playBackwards
playSetting = BACKWARDS if playBackwards else FORWARDS

# don't proceed if zero frames per second was specified
if fps == 0:
	print "frames per second must be greater than zero"

else:

	# make sure the first input file exists
	if os.path.isfile(inputFileName + '.001.png'):

		# create the input and output file name parameters for ffmpeg
		inputParm = '-i ' + inputFileName + '.%03d.png'
		outputParm = '-y ' + outputFileName + '.mp4'
		fpsParm = '-r ' + str(fps)

		# construct the full ffmpeg command
		if playBackwards:
			ffmpegCommand = ' '.join(['ffmpeg', '-f image2', fpsParm, inputParm, '-vcodec mpeg4', '-vf reverse', outputParm])
		else:
			ffmpegCommand = ' '.join(['ffmpeg', '-f image2', fpsParm, inputParm, '-vcodec mpeg4',  outputParm])

		if not silent:

			# print the settings
			print 'input file is ' + inputFileName
			print 'output file is ' + outputFileName
			print 'movie will be recorded at ' + str(fps) + ' frames per second'
			print 'output movie will play ' + playSetting
			print ''
			
			# print the command
			print ffmpegCommand
			print ''
	
		# execute the ffmpeg command
		returnCode = subprocess.call(ffmpegCommand)

	# the first input file 'file.001.png' does not exist
	else:
		# print an error message
		print 'input file ' + inputFileName + '.001.png does not exist'