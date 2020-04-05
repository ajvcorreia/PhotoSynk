from __future__ import print_function
import psutil
import subprocess
import time

for part in psutil.disk_partitions():
    #print("Device: {}, Filesystem: {}, Mount: {}, Size: {}, Disk Used: {}%".format(part[0], part[2], part[1], psutil.disk_usage(part[1])[0], psutil.disk_usage(part[1])[3]))
    MountPoint = part[1]
    Size = psutil.disk_usage(part[1])[0]/1024/1024/1024
    print ("-------------------------------------")
    drive = part[0]
    print ("drive : %s" % drive)

    Command = "udevadm info --query=all --name=%s" % drive
    proc = subprocess.Popen(Command, stdout=subprocess.PIPE, shell=True)
    (executed, err) = proc.communicate()
    wxecuted_status = proc.wait()
    Results=str(executed)

    properties = Results.split("\\n")
    #print(Bus.split("\\n"))
    FileSystem = "N\A"
    BusType = "N\A"
    Serial = "N\A"
    UUID = "N\A"
    SerialShort = "N\A"
    for property in properties:
        #print("1-> %s" % property)
        property = property.split(":")

        if len(property) > 1:
            property = property[1].split("=")

            if len(property) > 1:
                #print("2-> %s" % property[0])
                #print("3-> %s" % property[1])
                if property[0] == " ID_FS_TYPE":
                    FileSystem = property[1]
                if property[0] == " ID_BUS":
                    BusType = property[1]
                if property[0] == " ID_SERIAL":
                    Serial = property[1]
                if property[0] == " ID_FS_UUID":
                    UUID = property[1]
                if property[0] == " ID_SERIAL_SHORT":
                    SerialShort = property[1]



    #               time.sleep(1)
    print ("#######################################")
    print ("drive        : %s" % drive)
    print ("Mount        : %s" % MountPoint)
    print ("Size         : %s" % Size)
    print ("FileSystem   : %s" % FileSystem)
    print ("Bus          : %s" % BusType)
    print ("Serial       : %s" % Serial)
    print ("UUID         : %s" % UUID)
    print ("Serial Short : %s" % SerialShort)
    #print (BusType)
