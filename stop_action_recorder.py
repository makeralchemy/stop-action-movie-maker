""" stop action movie recorder """

# disable pylint too many locals messages
#pylint: disable=R0914

# disable too many nested blocks
#pylint: disable=R0101

# disable too many branches
#pylint: disable=R0912

# disable too many statements
#pylint: disable=R0915

import time
import argparse
import cv2

ESCAPE_KEY = 27
SPACE_BAR = 32
LOWERCASE_C = 99
LOWERCASE_G = 103
UPPERCASE_G = 71
LOWERCASE_S = 115
OUTPUT_FILETYPE = ".png"
DEFAULT_ALPHA = 0.65
GRID_LINE_COLOR = (50, 50, 50)
GRID_LINE_WIDTH = 1
GRID_SPACING = 15
WEBCAM_0 = 0                    # default webcam to use

def debug(program_name, print_debug_messages, display_text):
    """ print debug messages prefixed by the program name """
    if print_debug_messages:
        print program_name + ':', display_text
    return

def main():
    """ main program """

    # parse the command line parameters
    parser = argparse.ArgumentParser(description='Stop action movie recorder')
    parser.add_argument('movie_name', help='file name of the stop action movie')
    parser.add_argument('-d', '--debug', dest='debug_switch',
                        action='store_true', help='display debugging messages')
    parser.add_argument('-g', '--gridlines', dest='gridlines_switch',
                        action='store_true', help='display grid lines')
    parser.add_argument('-s', '--spacing', dest='grid_spacing_pixels',
                        default=GRID_SPACING, type=int,
                        help='grid spacing (pixels)')
    parser.add_argument('-w', '--webcam', dest='webcam_number',
                        default=WEBCAM_0, type=int,
                        help='number of the webcam to use')
    parser.add_argument('-r', '--reverse_images', dest='reverse_images_switch',
                        action='store_true',
                        help='reverses the foreground and background images')
    parser.add_argument('-a', '--alpha', dest='alpha_value',
                        default=DEFAULT_ALPHA, type=float,
                        help='alpha value for the background image; default is ' + \
                        str(DEFAULT_ALPHA))
    args = parser.parse_args()

    # extract the command line parameters
    prog_name = parser.prog.rsplit(".", 1)[0]
    output_file_name = args.movie_name
    print_dm = args.debug_switch
    display_grid = args.gridlines_switch
    reverse_images = args.reverse_images_switch
    webcam_number = args.webcam_number
    grid_spacing_pixels = args.grid_spacing_pixels
    alpha = args.alpha_value

    debug(prog_name, print_dm, 'movie name is ' + output_file_name)
    debug(prog_name, print_dm, 'debug is set to ' + str(print_dm))
    debug(prog_name, print_dm, 'grid display is initially set to ' + \
          str(display_grid))
    debug(prog_name, print_dm, 'reverse images is set to ' + \
        str(reverse_images))
    debug(prog_name, print_dm, 'webcam ' + str(webcam_number) + ' will be used')
    debug(prog_name, print_dm, 'alpha is set to ' + str(alpha))

    # make sure the alpha value is valid
    if (alpha < 0.0) or (alpha > 1.0):
        exit_message = 'alpha value not valid: must be in range of 0.0 to 1.0'
        return exit_message

    file_number = 0     # number of images written to disk

    debug(prog_name, print_dm,
          'opening webcam. file name being used is ' + output_file_name)

    # open the webcam
    cap = cv2.VideoCapture(webcam_number)
    if not cap.isOpened():
        exit_message = 'cannot open webcam'
        return exit_message

    debug(prog_name, print_dm, 'waiting for webcam to open')
    time.sleep(2)  # wait two seconds for webcam to actually open

    # capture the initial image
    successful_capture, prev_image = cap.read()
    debug(prog_name, print_dm, 'captured initial image')
    height, width, channels = prev_image.shape
    debug(prog_name, print_dm, 'height=' + str(height) + ' width=' + \
          str(width) + ' channels=' + str(channels))

    if successful_capture:

        while True:

            # capture a new image
            successful_capture, cur_image = cap.read()

            if successful_capture:

                # make a copy of the current image that will be
                # used for displaying
                disp_image = cur_image.copy()

                # ghost image is the new image
                if reverse_images:
                    # add shadow of previous image to display
                    cv2.addWeighted(prev_image, alpha, disp_image,
                                    1 - alpha, 0, disp_image)

                # ghost image will be the previous image
                else:
                    cv2.addWeighted(disp_image, alpha, prev_image,
                                    1 - alpha, 0, disp_image)

                # display the grid if requested
                if display_grid:
                    for grid_h in range(0, height + 1, grid_spacing_pixels):
                        cv2.line(disp_image, (0, grid_h), (width, grid_h),
                                 GRID_LINE_COLOR, GRID_LINE_WIDTH)
                    for grid_w in range(0, width + 1, grid_spacing_pixels):
                        cv2.line(disp_image, (grid_w, 0), (grid_w, height),
                                 GRID_LINE_COLOR, GRID_LINE_WIDTH)

                # display the current and previous images
                cv2.imshow('disp_image', disp_image)

                # delay a millisecond and check for a pressed key
                char = cv2.waitKey(1)

                # if the space bar is pressed, save the current image
                if char == SPACE_BAR:
                    file_number = file_number + 1
                    file_name = output_file_name + "." + \
                                str(file_number).zfill(3) + \
                                OUTPUT_FILETYPE
                    cv2.imwrite(file_name, cur_image)
                    prev_image = cur_image.copy()
                    debug(prog_name, print_dm, 'image saved as ' + file_name)

                # if 'G' or 'g' is pressed toggle the grid on or off
                if (char == LOWERCASE_G) or (char == UPPERCASE_G):
                    display_grid = not display_grid
                    if display_grid:
                        debug(prog_name, print_dm, 'grid lines are now ON')
                    else:
                        debug(prog_name, print_dm, 'grid lines are now OFF')

                # if 'ESC' is pressed, write the number of images to a file
                # and stop capturing images
                if char == ESCAPE_KEY:
                    if file_number > 0:
                        file_name = output_file_name + ".count"
                        count_file = open(file_name, "w")
                        count_file.write(str(file_number))
                        count_file.close()
                        debug(prog_name, print_dm,
                              'count file written; total count is ' + \
                              str(file_number))
                    exit_message = 'ESC pressed'
                    break

            # error trying to capture an image
            else:
                exit_message = 'unable to read webcam image in loop'
                break

    # error trying to capture the initial image
    else:
        exit_message = 'unable to read initial webcam image'

    # release the camera and close the display windows
    cap.release()
    cv2.destroyAllWindows()

    return exit_message

if __name__ == "__main__":
    print main()
