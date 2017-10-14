#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
from PIL import Image
import piexif
import glob, os, sys
from datetime import datetime, date, timedelta
import getopt
def usage():
    print("{} -f <file> -t <time diff hours>".format(sys.argv[0]))
    print("-h: help")
    print("-f <file>: select the file")
    print("-t <time diff hours>: time diff in hours")
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:t:", ["help"])
    except getopt.GetoptError as error:
        print(str(error))
        usage()
        sys.exit(2)
    target = None
    timediff = 6
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
    if target is None:
        usage()
        sys.exit(-1)
    im = Image.open(target)
    exif_dict = piexif.load(im.info["exif"])
    if piexif.ImageIFD.DateTime in exif_dict["0th"]:
        datetime_org = datetime.strptime(exif_dict["0th"][piexif.ImageIFD.DateTime], '%Y:%m:%d %H:%M:%S')
        datetime_mod = datetime_org - timedelta(hours=timediff)
        if piexif.ExifIFD.UserComment in exif_dict["Exif"] and exif_dict["Exif"][piexif.ExifIFD.UserComment] == "Modified Time":
            print("User comment: {} (keep datetime: {})".format(exif_dict["Exif"][piexif.ExifIFD.UserComment], exif_dict["0th"][piexif.ImageIFD.DateTime]))
            sys.exit(0)
        exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime_mod.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime_mod.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = datetime_mod.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = 'Modified Time'
        exif_bytes = piexif.dump(exif_dict)
        im.save(target, "jpeg", exif=exif_bytes)
        print("{}: DateTime is {} -> {}".format(target, exif_dict["0th"][piexif.ImageIFD.DateTime], datetime_mod))

if __name__ == "__main__":
    main()
