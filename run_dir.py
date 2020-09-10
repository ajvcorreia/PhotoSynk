import os
import hashlib
import io
import hash
import psutil
import time
import math
import configparser
import pymysql
import db
import accessories
import shutil
import sys
import time
import datetime
#import pyfastcopy

#Search for Storage device
##Check Free disk space
#Calculate total space used by files to be copied

#Create folder with todays date
#Check following conditions:
#1 - Does a file exist with the same filename?
#2 - Does a file exist with the same creation database
#3 - Does a file exist with the same MD5 hash
#4 - if is a photo Does a file exist with same EXIF data


#Get configuration from ini file
config = configparser.ConfigParser(allow_no_value=True)
config.read('PhotoSynk.ini')
for IgnoredFile in config['IgnoredFiles']:
    print(IgnoredFile)

mydb = pymysql.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
cursor = mydb.cursor()

obj_Disk = psutil.disk_usage('/')
DiskPercentUsed = (obj_Disk.percent)
FreeSpace = (obj_Disk.free)
print(FreeSpace/1024)
#create connection mongo database
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient["CopiedFiles"]
#mycol = mydb["Files"]
#errors = mydb["Errors"]
#Set file count to 0
FileCount = 0
#Set total file size to 0
total_size = 0
PercentageProgress = 0
CameraModel = ""
start_path = "/mnt/temp"
#start_path = "/mnt/Photos/20161023_iPhoneJovita" 
#start_path = "/Users/acorreia/Photos_Test"
DestinatioPath = "/media/pi/SSD1/temp/"
FileHash = ""
FilesCount = 0
begin = time.time()
#Count number of files for progress
print("Counting files to be processed!")
for path,dirs,files in os.walk(start_path):
    for filename in files:
        if filename[0] != ".":
            FilesCount = FilesCount + 1
            print '\r' + "Found : " + str(FilesCount) + " files" , 

print("Found %d files." % (FilesCount))
#print('%d %s cost $%.2f' % (6, 'bananas', 1.74))
        

for path,dirs,files in os.walk(start_path):
    for filename in files:
        Reason = "unknown"
        if filename[0] != ".": #ignore files starting with a '.'
            start_time = time.time()
            #create filename with path
            file = os.path.join(path,filename)
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
            print("Calculating Hash for file : %s" % (file))
            #Calculate MD5 hash of file
            #FileHash = hash.md5sum_chunks(file)
            FileHash = hash.md5sum_whole(file)
            #Check if file exists or is in database already
            sql_select_query = """select * from Files where Hash = %s"""
            cursor.execute(sql_select_query, (FileHash.hexdigest(), ))
            record = cursor.fetchall()
            FilesFoundCount = cursor.rowcount
            #Get FileSize
            FileSize = os.stat(file).st_size
            #Keep runnig total of FileSize
            total_size = total_size + FileSize
            #Keep count of files
            FileCount = FileCount + 1
            #calculate elapsed time for this file
            #get exif info from photo
            CameraModel = accessories.GetExifTagData(file,'Image Model')
            PercentageProgress = (FileCount * 100) / FilesCount
            ElapsedTime = time.time() - start_time
            if FreeSpace > FileSize:
                print("Enough space on destination storage, file should be copied")
            else:
                print("Not enough space on destination storage, file should NOT be copied")
            if FilesFoundCount > 0:
                print("%s File %s allready in database" % (PercentageProgress, file))
                Reason = "File allready in database"
            if os.path.exists(file) and FilesFoundCount == 0:
                #write filename and hash to database
                mydict = { "filename": file, "Hash": FileHash.hexdigest(), "Camera": str(CameraModel), "Created": str(time.ctime(mtime)) }
                #x = mycol.insert_one(mydict)
                #print results to default output
                #shutil.copy2 (file, DestinatioPath+filename)
                sql = "INSERT INTO Files (Camera, Hash, FileName) VALUES (%s, %s, %s)"
                val = (str(CameraModel), FileHash.hexdigest(), file)
                cursor.execute(sql, val)
                mydb.commit()
                print("%s, %s, %s, %s, %s, %s, %sMB, %s, %s" % (PercentageProgress, FileCount, FilesCount, file, CameraModel, FileHash.hexdigest(), FileSize/1024/1024, round(ElapsedTime,2), time.ctime(mtime)))
                source = file
                destination = DestinatioPath
                print("copy %s to %s" % (source, destination))
                ExifDate = accessories.GetExifTagData(file,'EXIF DateTimeOriginal')
                FileDate = accessories.GetFileDate(source)
                print("ExifDate %s FileDate %s" % (ExifDate, FileDate))
                #shutil.copy2()
            else:
                #Error occured, file does not seem to exist
                #Write error filename to database
                mydict = { "filename": file, "Hash": FileHash.hexdigest(), "Camera": str(CameraModel), "Created": str(time.ctime(mtime)), "Error": Reason }
                sql = "INSERT INTO Errors (Camera, Hash, FileName, Error) VALUES (%s, %s, %s, %s)"
                val = (str(CameraModel), FileHash.hexdigest(), file, Reason)
                cursor.execute(sql, val)
                mydb.commit()
                #x = errors.insert_one(mydict)
                #print("could not open :", file)
finished = time.time() - begin
print("Total time : %s" % round(finished,2))
print("Total %sMB" % (total_size/1024/1024))
#for x in mycol.find():
#  print(x)
