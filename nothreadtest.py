import time
import os
import hash
import time
import datetime
import accessories

begin = time.time()

def filehash(file):
    #file = os.path.join(path,filename)
    print("Hashing %s" % file)
    FileHash = hash.md5sum_full(file)
    FileHash.hexdigest()
    print("Finished %s" % file)

start_path = "/mnt/source/Dubai 2011"
FilesCount = 0

p1 = accessories.person("Antonio", 41)
p1.myfunc()


# Load up a queue with your data. This will handle locking

print("Scanning files...")
for path,dirs,files in os.walk(start_path):
    for filename in files:
        if filename[0] != ".":
            FilesCount = FilesCount + 1
            file = os.path.join(path,filename)
            filehash(file)
print("Finished scanning...")

    
finished = time.time() - begin
print("Total time : %s" % round(finished,2))