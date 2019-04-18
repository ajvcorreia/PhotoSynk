import hash
import accessories
import exifread

file = '/media/pi/SD/iPhone_old/2016-09-01 16.53.04.jpg'
print(hash.md5sum.chunks(file).hexdigest())
print(accessories.GetExifTagData(file,'Image Model'))


#GetExifTagInfo(file, 'Image Model')
#print(test("text"))
