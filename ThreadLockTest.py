import time
import os
import hash
import queue
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
import threading
import filetype
from datetime import datetime
from pathlib import Path

ProcessedFiles = 0 
thread_count = 8
total_size = 0
CameraModel = ""
source = "/mnt/source2/"
target = "/mnt/target/"
FilesCount = 0
begin = time.time()
job_lock = threading.Lock()

mydb = pymysql.connect(
      host="localhost",
        user="photosynk",
          passwd="password",
          database="photosynk"
          )

# Define a worker function
def worker(file_queue):
    queue_full = True
    while queue_full:
        try:
            # Get your data off the queue, and do some work
            QtimeStart = datetime.now()
            file = file_queue.get(False)
            processfile(file)
            file_queue.task_done()
            Qtime = (datetime.now() - QtimeStart).total_seconds()
            #print ("Qtime %s" % Qtime)
        except queue.Empty:
            queue_full = False


def processfile(pathfile):
    log = open("output.log","a")
    ProcessStart = datetime.now()
    with job_lock:
        global ProcessedFiles 
        LocalProcessedFiles = ProcessedFiles
        LocalProcessedFiles += 1
        ProcessedFiles = LocalProcessedFiles
    file = accessories.File(pathfile)
    with job_lock:
        FileInDB = file.AllreadyInDB(mydb)
    if not FileInDB:
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
            newFileName = Path(file.Filename)
            #print(FileDestination)
            while Path.exists(newFileName):
                #print("before : %s" % newFileName)
                fullpath, filename = os.path.split(newFileName)
                currentfile = Path(filename)
                nameNoSuffix = currentfile.with_suffix('')
                namewithSuffix = str(nameNoSuffix) + "-dup" + currentfile.suffix
                newFileName = os.path.join(FileDestination, namewithSuffix)
                newFileName = Path(newFileName)
                #print("after  : %s" % newFileName)
            success, error, time = file.CopyTo(newFileName)    
            if not success:
                print("%s/%s %s : %s : %s" % (LocalProcessedFiles, FilesCount, threading.current_thread().name, error, file.Filename))
                log.write("%s/%s %s : %s : %s\n" % (LocalProcessedFiles, FilesCount, threading.current_thread().name, error, file.Filename))
                with job_lock:
                    file.WriteErrorToDB(("%s : %s" % (error, file.Filename)), mydb)
            else:
                print("%s/%s %s : %s, %s, %s, %s, %s, %s" % (LocalProcessedFiles, FilesCount, threading.current_thread().name, file.Filename, file.Make, file.Model, round(file.Size/1024/1024,2), round(file.HashTime,2),round((file.Size/1024/1024)/time,2)))
                log.write("%s/%s, %s, %s, %s, %s, %s, %s\n" % (LocalProcessedFiles, FilesCount, file.Filename, file.Make, file.Model, round(file.Size/1024/1024,2), round(file.HashTime,2),round((file.Size/1024/1024)/time,2)))
                with job_lock:
                    file.WriteFiletoDB(mydb)
        else:
            print("Could not create destination %s" % (FileDestination))
            log.write("Could not create destination %s\n" % (FileDestination))
            with job_lock:
                file.WriteErrorToDB(("Could not create destination %s\n" % (FileDestination)), mydb)
    else:
        with job_lock:
            file.WriteErrorToDB(("Allready in database %s" % str(file.Filename)), mydb)
        ProcessingTime = (datetime.now() - ProcessStart).total_seconds()
        print("%s/%s %s : Allready in database %s, %s, %s" % (LocalProcessedFiles, FilesCount, threading.current_thread().name, str(file.Filename), round(file.HashTime,2) , round(ProcessingTime,2)))
        log.write("Allready in database %s\n" % str(file.Filename))
        
    

# Load up a queue with your data. This will handle locking
q = queue.Queue()
print("Scanning files...")
for path,dirs,files in os.walk(source):
    for filename in files:
        import filetype
        if filename[0] != "." and (filetype.is_image(os.path.join(path,filename)) or filetype.is_video(os.path.join(path,filename))):
            FilesCount = FilesCount + 1
            file = os.path.join(path,filename)
            print("%s : %s" % (FilesCount,file))
            q.put(file)
            
print ("%s Files found." % FilesCount)

print("Finished scanning...")
for i in range(thread_count):
    t = threading.Thread(target=worker, args = (q,))
    t.start()
q.join()

mydb.close()
finished = time.time() - begin
print("Total time : %s" % round(finished,2))