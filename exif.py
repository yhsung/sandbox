#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
from PIL import Image
import piexif
import glob, os, sys
from datetime import datetime, date, timedelta
import getopt
def restore(filename):
    im = Image.open(filename)
    exif_dict = piexif.load(im.info["exif"])
    if piexif.ExifIFD.MakerNote in exif_dict["Exif"] and exif_dict["Exif"][piexif.ExifIFD.UserComment] == 'Modified Time':
        original_time = exif_dict["Exif"][piexif.ExifIFD.MakerNote]
        print("{}: DateTime is {} -> {}".format(filename, exif_dict["0th"][piexif.ImageIFD.DateTime], original_time))
        exif_dict["0th"][piexif.ImageIFD.DateTime] = original_time
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = original_time 
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = original_time
        del exif_dict["Exif"][piexif.ExifIFD.UserComment]
        del exif_dict["Exif"][piexif.ExifIFD.MakerNote]
        exif_bytes = piexif.dump(exif_dict)
        im.save(filename, "jpeg", exif=exif_bytes)
    else:

        print("{}: Datetime: {}".format(filename, exif_dict["0th"][piexif.ImageIFD.DateTime]))
        sys.exit(0)

def modify(filename, timediff):
    im = Image.open(filename)
    exif_dict = piexif.load(im.info["exif"])
    if piexif.ImageIFD.DateTime in exif_dict["0th"]:
        datetime_org = datetime.strptime(exif_dict["0th"][piexif.ImageIFD.DateTime], '%Y:%m:%d %H:%M:%S')
        datetime_mod = datetime_org - timedelta(hours=timediff)
        if piexif.ExifIFD.UserComment in exif_dict["Exif"] and exif_dict["Exif"][piexif.ExifIFD.UserComment] == "Modified Time":
            print("{}: Modified; keep datetime: {}".format(filename, exif_dict["0th"][piexif.ImageIFD.DateTime]))
            sys.exit(0)
        print("{}: DateTime is {} -> {}".format(filename, exif_dict["0th"][piexif.ImageIFD.DateTime], datetime_mod))
        exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime_mod.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime_mod.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = datetime_mod.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = 'Modified Time'
        exif_dict["Exif"][piexif.ExifIFD.MakerNote] = datetime_org.strftime('%Y:%m:%d %H:%M:%S')
        exif_bytes = piexif.dump(exif_dict)
        im.save(filename, "jpeg", exif=exif_bytes)

def usage():
    print("{} -f <file> -t <time diff hours>".format(sys.argv[0]))
    print("-h: help")
    print("-f <file>: select the file")
    print("-t <time diff hours>: time diff in hours")
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrf:t:", ["help"])
    except getopt.GetoptError as error:
        print(str(error))
        usage()
        sys.exit(2)
    filename = None
    timediff = 6
    _restore = False
    for option, argument in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option == "-f":
            filename = argument
        elif option == "-t":
            timediff = int(argument)
        elif option == "-r":
            _restore = True
        else:
            print("not supported argument {}".format(option))
            usage()
            sys.exit()
    if filename is None:
        usage()
        sys.exit(-1)
    if _restore == True:
        restore(filename)
    else:
        modify(filename=filename, timediff=timediff)

if __name__ == "__main__":
    main()
