#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from PIL import Image
import piexif
import glob, os, sys
import datetime
import getopt

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:t:", ["help"])
    except getopt.GetoptError as error:
        print(str(error))
        usage()
        sys.exit(2)
    target = None
    timediff = None
    for option, argument in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option == "-f":
            target = argument
        elif option == "-t":
            timediff = int(argument)
        else:
            print("not supported argument {}".format(option))
            usage()
            sys.exit()
    print("Processing {}".format(target))
    im = Image.open(target)
    exif_dict = piexif.load(im.info["exif"])
    #for i in exif_dict:
    if piexif.ImageIFD.DateTime in exif_dict["0th"]:
        #datetime_org = datetime(exif_dict["0th"][piexif.ImageIFD.DateTime])
        #datetime_mod = datetime_org - datetime.timedelta(hours=6)
        print("DateTime is {}".format(exif_dict["0th"][piexif.ImageIFD.DateTime]))
        #print(datetime_mod)
    # metadata = pyexiv2.ImageMetadata(target)
    # metadata.read()
    # #print(metadata.exif_keys)
    # tag = metadata['Exif.Image.DateTime']
    # tag.value = tag.value - datetime.timedelta(hours=6)
    # tag = metadata['Exif.Photo.DateTimeOriginal']
    # tag.value = tag.value - datetime.timedelta(hours=6)
    # tag = metadata['Exif.Photo.DateTimeDigitized']
    # tag.value = tag.value - datetime.timedelta(hours=6)
    # #metadata.write()
    print("Update {}".format(target))

if __name__ == "__main__":
    main()
