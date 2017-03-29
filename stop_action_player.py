""" plays stop action movies created by stop_action_player """

# disable pylint too many locals messages
#pylint: disable=R0914

# disable too many nested blocks
#pylint: disable=R0101

# disable too many branches
#pylint: disable=R0912

# disable too many statements
#pylint: disable=R0915


import argparse
import os
import cv2

RBG_GREEN = (0, 255, 0)   # green (red, green, blue)
FILE_TYPE = '.png'        # images will be saved as .png files
COUNT_TYPE = '.count'     # file type for the file containing the image count
TEXT_COLOR = RBG_GREEN    # frame number text color
TEXT_THICKNESS = 1        # frame number text thickness
TEXT_ORIGIN = (10, 25)    # location to place frame number text
TEXT_FONT_SCALE = 0.65    # font size for frame number textpress
DEFAULT_FPS = 10          # default frames per second
ESCAPE_KEY = 27           # ASCII value for the ESC key
LOWERCASE_F = 102         # ASCII value for 'f'
READ_ONLY = 'r'           # read only parameter for opening files
BACKWARDS = 'backwards'   # text to use in messages about playback sequence
FORWARDS = 'forwards'     # text to use in messages about playback sequence
FIRST_FRAME_REPEAT = 0    # number of times to repeat the frst frame on playback
LAST_FRAME_REPEAT = 0     # number of times to repeat the last frame on playback

def debug(program_name, print_debug_messages, display_text):
    """ print debugging messages prefixed by the name of the program """
    if print_debug_messages:
        print program_name + ':', display_text
    return

def main():
    """ main program """

    exit_message = 'user pressed ESC'

    # extract the parameters specified on the command line
    parser = argparse.ArgumentParser(description='Stop action movie player')
    parser.add_argument('movie_name', help='file name of the stop action movie')
    parser.add_argument('-f', '--FPS', dest='frames_per_second',
                        default=DEFAULT_FPS,
                        type=int, help='frames per second')
    parser.add_argument('-s', '--suppressframenumbers',
                        dest='suppress_frame_text',
                        action='store_true',
                        help='suppress display of frame numbers')
    parser.add_argument('-d', '--debug', dest='debug_switch',
                        action='store_true',
                        help='display debugging messages')
    parser.add_argument('-b', '--playbackwards', dest='play_backwards',
                        action='store_true', help='play the movie backwards')
    parser.add_argument('-a', '--firstframerepeat', dest='first_frame_repeat',
                        default=FIRST_FRAME_REPEAT, type=int,
                        help='number of times to repeat the first frame on playback')
    parser.add_argument('-z', '--lastframerepeat', dest='last_frame_repeat',
                        default=LAST_FRAME_REPEAT, type=int,
                        help='number of times to repeat the last frame on playback')
    args = parser.parse_args()

    # remove the .py from the program name
    prog_name = parser.prog.rsplit(".", 1)[0]
    movie_name = args.movie_name
    frames_per_second = args.frames_per_second
    print_dm = args.debug_switch
    suppress_frame_text = args.suppress_frame_text
    play_backwards = args.play_backwards
    first_frame_repeat = args.first_frame_repeat
    last_frame_repeat = args.last_frame_repeat

    # check for invalid frames per second setting
    if frames_per_second < 1:
        exit_message = 'frames per second must be one or higher'
        return exit_message

    # determine how to play the movie
    play_setting = BACKWARDS if play_backwards else FORWARDS

    # calculate the delay in millseconds between frames
    time_between_frames = int(1000 / frames_per_second)

    # display the command parameters if debug is turned on
    debug(prog_name, print_dm, 'movie name is ' + movie_name)
    debug(prog_name, print_dm, 'frames per second are ' + \
          str(frames_per_second))
    debug(prog_name, print_dm, 'time delay between frame is ' + \
          str(time_between_frames))
    debug(prog_name, print_dm, 'debug is set to ' + str(print_dm))
    debug(prog_name, print_dm, 'movie will be played ' + play_setting)
    debug(prog_name, print_dm, 'first frame will be repeated ' + \
          str(first_frame_repeat) + ' times')
    debug(prog_name, print_dm, 'last frame will be repeated ' + \
          str(last_frame_repeat) + ' times')

    # construct the file name for file containing the count of images
    # in the movie
    file_name = movie_name + COUNT_TYPE
    debug(prog_name, print_dm, 'count file name is ' + file_name)

    # verify the frame count file exists before trying to open it
    if os.path.isfile(file_name):
        count_file = open(file_name, READ_ONLY)

        # read the number of frames in the moview
        count = int(count_file.read())
        debug(prog_name, print_dm, 'frame count is ' + str(count))

        # make sure the movie has at least two frames
        if count < 2:
            exit_message = 'movie must contain at least two frames'
            return exit_message

        # close the frame count file
        count_file.close()

        # loop reading and displaying all the frames until the
        # ESC key is pressed
        keep_playing = True

        # create the sequence of frames to play
        play_sequence = range(1, count + 1, 1)

        # if play backwards was specified, reverse the play sequence
        if play_backwards:
            play_sequence.reverse()

        debug(prog_name, print_dm, 'frame play sequence: ' + str(play_sequence))

        # get the first frame in the sequence specified by the user
        first_frame = play_sequence[0]
        # get the last frame in the sequence specified by the user
        last_frame = play_sequence[-1]

        debug(prog_name, print_dm, 'first frame is ' + str(first_frame))
        debug(prog_name, print_dm, 'last frame is ' + str(last_frame))

        # play the movie until the user presses the escape key
        while keep_playing:
            # loop through all the image files
            for i in play_sequence:
                # construct the image number used in the file name
                sequence = str(i).zfill(3)
                # construct the file name
                file_name = movie_name + "." + sequence + FILE_TYPE
                debug(prog_name, print_dm, 'displaying ' + file_name)

                # verify the frame image file exists before trying to read it
                if os.path.isfile(file_name):

                    # read the image from the file
                    disp_image = cv2.imread(file_name, 1)

                    # ensure c has a value since some paths do not call waitkey
                    char = 0

                    # if this is the first frame, repeat it according to what
                    # the user specified
                    if i == first_frame:

                        # display the first frame the number of times specified
                        for rep in range(0, first_frame_repeat):

                            debug(prog_name, print_dm, 're-displaying ' + \
                                  file_name + ' ' + str(rep).zfill(3))

                            # make a copy of the image so there's a clean copy
                            # used to add text each iteration
                            disp_temp_image = disp_image.copy()

                            # check to see whether to suppress the display of
                            # frames per second, frame number, and repeat number
                            if not suppress_frame_text:
                                frame_text = 'FPS: ' + str(frames_per_second) + \
                                            ' Frame: ' + sequence + \
                                            ' Repeat: ' + str(rep).zfill(3)
                                cv2.putText(disp_temp_image, frame_text,
                                            TEXT_ORIGIN,
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            TEXT_FONT_SCALE, TEXT_COLOR,
                                            TEXT_THICKNESS)

                            # display the frame
                            cv2.imshow(movie_name, disp_temp_image)

                            # delay between frames and check to see if a
                            # key was pressed
                            char = cv2.waitKey(time_between_frames)

                            # if lower case f is pressed, toggle the display
                            # of the frame numbers
                            if char == LOWERCASE_F:
                                suppress_frame_text = not suppress_frame_text

                            # if the escape key was pressed exit the loops
                            if char == ESCAPE_KEY:
                                keep_playing = False
                                break

                    # if this is the last frame, repeat it according to what
                    # the user specified
                    elif i == last_frame:

                        # display the last frame the number of times specified
                        for rep in range(0, last_frame_repeat):
                            debug(prog_name, print_dm, 're-displaying ' + \
                                  file_name + ' ' + str(rep).zfill(3))

                            # make a copy of the image so there's a clean copy
                            # used to add text each iteration
                            disp_temp_image = disp_image.copy()

                            # check to see whether to suppress the display of
                            # frames per second, frame number, and repeat number
                            if not suppress_frame_text:
                                frame_text = 'FPS: ' + str(frames_per_second) + \
                                             ' Frame: ' + sequence + \
                                             ' Repeat: ' + str(rep).zfill(3)
                                cv2.putText(disp_temp_image, frame_text,
                                            TEXT_ORIGIN,
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            TEXT_FONT_SCALE, TEXT_COLOR,
                                            TEXT_THICKNESS)

                            # display the frame
                            cv2.imshow(movie_name, disp_temp_image)

                            # delay between frames and check to see if a
                            # key was pressed
                            char = cv2.waitKey(time_between_frames)

                            # if lower case f is pressed, toggle the display
                            # of the frame numbers
                            if char == LOWERCASE_F:
                                suppress_frame_text = not suppress_frame_text

                            # if the escape key was pressed exit the loops
                            if char == ESCAPE_KEY:
                                keep_playing = False
                                break

                    # this is not the first or last frame so just display
                    # it once
                    else:

                        # check to see whether to suppress the display of frames
                        # per second and the frame number
                        if not suppress_frame_text:
                            frame_text = 'FPS: ' + str(frames_per_second) + \
                                        ' Frame: ' + sequence
                            cv2.putText(disp_image, frame_text, TEXT_ORIGIN,
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        TEXT_FONT_SCALE, TEXT_COLOR,
                                        TEXT_THICKNESS)

                        # display the frame
                        cv2.imshow(movie_name, disp_image)

                        # delay between frames and check to see if a
                        # key was pressed
                        char = cv2.waitKey(time_between_frames)

                        # if lower case f is pressed, toggle the display
                        # of the frame numbers
                        if char == LOWERCASE_F:
                            suppress_frame_text = not suppress_frame_text

                        # if the escape key was pressed exit the loops
                        if char == ESCAPE_KEY:
                            keep_playing = False
                            break

                # the frame file does not exist: print an error and exit
                else:
                    exit_message = 'frame file ' + file_name + ' does not exist'
                    return exit_message

        # clean everything up and exit
        cv2.destroyAllWindows()

    # the frame count file does not exist: print an error message
    else:
        exit_message = 'can not open frame count file ' + file_name

    return exit_message

# command line execution starts here
if __name__ == "__main__":
    print main()
