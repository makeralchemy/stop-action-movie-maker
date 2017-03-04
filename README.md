# stop-action-movie-maker

## Overview

The stop action movie recorder and player are two command line python scripts for creating stop action movies.  As the name implies, *stop-action-recorder.py* is used to record the movie and *stop-action-player.py* is used to play the movie.

***stop-action-recorder.py*** uses the specified webcam to record the movie. Upon start up, the program will capture an frame and display a live view of what is visible on the webcam. When the SPACE key is pressed, the frame will be saved.  That image will be shown as a faint image behind the live image for reference as the next frame is being prepared.

These keys have the following functions:

<kbd>Space</kbd> Saves a frame

<kbd>G</kbd> or <kbd>g</kbd> Toggles the display of the grid from on to off or visa versa

<kbd>ESC</kbd> Exits the program.

The frames are stored as *.png* files with names in the form of *filename.nnn.png* where *filename* is the name provided to the command and *nnn* is the number of the frame.  For example: *testmovie.002.png*.

An additional file named *filename.count* containing the number of frames in the movie is also created.  For example: *testmovie.count*. This file is used by *stop-action-player.py* to play the movie.

The *frame* and *.count* files are stored in the current directory.

***stop-action-player.py*** uses the files created by *stop-action-recorder.py* to play back the movie. The movie will be played until the <kbd>ESC</kbd> key is pressed. The time between frames can be specified on the command line; the default is 0.1 seconds.

When the movie is played, the frame numbers and frames per second (fps) are displayed in the upper left corner of the screen. The display of the frame numbers and fps  can be suppressed using the *-s* or *--suspressframetext* options on the command line. The frame numbers and fps can be toggled on and off by pressing the <kbd>f</kbd> key while the movie is playing.

***mpeg-maker.py*** uses the files created by *stop-action-recorder.py* to create a .mp4 video.

The stop action movie recorder, player, and mpeg maker are written for python 2.7.x.

## Usage Instructions

### stop-action-recorder.py

#### Recorder Command Syntax

    $ stop-action-recorder.py -h

    usage: stop-action-recorder.py [-h] [-d] [-g] [-s GRIDSPACING]
                                   [-w WEBCAMNUMBER] [-r] [-a ALPHAVALUE]
                                   moviename

    Stop action movie recorder

    positional arguments:
      moviename             file name of the stop action movie

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

    $ python stop-action-recorder.py testmovie

Record a movie using webcam 1 and store the frames in files with the name *testmovie*.

    $ python stop-action-recorder.py testmovie -w 1

Record a movie using webcam 0, display grid lines and space them 25 pixels apart. Note: display of grid lines can be turned on or off from the keyboard by pressing the <kbd>g</kbd> key.

    $ python stop-action-recorder.py testmovie -g -s 25

Record a movie using webcam 0 and store the frames in files with the name *testmovie*. When displaying the images make the live frames fainter than and the previous frame.

    $ python stop-action-recorder.py testmovie -r

Record a movie using webcam 0 and store the frames in files with the name *testmovie* using an alpha value of 0.50 for the background image.

    $ python stop-action-recorder.py testmovie -a 0.50

Record a movie using webcam 0 and store the frames in files with the name *testmovie*. When displaying the images make the live frames fainter than and the previous frame and an alpha value of 0.50

    $ python stop-action-recorder.py testmovie -r -a 0.50

#### Recorder Messages
If *stop-action-recorder.py* is unable to open the webcam, it will display the message:

    cannot open webcam    

If *stop-action-recorder.py* is unable to capture the initial frame, it will display the following message and exit.

    unable to read initial webcam image

If *stop-action-recorder.py* is unable to capture a subsequent frame, it will display the following message and exit.

    unable to read webcam image in loop

### stop-action-player.py

#### Player Command Syntax

    $ python stop-action-player.py -h

    usage: stop-action-player.py [-h] [-t TIMEDELAY] [-s] [-d] moviename

    Stop action movie player

    positional arguments:
      moviename             file name of the stop action movie

    optional arguments:
      -h, --help            show this help message and exit
      -t TIMEDELAY, --timebetweenframes TIMEDELAY
                            time delay between displaying frames (milliseconds)
      -s, --suppressframenumbers
                            suppress display of frame numbers
      -d, --debug           display debugging messages

    
#### Player Usage Examples
Record a movie using webcam 0 and store the frames in files with the name *testmovie*.

    $ python stop-action-recorder.py testmovie

Record a movie using webcam 1 and store the frames in files with the name *testmovie*.

    $ python stop-action-recorder.py testmovie -w 1

Record a movie using webcam 0, display grid lines and space them 25 pixels apart. Note: display of grid lines can be turned on or off from the keyboard by pressing the <kbd>g</kbd> key.

    $ python stop-action-recorder.py testmovie -g -s 25

Record a movie using webcam 0 and store the frames in files with the name *testmovie*. When displaying the images make the live frames fainter than and the previous frame.

    $ python stop-action-recorder.py testmovie -r

Play a movie named *testmovie* using the default delay between frames of a tenth of a second.

    $ python stop-action-player.py testmovie

Play a movie named *testmovie* with a delay between frames of half a second (500 milliseconds).

    $ python stop-action-player.py testmovie -t 500

Play a movie named *testmovie* and suppress the display of the frame numbers. Note: the display of frame numbers can be toggled on and off by pressing the <kbd>f</kbd> key while the movie is playing.

    $ python stop-action-player.py testmovie -s

#### Player Messages

If *stop-action-player.py* is unable to open the frame count file, it will display a message like the one below and exit:

    can not open frame count file testmovie.count

If *stop-action-player.py* is unable to open one of the frame files, it will display a message like the one below and exit:

    frame file testmovie.001.png does not exist

### mpeg-maker.py

#### mpeg-maker Command Syntax

    $ python mpeg-maker.py -h

    usage: mpeg-maker.py [-h] [-f FPS] inputfile outputfile

    Stop action mpeg movie maker

    positional arguments:
      inputfile          input file name
      outputfile         output file name

    optional arguments:
      -h, --help         show this help message and exit
      -f FPS, --fps FPS  frames per second, default is 2 fps

#### mpeg-maker Usage Examples

Make a .mp4 movie from the *testmovie* frames created by *stop-action-recorder.py*, default two frames per second, and save the resulting movie as *finalmovie.mp4*:

    $ python mpeg-maker.py testmovie finalmovie

Make a .mp4 movie from the *testmovie* frames created by *stop-action-recorder.py*, one frame per second, and save the resulting movie as *finalmovie.mp4*:

    $ python mpeg-maker.py testmovie finalmovie -f 1 

#### mpeg-maker Messages

## Installation Instructions

The *mpeg-maker* python program uses *FFmpeg* to create the mp4 file. Instructions for installing *FFmpeg* can be found [here](https://ffmpeg.org/).

The *stop-action-movie-maker* python programs requires the the OpenCV for Python  library for Python 2 to be installed. Installing OpenCV on MacOS can be tricky, good instructions can be found [here](https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/).

After installing CV2 for your operating system, change to the directory where you want the *stop-action-movie-maker* files to be installed.

Install the *stop-action-movie-maker* files by cloning this repository with this command:

    $ git clone https://github.com/makeralchemy/stop-action-movie-maker

Make your first stop action movie with the command:

    $ python stop-action-recorder.py testmovie

## License
This project is licensed under the MIT license.

