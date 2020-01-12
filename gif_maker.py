#!/usr/bin/python3
# Version 1.1

import sys
import getopt
import os
from PIL import Image


def gen_transparent_frame(path):
    im = Image.open(path)
    alpha = im.getchannel('A')

    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)

    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)

    # The transparency index is 255
    im.info['transparency'] = 255

    return im


def create_gif(transparent):
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
        file_path = os.path.join(path, file)

        if transparent:
            images.append(gen_transparent_frame(file_path))
        else:
            images.append(Image.open(file_path))

    images[0].save(output_file, save_all=True, append_images=images[1:], duration=frame_time,
                   loop=0, optimize=False, disposal=2)

    print(f'{output_file} was successfully created!')
    print(f'Directory:{os.path.abspath(output_file)}')


def help_me():
    print('--------------------------------------------')
    print(f'{os.path.basename(__file__)}:')
    print(f'    -i <input_directory> : The directory with input images (default: {input_directory})')
    print(f'    -o <output_file.gif> : Name of the output file (default: {output_file})')
    print(f'    -f <frame_time> : Frame duration in milliseconds (default: {frame_time})')
    print(f'    -t : Gif will have an alpha channel (default: NO TAG)')
    print()
    print(f'Defaults and Example:\n   > python3 {os.path.basename(__file__)} -i inputs -o test.gif -f 200')
    print()
    print(f"Supported image file types: {['.png', '.bmp', '.jpg', '.jpeg']}")
    print('--------------------------------------------')
    sys.exit(2)


if __name__ == '__main__':
    input_directory = 'inputs'
    output_file = 'animation.gif'
    frame_time = 200
    transparent = False

    opts, args = getopt.getopt(sys.argv[1:], "hi:o:f:t")
    for opt, arg in opts:
        if opt == '-h':
            help_me()
        elif opt == "-i":
            input_dir = arg
        elif opt == "-o":
            output_file = arg + '.gif' if '.gif' not in arg else arg
        elif opt == '-f':
            frame_time = int(arg)
        elif opt == '-t':
            transparent = True

    if os.path.exists(input_directory):
        create_gif(transparent)
    else:
        help_me()
