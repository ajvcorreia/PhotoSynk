import exifread

def GetExifTagData(file,TagName):
    f = open(file, 'rb')
    tags = exifread.process_file(f)
    CameraModel = "N/A"
    for tag in tags.keys():
        if tag in (TagName):
            CameraModel = tags[tag]
            return CameraModel
