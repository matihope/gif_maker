#!/usr/bin/python3

import sys
import getopt
import os
from PIL import Image


def get_args(argv):
    input_dir = ''
    output_file = ''
    frame_time = 1000

    opts, args = getopt.getopt(argv, "hi:o:f:")

    for opt, arg in opts:
        if opt == '-h':
            print(f'{os.path.basename(__file__)} -i <input_directory> -o <output_file>')
            sys.exit()

        elif opt == "-i":
            input_dir = arg
        elif opt == "-o":
            output_file = arg + '.gif' if '.gif' not in arg else ''
        elif opt == '-f':
            frame_time = int(arg)

    return input_dir, output_file, frame_time


def main():
    path = os.path.abspath(input_directory)
    files = []
    images = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if any(x in file for x in ['.png', '.bmp', '.jpg', '.jpeg']):
                files.append(os.path.join(r, file))
    files.sort()

    for file in files:
        images.append(Image.open(file))
    images[0].save(output_file_name, save_all=True, append_images=images[1:], optimize=False,
                   duration=frame_duration, loop=0)

    print(f'{output_file_name} was successfully created!')
    print(f'Directory:{os.path.abspath(output_file_name)}')


if __name__ == '__main__':
    input_directory, output_file_name, frame_duration = get_args(sys.argv[1:])
    if os.path.exists(input_directory):
        main()
    else:
        print(f'{os.path.basename(__file__)} -i <input_directory> -o <output_file>')
        print(f'Example: {os.path.basename(__file__)} -i inputs -o test.gif')
