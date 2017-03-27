#!/usr/bin/env python
"""
deletes the frame files associated with a stop action movie
"""

import argparse
import os

FILE_TYPE = '.png'          # images will be saved as .png files
COUNT_TYPE = '.count'       # file type for the file containing the image count
READ_ONLY = 'r'             # open files in read only mode

SUCCESS_CODE = 0            # successful processing
CMD_ERROR_CODE = 1          # error with command parameters
DFS_ERROR_CODE = 2          # error occurred in delete_frame_set

def debug(program_name, print_msgs, display_text):
    """
    print debug messages prefixed by the program name
    """
    if print_msgs:
        print program_name + ':', display_text
    return

def delete_frame_set(target_movie_name, prog_name, print_dm):
    """
    delete all the frame files for the specified movie
    """

    # construct the file name for input file containing the count
    # of images in the movie
    target_count_file_name = target_movie_name + COUNT_TYPE
    debug(prog_name, print_dm, 'target count file name is ' + \
          target_count_file_name)

    # verify the frame count file exists before trying to open it
    if os.path.isfile(target_count_file_name):
        tcf = open(target_count_file_name, READ_ONLY)

        # read the number of frames in the moview
        tcf_count = int(tcf.read())
        debug(prog_name, print_dm, 'target frame count is ' + str(tcf_count))

        # close the frame count file
        tcf.close()

        # loop through the input files and create new output files with the
        # first frame repeat the number of time specified

        target_frame_play_sequence = range(1, tcf_count + 1, 1)

        # loop through all the image files
        for i in target_frame_play_sequence:
            # construct the image number used in the file name
            target_frame_sequence_num = str(i).zfill(3)
            target_file_name = target_movie_name + "." + \
                               target_frame_sequence_num + \
                               FILE_TYPE     # construct the file name

            if os.path.isfile(target_file_name):
                debug(prog_name, print_dm, "deleting " + target_file_name)
                os.remove(target_file_name)
            else:
                error_message = target_file_name + ' does not exist'
                return DFS_ERROR_CODE, error_message

    # the frame count file does not exist: print an error message
    else:
        error_message = 'can not open target frame count file ' + \
                        target_count_file_name
        return DFS_ERROR_CODE, error_message

    # delete the target count file

    debug(prog_name, print_dm, "deleting " + target_count_file_name)
    os.remove(target_count_file_name)

    success_message = 'frame set ' + target_movie_name + ' deleted'
    return SUCCESS_CODE, success_message

def main():
    """
    main python program
    """
    # extract the parameters specified on the command line
    parser = argparse.ArgumentParser(description='Delete frame set')
    parser.add_argument('target_movie_name',
                        help='name of the stop action movie frame set to delete')
    parser.add_argument('-x', '--deletewithoutconfirmation',
                        dest='delete_without_confirmation', action='store_true',
                        help='delete without asking for confirmation')
    parser.add_argument('-d', '--debug', dest='debug_switch',
                        action='store_true', help='display debugging messages')
    args = parser.parse_args()

    # remove the .py from the program name for use in debug messages
    prog_name = parser.prog.rsplit(".", 1)[0]
    print_dm = args.debug_switch

    # display the command parameters if debug is turned on
    debug(prog_name, print_dm, 'target movie name is ' + args.target_movie_name)
    debug(prog_name, print_dm, 'delete without confirmation is set to ' + \
                    str(args.delete_without_confirmation))
    debug(prog_name, print_dm, 'debug is set to ' + str(print_dm))

    if args.delete_without_confirmation:
        delete_files = True
    else:
    # ask for confirmation to delete the files
        delete_confirmation = raw_input('delete frame files for ' + \
                                       args.target_movie_name + \
                                       '? Type YES to confirm: ')
        delete_files = delete_confirmation == 'YES'
#        if delete_confirmation == 'YES':
#            delete_files = True
#        else:
#            delete_files = False

    if delete_files:
        _, return_message = delete_frame_set(args.target_movie_name,
                                             prog_name,
                                             print_dm)
        print return_message
    else:
        print "files will not be deleted"

    # sys.exit(return_code)

# command line execution starts here
if __name__ == "__main__":
    main()
