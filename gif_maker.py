#!/usr/bin/python3

import sys
import getopt
import os
from PIL import Image


def create_gif():
    path = os.path.abspath(input_directory)
    files = []
    images = []

    extensions = ['.png', '.bmp', '.jpg', '.jpeg']

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if any(x in file for x in extensions):
                files.append(file)

    # Sort images by name, in ascending order
    files.sort(key=lambda x: int(x.split('.')[0]))

    for file in files:
        file = os.path.join(path, file)
        images.append(Image.open(file))

    images[0].save(output_file, save_all=True, append_images=images[1:], optimize=False,
                   duration=frame_time, loop=0)

    print(f'{output_file} was successfully created!')
    print(f'Directory:{os.path.abspath(output_file)}')


def help_me():
    print('--------------------------------------------')
    print(f'{os.path.basename(__file__)} -i <input_directory> -o <output_file.gif> -f <frame_time_in_milliseconds>')
    print()
    print(f'Defaults and Example:\n   > python3 {os.path.basename(__file__)} -i inputs -o test.gif -f 200')
    print()
    print(f"Supported image file types: {['.png', '.bmp', '.jpg', '.jpeg']}")
    print('--------------------------------------------')
    sys.exit(2)


if __name__ == '__main__':
    input_directory = 'inputs'
    output_file = 'test.gif'
    frame_time = 200

    opts, args = getopt.getopt(sys.argv[1:], "hi:o:f:")
    for opt, arg in opts:
        if opt == '-h':
            help_me()
        elif opt == "-i":
            input_dir = arg
        elif opt == "-o":
            output_file = arg + '.gif' if '.gif' not in arg else ''
        elif opt == '-f':
            frame_time = int(arg)

    if os.path.exists(input_directory):
        create_gif()
    else:
        help_me()
