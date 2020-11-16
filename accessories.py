import exifread
import os
import datetime
import time
import exiftool
import hash
import db
import pymysql
import shutil
import xxhash
import threading
from pathlib import Path



class File:
    def __init__(self, Filename): #, HashValue, creationDate, Size, GPSCoords, Make, Model):
        hashstarttime = time.time()
        self.Filename = Filename
        #self.HashValue = hash.md5sum_chunks(Filename, 65536)
        self.HashValue = hash.xxhash_chunks(Filename, 65536)
        self.HashTime = time.time() - hashstarttime
        self.creationDate = GetFileDate(Filename)
        self.Size = os.stat(Filename).st_size
        self.GPSCoords = GetGPS(Filename)
        self.Make = GetCameraMake(Filename)
        self.Model = GetCameraModel(Filename)
        
        
    def WriteFiletoDB(self, mydb):
        Test = time.time()
        # mydb = pymysql.connect(
        #       host="localhost",
        #         user="photosynk",
        #           passwd="password",
        #           database="photosynk"
        #           )
        cursor = mydb.cursor()
        fullpath, filename = os.path.split(self.Filename)
        Date = ("%s:%s:%s %s:%s:%s" % (self.creationDate[0], self.creationDate[1], self.creationDate[2], self.creationDate[3], self.creationDate[4], self.creationDate[5]))
        sql = "INSERT INTO Files (DateTime, Make, Model, GPSCoords, Hash, FileName) Values (%s, %s, %s, %s, %s, %s)"
        val = (Date, str(self.Make), str(self.Model), str(self.GPSCoords), str(self.HashValue.hexdigest()), str(filename))
        cursor.execute(sql, val)
        mydb.commit()
        #mydb.close()
        #print("WriteFiletoDB %s : %s" % (filename, time.time() - Test))
    
    def AllreadyInDB(self, mydb):
        Test = time.time()
        # mydb = pymysql.connect(
        #       host="localhost",
        #         user="photosynk",
        #           passwd="password",
        #           database="photosynk"
        #           )
        cursor = mydb.cursor()
        fullpath, filename = os.path.split(self.Filename)
        Date = ("%s:%s:%s %s:%s:%s" % (self.creationDate[0], self.creationDate[1], self.creationDate[2], self.creationDate[3], self.creationDate[4], self.creationDate[5]))
        sql_select_query = "SELECT * FROM Files WHERE DateTime = %s AND Make = %s AND Model = %s AND GPSCoords = %s AND Hash = %s AND FileName = %s"
        val = (Date, str(self.Make), str(self.Model), str(self.GPSCoords), str(self.HashValue.hexdigest()), str(filename))
        cursor.execute(sql_select_query, val)
        cursor.fetchall()
        if cursor.rowcount > 0:
            #print("AllreadyInDB %s : %s" % (filename, time.time() - Test))
            #mydb.close()
            return True
        else:
            #print("AllreadyInDB %s : %s" % (filename, time.time() - Test))
            #mydb.close()
            return False
            
    
    def WriteErrorToDB(self, error, mydb):
        Test = time.time()
        # mydb = pymysql.connect(
        #       host="localhost",
        #         user="photosynk",
        #           passwd="password",
        #           database="photosynk"
        #           )
        cursor = mydb.cursor()
        error = "Already in database."
        Date = ("%s:%s:%s %s:%s:%s" % (self.creationDate[0], self.creationDate[1], self.creationDate[2], self.creationDate[3], self.creationDate[4], self.creationDate[5]))
        sql = "INSERT INTO Errors (DateTime, Make, Model, GPSCoords, Hash, FileName, Error) Values (%s, %s, %s, %s, %s, %s, %s)"
        val = (Date, str(self.Make), str(self.Model), str(self.GPSCoords), str(self.HashValue.hexdigest()), str(self.Filename), str(error))
        cursor.execute(sql, val)
        mydb.commit()
        #mydb.close()
        #print("WriteErrorToDB %s : %s" % (self.Filename, time.time() - Test))
            
            
    def CopyTo(self, Destination):
        copy_time = time.time()
        error = "none"
        fullpath, filename = os.path.split(self.Filename)
        success = False
        if not os.path.exists(os.path.join(Destination,filename)):
            try:
                shutil.copy2(self.Filename, Destination)
                success = True
            except IOError as e:
                error = e
        else:
            success = False
            error = "Destination file allready exists."
        CopyElapsedTime = time.time() - copy_time
        return success, error, CopyElapsedTime


def IsIgnoredFile(filename):
        fullpath, filename = os.path.split(filename)
        file = Path(filename)
        if filename in IgnoredFiles():
            return True
        if file.suffix in IgnoredExtensions():
            return True
        return False
  
  
def IgnoredFiles():
    return ["thumbs.db", "Thumbs.db", ".DS_Store", "*.ini", ".dropbox", "desktop.ini"]
    
    
def IgnoredExtensions():
    return [".ini", ".dat", ".txt", ".xml", ".exe", ".py", ".bat", ".iso", ".rar", ".zip", ".rtf", ".mds", ".ffs_batch", ".lnk", ".pdf", ".ithmb", ".z", ".zDestination", ".m3gDestination", ".banim", ".ddsDestination", ".mp3", ".mpc"]
    
    
def GetCameraMake(source):
    try:
        et = exiftool.ExifTool()
        et.start()
        metadata = et.get_tag("Make", source)
        if metadata is None:
            metadata = "Other"
        et.terminate()
    except:
        metadata = "Other"
    return metadata
        

def GetCameraModel(source):
    try:
        et = exiftool.ExifTool()
        et.start()
        metadata = et.get_tag("QuickTime:ContentDistributor", source)
        if metadata is None:
            metadata = et.get_tag("Model", source)
        if metadata is None:
            metadata = et.get_tag("Camera Model Name", source)
        if metadata is None:
            metadata = "Other"
        et.terminate()
    except:
        metadata = "Other"
    return metadata


def GetCoords(source):
    try:
        et = exiftool.ExifTool()
        et.start()
        metadata = et.get_tag("GPS Position", source)
        #print(metadata)
        if metadata is None:
            metadata = "Other"
        et.terminate()
    except:
        metadata = "Other"
    return metadata


def GetGPS(file):
    Lat = GetExifTagData(file,"GPS GPSLatitude")
    LatRef = GetExifTagData(file,"GPS GPSLatitudeRef")
    Lon = GetExifTagData(file,"GPS GPSLongitude")
    LonRef = GetExifTagData(file,"GPS GPSLongitudeRef") 
    #print(file)
    #print(Lat)
    #print(">%s<" % LatRef)
    #print(Lon)
    #print(">%s<" % LonRef)
    if (Lat != "N/A" and LatRef != "N/A" and Lon != "N/A" and LonRef != "N/A") and not (LatRef != "" or LonRef != ""):
        LatSplit = str(Lat).split(',')
        LatRefSplit = str(LatRef)
        LonSplit = str(Lon).split(',')
        LonRefSplit = str(LonRef)
        LatMin = LatSplit[2].strip(']').strip().split('/')
        LonMin = LonSplit[2].strip(']').strip().split('/')
        if LatSplit[2].strip(']').strip().find("/") > -1:
            LatMinCalc = int(LatMin[0]) / int(LatMin[1])
        else:
            LatMinCalc = int(LatMin[0])
        if LonSplit[2].strip(']').strip().find("/") > -1:
            LonMinCalc = int(LonMin[0]) / int(LonMin[1])
        else:
            LonMinCalc = int(LonMin[0])
        Coord = "%s° %s' %s\" %s, %s° %s' %s\" %s" % (LatSplit[0].strip('['), LatSplit[1].strip(), LatMinCalc, LatRef, LonSplit[0].strip('['), LonSplit[1].strip(), LonMinCalc, LonRef)
        return Coord
    else:
        return "N/A"

    
def GetExifTagData(file,TagName):
    f = open(file, 'rb')
    try:
        tags = exifread.process_file(f)
    except:
        return "N/A"
    TagValue = "N/A"
    for tag in tags.keys():
        #print(tag)
        if tag in (TagName):
            TagValue = tags[tag]
            #print("%s = >%s<" % (tag, tags[tag]))
            return TagValue
    return "N/A"


def GetFileDate(file):
    try:
        Date = str(GetExifTagData(file,'EXIF DateTimeOriginal'))
        if Date == "N/A" or Date == "0000:00:00 00:00:00" or Date == "" or Date == "    :  :     :  :  ":
            Date = str(GetExifTagData(file,'EXIF DateTimeDigitized'))
        if Date == "N/A":
            Date = str(GetExifTagData(file,'Date/Time Original'))
        if Date == "N/A" or Date == "0000:00:00 00:00:00" or Date == "":
            created = os.path.getmtime(file)
            Date = str(datetime.datetime.fromtimestamp(created))
        year=Date[0:4]
        month=Date[5:7]
        day=Date[8:10]
        hour=Date[11:13]
        minute=Date[14:16]
        second=Date[17:19]
    except:
        year = datetime.date.today().year
        month = datetime.date.today().month
        day = datetime.date.today().day
        hour = datetime.date.today().hour
        minute = datetime.date.today().minute
        second = datetime.date.today().second
    return year, month, day, hour, minute, second

    
def CreateDestionation(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except OSError:
            return False
    else:
        return True


def WriteFiletoDB(file):
    mydb = pymysql.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
    cursor = mydb.cursor()
    fullpath, filename = os.path.split(file.Filename)
    sql = "INSERT INTO Files (DateTime, Make, Model, GPSCoords, Hash, FileName) Values (%s, %s, %s, %s, %s, %s)"
    val = (str(file.creationDate), str(file.Make), str(file.Model), str(file.GPSCoords), str(file.HashValue.hexdigest()), str(filename))
    cursor.execute(sql, val)
    mydb.commit()    
