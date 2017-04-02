#! /usr/bin/env python
# make_mpeg.py
""" makes a movie from a set of frames (.png files) """

# written for python 2.7.x

import argparse
import subprocess
import os

DEFAULT_FRAMES_PER_SECOND = 2    # default is 2 frames per specond
BACKWARDS = 'backwards'          # text to use in messages about playback sequence
FORWARDS = 'forwards'            # text to use in messages about playback sequence

def main():
    """
    Main code for this python script
    """

    # setup the command line parser
    parser = argparse.ArgumentParser(description='Stop action mpeg movie maker')
    parser.add_argument('input_file', help='input file name')
    parser.add_argument('output_file', help='output file name')
    parser.add_argument('-f', '--fps', default=DEFAULT_FRAMES_PER_SECOND,
                        type=int, help='frames per second, default is ' + \
                        str(DEFAULT_FRAMES_PER_SECOND) + ' fps')
    parser.add_argument('-s', '--silent', dest='silent_setting',
                        action='store_true',
                        help='if specified, do not display messages')
    parser.add_argument('-b', '--play_backwards', dest='play_backwards',
                        action='store_true',
                        help='create the movie to play backwards')

    # extract the input and output file names
    args = parser.parse_args()
    input_file_name = args.input_file
    output_file_name = args.output_file
    fps = args.fps
    silent = args.silent_setting
    play_backwards = args.play_backwards
    play_setting = BACKWARDS if play_backwards else FORWARDS

    # don't proceed if zero frames per second was specified
    if fps == 0:
        print "frames per second must be greater than zero"

    else:

        # make sure the first input file exists
        if os.path.isfile(input_file_name + '.001.png'):

            # create the input and output file name parameters for ffmpeg
            input_parm = '-i ' + input_file_name + '.%03d.png'
            output_parm = '-y ' + output_file_name + '.mp4'
            fps_parm = '-r ' + str(fps)

            # construct the full ffmpeg command
            if play_backwards:
                ffmpeg_command = ' '.join(['ffmpeg', '-f image2', fps_parm,
                                           input_parm, '-vcodec mpeg4',
                                           '-vf reverse', output_parm])
            else:
                ffmpeg_command = ' '.join(['ffmpeg', '-f image2', fps_parm,
                                           input_parm,
                                           '-vcodec mpeg4', output_parm])

            if not silent:

                # print the settings
                print 'input file is ' + input_file_name
                print 'output file is ' + output_file_name
                print 'movie will be recorded at ' + str(fps) + ' frames per second'
                print 'output movie will play ' + play_setting
                print ''

                # print the command
                print ffmpeg_command
                print ''

            # execute the ffmpeg command
            _ = subprocess.call(ffmpeg_command)

        # the first input file 'file.001.png' does not exist
        else:
            # print an error message
            print 'input file ' + input_file_name + '.001.png does not exist'

if __name__ == "__main__":
    main()
