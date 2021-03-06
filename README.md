# stop-action-movie-maker

## Overview

The stop action movie recorder and player are two command line python scripts for creating stop action movies.  As the name implies, *stop\_action\_recorder.py* is used to record the movie and *stop_action_player.py* is used to play the movie.

***stop\_action\_recorder.py*** uses the specified webcam to record the movie. Upon start up, the program will capture an frame and display a live view of what is visible on the webcam. When the SPACE key is pressed, the frame will be saved.  That image will be shown as a faint image behind the live image for reference as the next frame is being prepared.

These keys have the following functions:

<kbd>Space</kbd> Saves a frame

<kbd>G</kbd> or <kbd>g</kbd> Toggles the display of the grid from on to off or visa versa

<kbd>ESC</kbd> Exits the program.

The frames are stored as *.png* files with names in the form of *filename.nnn.png* where *filename* is the name provided to the command and *nnn* is the number of the frame.  For example: *testmovie.002.png*.

An additional file named *filename.count* containing the number of frames in the movie is also created.  For example: *testmovie.count*. This file is used by *stop\_action\_player.py* to play the movie.

The *frame* and *.count* files are stored in the current directory.

***stop\_action\_player.py*** uses the files created by *stop\_action\_recorder.py* to play back the movie. The movie will be played until the <kbd>ESC</kbd> key is pressed. The time between frames can be specified on the command line; the default is 0.1 seconds.

When the movie is played, the frame numbers and frames per second (fps) are displayed in the upper left corner of the screen. The display of the frame numbers and fps  can be suppressed using the *-s* or *--suspressframetext* options on the command line. The frame numbers and fps can be toggled on and off by pressing the <kbd>f</kbd> key while the movie is playing.

***make\_mpeg.py*** uses the files created by *stop\_action\_recorder.py* to create a .mp4 video.

***delete\_frame\_set.py*** will delete all the files associated with a movie created by *stop\_action\_recorder.py*.

***repeat\_first\_frame.py*** will add extra first frames to the beginning of the movie. This makes the first frame display longer when playing the movie with *stop\_action\_player.py* or when making a mp4 with *make\_mpeg.py*.

***repeat\_last\_frame.py*** will add extra last frames to the end of the movie. This makes the last frame display longer when playing the movie with *stop\_action\_player.py* or when making a mp4 with *make\_mpeg.py*.

The stop action movie recorder, player, and the mpeg maker are written for python 2.7.x.

## Usage Instructions

### stop\_action\_recorder.py

#### Recorder Command Syntax

    $ stop_action_recorder.py -h

    usage: stop_action_recorder.py [-h] [-d] [-g] [-s GRIDSPACING]
                                   [-w WEBCAMNUMBER] [-r] [-a ALPHAVALUE]
                                   movie_name

    Stop action movie recorder

    positional arguments:
      movie_name            file name of the stop action movie

    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           display debugging messages
      -g, --gridlines       display grid lines
      -s GRIDSPACING, --spacing GRIDSPACING
                            grid spacing (pixels)
      -w WEBCAMNUMBER, --webcam WEBCAMNUMBER
                            number of the webcam to use
      -r, --reverseimages   reverses the foreground and background images
      -a ALPHAVALUE, --alpha ALPHAVALUE
                            alpha value for the background image
                            valid values are 0.0 to 1.0
                            default is 0.65


#### Recorder Usage Examples
Record a movie using webcam 0 and store the frames in files with the name *testmovie*.

    $ python stop_action_recorder.py testmovie

Record a movie using webcam 1 and store the frames in files with the name *testmovie*.

    $ python stop_action_recorder.py testmovie -w 1

Record a movie using webcam 0, display grid lines and space them 25 pixels apart. Note: display of grid lines can be turned on or off from the keyboard by pressing the <kbd>g</kbd> key.

    $ python stop_action_recorder.py testmovie -g -s 25

Record a movie using webcam 0 and store the frames in files with the name *testmovie*. When displaying the images make the live frames fainter than and the previous frame.

    $ python stop_action_recorder.py testmovie -r

Record a movie using webcam 0 and store the frames in files with the name *testmovie* using an alpha value of 0.50 for the background image.

    $ python stop_action_recorder.py testmovie -a 0.50

Record a movie using webcam 0 and store the frames in files with the name *testmovie*. When displaying the images make the live frames fainter than and the previous frame and an alpha value of 0.50

    $ python stop_action_recorder.py testmovie -r -a 0.50

#### Recorder Messages
If *stop\_action\_recorder.py* is unable to open the webcam, it will display the message:

    cannot open webcam    

If *stop\_action\_recorder.py* is unable to capture the initial frame, it will display the following message and exit.

    unable to read initial webcam image

If *stop\_action\_recorder.py* is unable to capture a subsequent frame, it will display the following message and exit.

    unable to read webcam image in loop

### stop\_action\_player.py

#### Player Command Syntax

    $ python stop_action_player.py -h

    usage: stop_action_player.py [-h] [-f FRAMESPERSECOND] [-s] [-d] [-b]
                                 [-a FIRSTFRAMEREPEAT] [-z LASTFRAMEREPEAT]
                                 movie_name

    Stop action movie player

    positional arguments:
      movie_name            file name of the stop action movie

    optional arguments:
      -h, --help            show this help message and exit
      -f FRAMESPERSECOND, --FPS FRAMESPERSECOND
                            frames per second
      -s, --suppressframenumbers
                            suppress display of frame numbers
      -d, --debug           display debugging messages
      -b, --playbackwards   play the movie backwards
      -a FIRSTFRAMEREPEAT, --firstframerepeat FIRSTFRAMEREPEAT
                            number of times to repeat the first frame on playback
      -z LASTFRAMEREPEAT, --lastframerepeat LASTFRAMEREPEAT
                            number of times to repeat the last frame on playback

    
#### Player Usage Examples

Play a movie named *testmovie* using the default of tens frames per second.

    $ python stop_action_player.py testmovie

Play a movie named *testmovie* using the default of tens frames per second and play it backwards (frames played in the opposite order that it was recorded).

    $ python stop_action_player.py testmovie -b

Play a movie named *testmovie* using the default of ten frames per second and play frame 001 ten times (this allows the first frame to be visible longer which is good for the beginning or end of the movie if -b is also specified. 

    $ python stop_action_player.py testmovie -a 10

Play a movie named *testmovie* using the default of ten frames per second and play the last frame twenty times (this allows the first frame to be visible longer which is good for the beginning or end of the movie if -b is also specified. 

    $ python stop_action_player.py testmovie -z 20

Play a movie named *testmovie* at 20 frames per second.

    $ python stop_action_player.py testmovie -f 20

Play a movie named *testmovie* and suppress the display of the frame numbers. Note: the display of frame numbers can be toggled on and off by pressing the <kbd>f</kbd> key while the movie is playing.

    $ python stop_action_player.py testmovie -s

#### Player Messages

If *stop\_action\_player.py* is unable to open the frame count file, it will display a message like the one below and exit:

    can not open frame count file testmovie.count

If *stop\_action\_player.py* is unable to open one of the frame files, it will display a message like the one below and exit:

    frame file testmovie.001.png does not exist

If frames per second are specified as a negative number or zero, the following message will be displayed and the program will exit:

    frames per second must be one or higher

If the movie has too few frames, the following message will be displayed and the program will exit:

    movie must contain at least two frames

### make\_mpeg.py

#### make\_mpeg Command Syntax

    $ python make_mpeg.py -h

    usage: make_mpeg.py [-h] [-f FPS] [-s] [-b] input_file output_file

    Stop action mpeg movie maker

    positional arguments:
      input_file           input file name
      output_file          output file name

    optional arguments:
      -h, --help           show this help message and exit
      -f FPS, --fps FPS    frames per second, default is 2 fps
      -s, --silent         if specified, do not display messages
      -b, --playbackwards  create the movie to play backwards

#### make\_mpeg Usage Examples

Make a .mp4 movie from the *testmovie* frames created by *stop\_action\_recorder.py*, default two frames per second, and save the resulting movie as *finalmovie.mp4*:

    $ python make_mpeg.py testmovie finalmovie

Make a .mp4 movie from the *testmovie* frames created by *stop\_action\_recorder.py*, default two frames per second, make it play backwards (frames in the opposite order that they were recorded), and save the resulting movie as *finalmovie.mp4*:

    $ python make_mpeg.py testmovie finalmovie -b

Make a .mp4 movie from the *testmovie* frames created by *stop\_action\_recorder.py*, one frame per second, and save the resulting movie as *finalmovie.mp4*:

    $ python make_mpeg.py testmovie finalmovie -f 1 

#### make\_mpeg Messages

If the number frames per second specified is negative or zero, *make\_mpeg.py* will display a message like the one below and exit:

    frames per second must be greater than zero

If *make\_mpeg.py* is unable to open the first frame file, it will display a message like the one below and exit:

    input file testmovie.001.png does not exist

### delete\_frame\_set.py

#### delete\_frame\_set Command Syntax

    $ python delete_frame_set.py -h

    usage: delete_frame_set.py [-h] [-x] [-d] target_movie_name

    Delete frame set

    positional arguments:
       target_movie_name    name of the stop action movie frame set to delete

    optional arguments:
      -h, --help            show this help message and exit
      -x, --deletewithoutconfirmation
                            delete without asking for confirmation
      -d, --debug           display debugging messages

#### delete\_frame\_set Usage Examples

Delete all of the files associated with a stop action movie created by *stop\_action\_recorder.py* for a movie called *testmovie*.  Note *delete\_frame\_set.py* will not delete any files created by *make\_mpeg*.  *delete\_frame\_set.py* will ask for confirmation to delete the files.

    $ python delete_frame_set.py testmovie

Delete all of the files associated with a stop action movie created by *stop\_action\_recorder.py* for a movie called *testmovie*.  A command argument is used with *delete\_frame\_set.py* to not ask for confirmation to delete the files.  Use the '-x' or '--deletewithoutconfirmation' arguments with caution.

    $ python delete_frame_set.py testmovie -x

#### delete\_frame\_set Messages

*delete\_frame\_set.py* will ask for confirmation to delete the files associated with the movie using a message that looks like this:

    delete frame files for testmovie? Type YES to confirm: 

If any response other than *YES* is typed, the files will not be deleted and the message below will be displayed:

    files will not be deleted 

If *YES* was typed or the *-x* or *--deletewithoutconfirmation* command line arguments were specified, a message like the one below will be displayed after the files have been deleted:

    frame set testmovie deleted 

If the frame count file for the movie is not found, *delete\_frame\_set.py* will display a message like the one below and exit:

    can not open target frame count file testmovie

If a frame file associated with the stop action movie can not be found, a message like the one below will be displayed and the execution will be stopped.  

    testmovie.026.png does not exist


### repeat\_first\_frame.py

#### repeat\_first\_frame Command Syntax

    $ python repeat_first_frame.py -h

    usage: repeat_first_frame.py [-h] [-r FIRSTFRAMEREPEAT] [-d]
                                 input_movie_name output_movie_name

    Create frame set with repeated first frame

    positional arguments:
      input_movie_name      file name of the input stop action movie
      output_movie_name     file name of the output stop action movie

    optional arguments:
      -h, --help            show this help message and exit
      -r FIRSTFRAMEREPEAT, --firstframerepeat FIRSTFRAMEREPEAT
                            number of times to repeat the first frame on playback
      -d, --debug           display debugging messages

#### repeat\_first\_frame Usage Examples

Create a new version of the stop action *testmovie* movie called *newmovie* with the first frame repeated 40 times (at 10 frames per second this would be 4 seconds, at 20 frames per second this we be 2 seconds). 

    $ python repeat_first_frame.py testmovie newmovie -r 40

#### repeat\_first\_frame Messages

If a frame file associated with the stop action movie can not be found, a message like the one below will be displayed and the execution will be stopped.  

    input frame file testmovie does not exist: processing stopping

If the frame count file for the movie is not found, *repeat\_first\_frame.py* will display a message like the one below and exit:

    can not open input frame count file testmovie

If the number of times to repeat the first frame is negative or zero, *repeat\_first\_frame.py* will display the following message and exit:

    first frame repeat must be greater than zero

Each time a frame is copied, a message like the one below will be displayed:

    copying testmovie.012.png to newmovie.032.png

After all the new movie is created, a message like the following will be displayed:

    new frame set newmovie with first frame repeated 20 times successfully created

### repeat\_last\_frame.py

#### repeat\_last\_frame Command Syntax

    $ python repeat_last_frame.py -h

    usage: repeat_last_frame.py [-h] [-r LAST_FRAME_REPEAT] [-d]
                                input_movie_name output_movie_name

    Create frame set with the last frame repeated

    positional arguments:
      input_movie_name      file name of the input stop action movie
      output_movie_name     file name of the output stop action movie

    optional arguments:
      -h, --help            show this help message and exit
      -r LAST_FRAME_REPEAT, --lastframerepeat LAST_FRAME_REPEAT
                            number of times to repeat the last frame
      -d, --debug           display debugging messages

#### repeat\_last\_frame Usage Examples

Create a new version of the stop action *testmovie* movie called *newmovie* with the last frame repeated 40 times (at 10 frames per second this would be 4 seconds, at 20 frames per second this we be 2 seconds). 

    $ python repeat_last_frame.py testmovie newmovie -r 40

#### repeat\_last\_frame Messages

If a frame file associated with the stop action movie can not be found, a message like the one below will be displayed and the execution will be stopped.  

    input frame file testmovie does not exist: processing stopping

If the frame count file for the movie is not found, *repeat\_last\_frame.py* will display a message like the one below and exit:

    can not open input frame count file testmovie

If the number of times to repeat the first frame is negative or zero, *repeat\_last\_frame.py* will display the following message and exit:

    last frame repeat must be greater than zero

Each time a frame is copied, a message like the one below will be displayed:

    copying testmovie.012.png to newmovie.032.png

After all the new movie is created, a message like the following will be displayed:

    new frame set newmovie with last frame repeated 20 times successfully created

## Making a Stop Action Movie

Create a 20 frame per second stop action movie called *testmovie* with the first frame repeated for one second and the last frame repeated for 5 seconds:

Record the movie:

    $ python stop-action-recorder.py testmovie

Preview the movie:

    $ python stop_action_player.py testmovie -t XXX -a 20 -z 100

Create a new temporary movie with the first frame repeated 20 times:

    $ python repeat_first_frame.py testmovie tempmovie1 -r 20

Create a new temporary movie with the last frame repeated 100 times:

    $ python repeat_last_frame.py tempmovie1 tempmovie2 -r 100

Create a MP4 file with the movie:

    $ python make_mpeg.py tempmovie2 testmovie -f 20

Delete the files associated with the two temporary files:

    $ python delete_frame_set.py tempmovie1
    $ python delete_frame_set.py tempmovie2

## Installation Instructions

The *make\_mpeg* python program uses *FFmpeg* to create the mp4 file. Instructions for installing *FFmpeg* can be found [here](https://ffmpeg.org/).

The *stop-action-movie-maker* python programs requires the the OpenCV for Python  library for Python 2 to be installed. Installing OpenCV on MacOS can be tricky, good instructions can be found [here](https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/).

After installing CV2 for your operating system, change to the directory where you want the *stop-action-movie-maker* files to be installed.

Install the *stop-action-movie-maker* files by cloning this repository with this command:

    $ git clone https://github.com/makeralchemy/stop-action-movie-maker

Make your first stop action movie with the command:

    $ python stop_action_recorder.py testmovie

## License
This project is licensed under the MIT license.

