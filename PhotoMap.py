import os
import io
import psutil
import time
import math
import pymysql
import db
import shutil
import sys
import time
import datetime
import exiftool

def GetCoords(source):
    metadata = et.get_tag("GPS Position", source)
    if metadata is None:
        metadata = "Other"
    return metadata

et = exiftool.ExifTool()
et.start()
mydb = pymysql.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
cursor = mydb.cursor()

start_path = "/mnt/source"
FilesCount = 0
FileCount = 0

print("Counting files to be processed!")
for path,dirs,files in os.walk(start_path):
    for filename in files:
        if filename[0] != ".":
            FilesCount = FilesCount + 1
print("Found %d files." % (FilesCount))


for path,dirs,files in os.walk(start_path):
    for filename in files:
        Reason = "unknown"
        if filename[0] != ".": #ignore files starting with a '.'
            file = os.path.join(path,filename)
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
            FileCount = FileCount + 1
            PercentageProgress = (FileCount * 100) / FilesCount
            Camera = GetCoords(file)
            if Camera != "Other":
                print("%s, %s, %s, %s, %s" % (PercentageProgress, FileCount, FilesCount, file, Camera))
            
            
et.terminate()