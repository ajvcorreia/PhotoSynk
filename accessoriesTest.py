import os
import accessories

source = "/mnt/source/USA 2015/gps"
destination = "/mnt/source/USA 2015/gps2"

file ="/mnt/source/USA 2015/gps/IMG_1909.JPG"
#file ="/mnt/source/USA 2015/gps/IMG_1909.JPG"
#file ="/mnt/target/2006/12/08/CYBERSHOT/DSC08820.JPG"
#fileobj = accessories.File(file)
            
print("-----------------------------------")
#print(accessories.GetFileDate(file))
#print(accessories.GetCameraModel(file))
#print(accessories.GetGPS(file))
#accessories.CreateDestionation("/mnt/source/USA 2015/gps3/1/2/3")
#accessories.CreateDestionation("/mnt/source/USA 2015/gps2/2015/09/08")
#print(os.path.exists("/mnt/source/USA 2015/gps/IMG_1909.JPG"))

for path,dirs,files in os.walk(source):
    for filename in files:
        pathfile = os.path.join(path,filename)
        file = accessories.File(pathfile)
        print(file.HashTime)
        if not file.AllreadyInDB():
            CreationDate = file.creationDate
            FileDestination = os.path.join(destination, CreationDate[0], CreationDate[1], CreationDate[2])
            if accessories.CreateDestionation(FileDestination):
                success, error, time = file.CopyTo(FileDestination)    
                if not success:
                    print(error)
                else:
                    print((file.Size/1024/1024)/time)
                    file.WriteFiletoDB()
            else:
                print("Could not create destination %s" % (FileDestination))
        else:
            print("Allready in database %s" % str(file.Filename))