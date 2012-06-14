#!/usr/bin/python

"""Usage: importphotos.py [-h --help] [-c --copy] [-s --src_dir DIR] [-d --dest_dir DIR]

Move or optionally copy and rename photos from the source directory to the
destination directory renaming to YYYY-MM-DD HH.NN.SS.jpg in a directory
for the month that it was taken in the format YYYY-MM.

Options:
-h --help           Show this help message
-c --copy           Copy files instead of moving them
-s --src_dir DIR    Directory containing the photos to import [default: ./]
-d --dest_dir DIR   Directory under which the files will be imported [default: ./]

"""

from docopt import docopt
from PIL.ExifTags import TAGS
from PIL import Image
import os
import re
import shutil


def import_photos(copy_files, src_dir, dest_dir):

    tag_lookup = dict((value, key) for key, value in TAGS.iteritems())

    for root, dirs, files in os.walk(src_dir):
        for name in files:
            file_parts = os.path.splitext(name)
            ext = file_parts[1].lower()
            file_path = os.path.join(root, name)
            if ext in ['.jpg', '.jpeg']:
                creation_datetime = 0
                try:
                    img = Image.open(file_path)
                    info = img._getexif()
                    creation_datetime = info[tag_lookup['DateTimeOriginal']]
                except (IOError, TypeError, KeyError, AttributeError):
                    print('Could not determine creation date for: %s' % file_path)
                    continue
                parts = re.split('[: ]', creation_datetime)
                folder = '%s-%s' % (parts[0], parts[1])
                file_name = '%s %s%s' % ('-'.join(parts[:3]), '.'.join(parts[3:]), ext)
                folder_path = os.path.realpath(os.path.join(dest_dir, folder))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                output_path = os.path.join(dest_dir, folder, file_name)
                if os.path.exists(output_path):
                    print('Possible duplicate: %s' % output_path)
                else:
                    if copy_files:
                        shutil.copy(file_path, output_path)
                        pass
                    else:
                        pass
                        shutil.move(file_path, output_path)
                    print('%s and renaming %s to %s' % (('Copying' if copy_files else 'Moving'), file_path, output_path))
            else:
                pass
                # print 'Unknown file type: %s' % file_path, ext

if __name__ == '__main__':

    options, arguments = docopt(__doc__)

    src_dir = options.src_dir
    if not os.path.exists(src_dir):
        print('The source path (src_dir: %s) does not exist' % src_dir)
        exit(1)

    dest_dir = options.dest_dir
    if not os.path.exists(dest_dir):
        print('The destination path (dest_dir: %s) does not exist' % dest_dir)
        exit(1)

    import_photos(options.copy, src_dir, dest_dir)
