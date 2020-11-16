import time
import os
import hash
import time
import math
import datetime
import accessories

begin = time.time()
source = "/mnt/source/USA 2015/gps"
destination = "/mnt/source/USA 2015/gps2"

FilesCount = 0
print("Scanning files...")
for path,dirs,files in os.walk(start_path):
    for filename in files:
        if filename[0] != ".":
            FilesCount = FilesCount + 1
            file = os.path.join(path,filename)
            file = accessories.File(file)
            speed = file.Size / 1024 / 1024
            speed = round(speed / file.HashTime, 2)
            print("%s %s %s %s %s %s %s %s %s %s %s" % (FilesCount, file.Make, file.Model, file.GPSCoords, round(file.Size/1024/1024,2), file.creationDate, filename, file.HashValue.hexdigest(), round(file.HashTime,2), speed, str(file.AllreadyInDB())))
            file.WriteFiletoDB()
print("Finished scanning...")
finished = time.time() - begin
print("Total time : %s" % round(finished,2))
