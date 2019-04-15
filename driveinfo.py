#!/usr/bin/python
## get subprocess module
import subprocess
#import psutil
#print psutil.disk_partitions()
## call date command ##
#p1 = subprocess.Popen("udevadm info --query=all --name=/dev/sdb | grep ID_SERIAL=", stdout=subprocess.PIPE, shell=True)
CommandExecution = subprocess.Popen("ls /dev/", stdout=subprocess.PIPE, shell=True)
#ls /dev/sd*

#udevadm info --query=all --name=/dev/sdb | grep ID_SERIAL
## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
## or None, if no data should be sent to the child.
#(output1, err) = p1.communicate()
(output2, err) = CommandExecution.communicate()
## Wait for date to terminate. Get return returncode ##

#p1_status = p1.wait()
CommandExecution_status = CommandExecution.wait()
print ("output2=%s" % output2)
drives = output2.split()
for drive in drives:
    print ("drive   : %s" % drive)
    Command = "udevadm info --query=all --name=%s | grep DEVTYPE=" % drive
    print ("Command : %s" % Command)
    proc = subprocess.Popen(Command, stdout=subprocess.PIPE, shell=True)

    (DeviceType, err) = proc.communicate()
    DeviceType_status = proc.wait()
    print ("DeviceType=%s" % DeviceType)
    if DeviceType.strip() == "E: DEVTYPE=partition":
        print ("drive : %s" % drive)
#print "ID_SERIAL : %s" % output1
#print "Command exit status/return code : ", p_status
