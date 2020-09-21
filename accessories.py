import exifread
import os
import datetime
import exiftool

def GetCameraModel(source):
    et = exiftool.ExifTool()
    et.start()
    metadata = et.get_tag("QuickTime:ContentDistributor", source)
    if metadata is None:
        metadata = et.get_tag("Model", source)
    if metadata is None:
        metadata = et.get_tag("Camera Model Name", source)
    if metadata is None:
        metadata = "Other"
    #print("%s" % (metadata))
    et.terminate()
    return metadata

def GetCoords(source):
    et = exiftool.ExifTool()
    et.start()
    metadata = et.get_tag("GPS Position", source)
    if metadata is None:
        metadata = et.get_tag("Model", source)
    if metadata is None:
        metadata = et.get_tag("Camera Model Name", source)
    if metadata is None:
        metadata = "Other"
    print("%s" % (metadata))
    et.terminate()
    return metadata


def GetExifTagData(file,TagName):
    f = open(file, 'rb')
    try:
        tags = exifread.process_file(f)
    except:
        return "N/A"
    TagValue = "N/A"
    for tag in tags.keys():
        if tag in (TagName):
            TagValue = tags[tag]
            return TagValue
    return "N/A"

def GetFileDate(file):
    Date = str(GetExifTagData(file,'EXIF DateTimeOriginal'))
    if Date == "N/A":
        Date = str(GetExifTagData(file,'Date/Time Original'))
    if Date == "N/A" or Date == "0000:00:00 00:00:00" or Date == "":
        created = os.path.getmtime(file)
        Date = str(datetime.datetime.fromtimestamp(created))
    year=Date[0:4]
    month=Date[5:7]
    day=Date[8:10]
    return year, month, day
    
def CreateDestionation(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print("Creating directory : %s" % (path))
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)
    else:
        print("Directory allready exists : %s" % (path))
        