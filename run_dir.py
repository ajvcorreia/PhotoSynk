import os
import hashlib
import io
import hash
import psutil
import pymongo
import time
import exifread
import math
import configparser
import mysql.connector
import db

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
    print IgnoredFile

mydb = mysql.connector.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
mycursor = mydb.cursor()

obj_Disk = psutil.disk_usage('/')
DiskPercentUsed = (obj_Disk.percent)
FreeSpace = (obj_Disk.free)
print FreeSpace
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
start_path = "/mnt/SD"
#start_path = "/Users/acorreia/Photos_Test"
FileHash = ""
FilesCount = 0
begin = time.time()
#Count number of files for progress
for path,dirs,files in os.walk(start_path):
    for filename in files:
        if filename[0] != ".":
            FilesCount = FilesCount + 1

for path,dirs,files in os.walk(start_path):
    for filename in files:
        Reason = "unknown"
        if filename[0] != ".": #ignore files starting with a '.'
            start_time = time.time()
            #create filename with path
            file = os.path.join(path,filename)
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
            #Calculate MD5 hash of file
            FileHash = hash.md5sum_chunks(file)
            #Check if file exists or is in database already
            #myquery = { "Hash": FileHash.hexdigest() }
            #FilesFoundCount = mycol.count(myquery)
            #FilesFound = mycol.find(myquery)
            #Get FileSize



            sql = "SELECT * FROM Files WHERE Hash = '%s'"
            val = (FileHash.hexdigest())
            cursor.execute(sql, val)
            records = cursor.fetchall()
            FilesFoundCount = cursor.rowcount()
            print FilesFoundCount
            sys.exit(0)



            FileSize = os.stat(file).st_size
            #Keep runnig total of FileSize
            total_size = total_size + FileSize
            #Keep count of files
            FileCount = FileCount + 1
            #calculate elapsed time for this file
            #get exif info from photo
            f = open(file, 'rb')
            tags = exifread.process_file(f)
            CameraModel = "N/A"
            for tag in tags.keys():
                if tag in ('Image Model'):
                    CameraModel = tags[tag]
            PercentageProgress = (FileCount * 100) / FilesCount
            ElapsedTime = time.time() - start_time
            if FreeSpace > FileSize:
                print "Enough space on destination storage, file should be copied"
            else:
                print "Not enough space on destination storage, file should NOT be copied"
            #if FilesFoundCount > 0:
            #    print "%s File %s allready in datbase" % (PercentageProgress, file)
            #    Reason = "File allready in database"
            if os.path.exists(file) and FilesFoundCount == 0:
                #write filename and hash to database
                mydict = { "filename": file, "Hash": FileHash.hexdigest(), "Camera": str(CameraModel), "Created": str(time.ctime(mtime)) }
                #x = mycol.insert_one(mydict)
                #print results to default output
                sql = "INSERT INTO Files (Camera, Hash, FileName) VALUES (%s, %s, %s)"
                val = (str(CameraModel), FileHash.hexdigest(), file)
                mycursor.execute(sql, val)
                mydb.commit()
                print "%s, %s, %s, %s, %s, %s, %sMB, %s, %s" % (PercentageProgress, FileCount, FilesCount, file, CameraModel, FileHash.hexdigest(), FileSize/1024/1024, round(ElapsedTime,2), time.ctime(mtime))
            else:
                #Error occured, file does not seem to exist
                #Write error filename to database
                mydict = { "filename": file, "Hash": FileHash.hexdigest(), "Camera": str(CameraModel), "Created": str(time.ctime(mtime)), "Error": Reason }
                sql = "INSERT INTO Files (Camera, Hash, FileName, Error) VALUES (%s, %s, %s, %s)"
                val = (str(CameraModel), FileHash.hexdigest(), file, Reason)
                mycursor.execute(sql, val)
                mydb.commit()
                #x = errors.insert_one(mydict)
                #print("could not open :", file)
finished = time.time() - begin
print "Total time : %s" % round(finished,2)
print "Total %sMB" % (total_size/1024/1024)
#for x in mycol.find():
#  print(x)
