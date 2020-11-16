import os
#Scan source directory and delete any 0 byte files
source = "/mnt/source"
deleted = 0 
errors = 0
count = 0 
for path,dirs,files in os.walk(source):
    for filename in files:
        filepath = os.path.join(path, filename)
        size = os.stat(filepath).st_size
        count += 1
        if size == 0:
            try:
                os.remove(filepath)
                print("File deleted      : %s, %s" % (filepath, size))
                deleted += 1
            except Exception as error:
                print ("File not deleted : %s, %s, %s" % (filepath, size, error))
                errors += 1
print ("Deleted : %s" % deleted)
print ("Errors  : %s" % errors)
print ("Total   : %s" % count)