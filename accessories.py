import exifread
import os
import datetime
import exiftool


class File:
    def __init__(self, Filename, HashValue, creationDate, Size, GPSCoords, Make, Model):
        self.Filename = Filename
        self.HashValue = HashValue
        self.creationDate = creationDate
        self.Size = Size
        self.GPSCoords = GPSCoords
        self.Make = Make
        self.Model = Model
        
    def GetInfo(self):
        self.GPSCoords = GetCoords(self.filename)
        self.Model = GetCameraModel(self.filename)
        self.Make = GetCameraMake(self.filename)
        self.Size = 
        
        
def GetCameraMake(source):
    et = exiftool.ExifTool()
    et.start()
        metadata = et.get_tag("Make", source)
    if metadata is None:
        metadata = "Other"
    et.terminate()
    return metadata
        

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
            #print("Creating directory : %s" % (path))
        except OSError:
            print ("Creation of the directory %s failed" % path)
        #else:
         #   print ("Successfully created the directory %s" % path)
    #else:
       # print("Directory allready exists : %s" % (path))
        
def IgnoredFiles():
    return ["thumbs.db", "Thumbs.db", ".DS_Store", "*.ini", ".dropbox", "desktop.ini"]


#def FileInDB():
    
#def WriteFiletoDB():
    

#def GetFileData(file):
    #returns boolean
    #get date of file
    #   - from exif
    #   - from file information
    #get 