import time
import os
import hash
import queue
import threading
import time
import datetime

begin = time.time()

def filehash(file):
    #file = os.path.join(path,filename)
    print("Hashing %s" % file)
    FileHash = hash.md5sum_full(file)
    FileHash.hexdigest()
    print("Finished %s" % file)

start_path = "/mnt/source/Dubai 2011"
FilesCount = 0






# Define a worker function
def worker(file_queue):
    queue_full = True
    while queue_full:
        try:
            # Get your data off the queue, and do some work
            file = file_queue.get(False)
            filehash(file)
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

print()
# Create as many threads as you want
thread_count = 4
for i in range(thread_count):
    t = threading.Thread(target=worker, args = (q,))
    t.start()


q.join()
    
    
finished = time.time() - begin
print("Total time : %s" % round(finished,2))