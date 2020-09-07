import os
import hashlib
import accessories
import exifread

path = '/mnt/Photos'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        files.append(os.path.join(r, file))
        print(file)
        print(hashl.md5sum.chunks(file).hexdigest())
        print(accessories.GetExifTagData(file,'Image Model'))

#for f in files:
#    print(f)
