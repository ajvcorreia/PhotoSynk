import exifread
import os
import datetime

def GetExifTagData(file,TagName):
    f = open(file, 'rb')
    tags = exifread.process_file(f)
    TagValue = "N/A"
    for tag in tags.keys():
        #print(tag + " = " + str(tags[tag]))
        if tag in (TagName):
            TagValue = tags[tag]
            return TagValue

def GetFileDate(file):
    Date = str(GetExifTagData(file,'EXIF DateTimeOriginal'))
    print "------"
    print(Date)
    if Date == "None":
        created = os.path.getctime(file)
        Date = str(datetime.datetime.fromtimestamp(created))
    print(Date)
    print(Date[0:4])
    print(Date[5:7])
    print(Date[8:10])
    print "^^^^^^^"
    return Date
    