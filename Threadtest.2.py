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
source = "/mnt/source/From i2S/"
target = "/mnt/target/"
FileHash = ""
FilesCount = 0
FilesCount = 0
begin = time.time()

print(FreeSpace/1024)

def processfile(pathfile):
    global total_size
    global FileCount
    global target
    global FilesCount
    global log
    log = open("output.log","a")
    if accessories.IsIgnoredFile(pathfile):
        return
    file = accessories.File(pathfile)
    FileCount += 1
    #print(file.HashTime)
    if not file.AllreadyInDB():
        CreationDate = file.creationDate
        if file.Make == "Other" and file.Model == "Other":
            Camera = "Other"
        elif file.Make == "Other" and file.Model != "Other":
            Camera = file.Model
        elif file.Make != "Other" and file.Model == "Other":
            Camera = file.Make
        elif str(file.Make) in str(file.Model):
            Camera = file.Model
        else:
            Camera = str(file.Make) + " " + str(file.Model)
        FileDestination = os.path.join(target, CreationDate[0], CreationDate[1], CreationDate[2], Camera)
        if accessories.CreateDestionation(FileDestination):
            success, error, time = file.CopyTo(FileDestination)    
            if not success:
                print("%s : %s" % (error, file.Filename))
                log.write("%s : %s" % (error, file.Filename))
                file.WriteErrorToDB("%s : %s" % (error, file.Filename))
            else:
                print("%s/%s, %s, %s, %s, %s, %s, %s" % (FileCount, FilesCount, file.Filename, file.Make, file.Model, round(file.Size/1024/1024,2), round(file.HashTime,2),round((file.Size/1024/1024)/time,2)))
                log.write("%s/%s, %s, %s, %s, %s, %s, %s\n" % (FileCount, FilesCount, file.Filename, file.Make, file.Model, round(file.Size/1024/1024,2), round(file.HashTime,2),round((file.Size/1024/1024)/time,2)))
                file.WriteFiletoDB()
        else:
            print("Could not create destination %s" % (FileDestination))
            log.write("Could not create destination %s\n" % (FileDestination))
            file.WriteErrorToDB("Could not create destination %s\n" % (FileDestination))
    else:
        print("Allready in database %s" % str(file.Filename))
        log.write("Allready in database %s\n" % str(file.Filename))
        file.WriteErrorToDB("Allready in database %s" % str(file.Filename))

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
for path,dirs,files in os.walk(source):
    for filename in files:
        if filename[0] != ".":
            FilesCount = FilesCount + 1
            file = os.path.join(path,filename)
            q.put(file)
print("Finished scanning...")
thread_count = 8
for i in range(thread_count):
    t = threading.Thread(target=worker, args = (q,))
    t.start()
q.join()
finished = time.time() - begin
print("Total time : %s" % round(finished,2))
log.write("Total time : %s" % round(finished,2))