#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pyexiv2
import glob, os, sys
import datetime

print("Processing {}".format(sys.argv[1]))
metadata = pyexiv2.ImageMetadata(sys.argv[1])
metadata.read()
#print(metadata.exif_keys)
tag = metadata['Exif.Image.DateTime']
tag.value = tag.value - datetime.timedelta(hours=6)
tag = metadata['Exif.Photo.DateTimeOriginal']
tag.value = tag.value - datetime.timedelta(hours=6)
tag = metadata['Exif.Photo.DateTimeDigitized']
tag.value = tag.value - datetime.timedelta(hours=6)
metadata.write()
print("Update {}".format(sys.argv[1]))