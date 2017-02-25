# makes a movie from a set of .png
# written for python 2.7.x

import argparse
import subprocess
import sys
import os

DEFAULT_FRAMES_PER_SECOND = 2    # default is 2 frames per specond

# setup the command line parser
parser = argparse.ArgumentParser(description='Stop action mpeg movie maker')
parser.add_argument('inputfile',  help='input file name')
parser.add_argument('outputfile', help='output file name')
parser.add_argument('-f', '--fps', default=DEFAULT_FRAMES_PER_SECOND, type=int, help='frames per second, default is ' + str(DEFAULT_FRAMES_PER_SECOND) + ' fps')

# extract the input and output file names
args = parser.parse_args()
inputFileName = args.inputfile
outputFileName = args.outputfile
fps = args.fps

# don't proceed if zero frames per second was specified

if fps == 0:
	print "frames per second must be greater than zero"

else:

	# make sure the first input file exists

	if os.path.isfile(inputFileName + '.001.png'):

		# create the input and output file name parameters for ffmpeg
		inputParm = ' -i ' + inputFileName + '.%03d.png'
		outputParm = ' -y ' + outputFileName + '.mp4'
		fpsParm = ' -r ' + str(fps)

		# construct the full ffmpeg command

		ffmpegCommand = 'ffmpeg -f image2' + fpsParm + inputParm + ' -vcodec mpeg4' + outputParm

		# ffmpegCommand = 'ffmpeg -f image2 -r 2 ' + inputParm + '-vcodec mpeg4 ' + outputParm 

		# print the command
		print ffmpegCommand
	
		# execute the ffmpeg command
		returnCode = subprocess.call(ffmpegCommand)

	# the first input file 'file.001.png' does not exist
	else:
		# print an error message
		print 'input file ' + inputFileName + '.001.png does not exist'