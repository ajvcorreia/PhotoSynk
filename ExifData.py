import io
import exifread


def GetExifTagInfo(filename, exifdata):
    file = str(filename)
    f = open(file, 'rb')
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag == exifdata:
            return tags[tag]
    return ""

#print GetExifTag('/mnt/SD/iPhone_old/2016-09-01 16.53.04.jpg', 'Image Model')
