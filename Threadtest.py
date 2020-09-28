import time
import os
import hash
import queue
import threading
import time
import datetime
import hashlib
import io
import psutil
import math
import configparser
import pymysql
import db
import accessories
import shutil
import sys

lock = threading.Lock()
obj_Disk = psutil.disk_usage('/')
DiskPercentUsed = (obj_Disk.percent)
FreeSpace = (obj_Disk.free)
FileCount = 0
total_size = 0
PercentageProgress = 0
CameraModel = ""
start_path = "/mnt/source/20111112_MMM/"
DestinatioPath = "/mnt/target/threadtest/"
FileHash = ""
FilesCount = 0
FilesCount = 0
begin = time.time()

print(FreeSpace/1024)


def filehash(file):
    print("Hashing %s" % file)
    FileHash = hash.md5sum_full(file)
    FileHash.hexdigest()
    print("Finished %s" % file)


def processfile(file):
    global total_size
    global FileCount
    Reason = "unknown"
    mydb = pymysql.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
    cursor = mydb.cursor()
    if file[0] != ".": #ignore files starting with a '.'
        start_time = time.time()
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
        
        starthashtime = time.time()        
        FileHash = hash.md5sum_full(file)
        hashtime = time.time() - starthashtime
        
        sql_select_query = """select * from Files where Hash = %s"""
        startquery1time = time.time()        
        cursor.execute(sql_select_query, (FileHash.hexdigest(), ))
        record = cursor.fetchall()
        FilesFoundCount = cursor.rowcount
        query1time = time.time() - startquery1time
        
        FileSize = os.stat(file).st_size
        total_size += FileSize
        FileCount += 1
        
        startexiftime = time.time()
        CameraModel = accessories.GetExifTagData(file,'Image Model')
        exiftime = time.time() - startexiftime
        
        PercentageProgress = (FileCount * 100) / FilesCount
        #if FreeSpace > FileSize:
        #    #print("Enough space on destination storage, file can be copied")
        #else:
        #    #print("Not enough space on destination storage, file should NOT be copied")
        if FilesFoundCount > 0:
            #print("%s File %s allready in database should not be copied" % (PercentageProgress, file))
            Reason = "File allready in database"
        fullpath, filename = os.path.split("/tmp/d/a.dat")
        if os.path.exists(file) and FilesFoundCount == 0 and filename not in accessories.IgnoredFiles():
            mydict = { "filename": file, "Hash": FileHash.hexdigest(), "Camera": str(CameraModel), "Created": str(time.ctime(mtime)) }
            startquery2time = time.time()
            sql = "INSERT INTO Files (Camera, Hash, FileName) VALUES (%s, %s, %s)"
            val = (str(CameraModel), FileHash.hexdigest(), file)
            cursor.execute(sql, val)
            mydb.commit()
            query2time = time.time() - startquery2time    
            source = file
            Camera = accessories.GetCameraModel(source)
            destination = DestinatioPath
            FileDate = accessories.GetFileDate(source)
            destinationDir = os.path.join(destination, FileDate[0], FileDate[1], FileDate[2], str(Camera))
            accessories.CreateDestionation(destinationDir)
            copy_time = time.time()
            try:
                shutil.copy2(source, destinationDir)
            except shutil.SameFileError: 
                print("Source and destination represents the same file.") 
            except PermissionError: 
                print("Permission denied.") 
            except: 
                print("Error occurred while copying file.") 
            CopyElapsedTime = time.time() - copy_time
            FileSizeMB = FileSize/1024/1024
            CopySpeed = FileSizeMB / CopyElapsedTime
            ElapsedTime = time.time() - start_time
            print("%s, %s, %s, %s, %s, %s, %sMB, %s, %s, %s, %s, %s %s" % (round(PercentageProgress), FileCount, FilesCount, file, CameraModel, FileHash.hexdigest(), round(FileSize/1024/1024,2), round(ElapsedTime,2), round(exiftime,2), round(hashtime,2), round(query1time,2), round(query2time,2), round(CopyElapsedTime,2)))
        else:
            mydict = { "filename": file, "Hash": FileHash.hexdigest(), "Camera": str(CameraModel), "Created": str(time.ctime(mtime)), "Error": Reason }
            sql = "INSERT INTO Errors (Camera, Hash, FileName, Error) VALUES (%s, %s, %s, %s)"
            val = (str(CameraModel), FileHash.hexdigest(), file, Reason)
            cursor.execute(sql, val)
            mydb.commit()


# Define a worker function
def worker(file_queue):
    queue_full = True
    while queue_full:
        try:
            # Get your data off the queue, and do some work
            file = file_queue.get(False)
            processfile(file)
            file_queue.task_done()
        except queue.Empty:
            queue_full = False


# Load up a queue with your data. This will handle locking
q = queue.Queue()
print("Scanning files...")
for path,dirs,files in os.walk(start_path):
    for filename in files:
        if filename[0] != ".":
            FilesCount = FilesCount + 1
            file = os.path.join(path,filename)
            q.put(file)
print("Finished scanning...")
thread_count = 4
for i in range(thread_count):
    t = threading.Thread(target=worker, args = (q,))
    t.start()
q.join()
finished = time.time() - begin
print("Total time : %s" % round(finished,2))