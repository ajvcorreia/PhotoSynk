#!/usr/bin/python
## get subprocess module
import subprocess
import time
#import psutil
#print psutil.disk_partitions()
## call date command ##

CommandExecution = subprocess.Popen("ls /dev/", stdout=subprocess.PIPE, shell=True)
(output2, err) = CommandExecution.communicate()

CommandExecution_status = CommandExecution.wait()
print ("output2=%s" % output2)
time.sleep(5)
drives = output2.split()
for drive in drives:
    print ("-------------------------------------")
    print ("drive   : %s" % drive)
    Command = "udevadm info --query=all --name=%s | grep DEVTYPE=" % drive
    print ("Command : %s" % Command)
    proc = subprocess.Popen(Command, stdout=subprocess.PIPE, shell=True)

    (DeviceType, err) = proc.communicate()
    DeviceType_status = proc.wait()
    print ("DeviceType=%s" % DeviceType)
    if DeviceType.strip() == "E: DEVTYPE=partition":
        print ("#######################################")
        print ("drive : %s" % drive)
#print "ID_SERIAL : %s" % output1
#print "Command exit status/return code : ", p_status
