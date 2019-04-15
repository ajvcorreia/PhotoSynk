import subprocess
import psutil
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.maxsize(480, 320)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        CommandExecution = subprocess.Popen("ls /dev/sd*", stdout=subprocess.PIPE, shell=True)
        (output2, err) = CommandExecution.communicate()
        CommandExecution_status = CommandExecution.wait()

        drives = output2.split()
        for drive in drives:
            Command = "udevadm info --query=all --name=%s | grep DEVTYPE=" % drive
            proc = subprocess.Popen(Command, stdout=subprocess.PIPE, shell=True)
            (DeviceType, err) = proc.communicate()
            DeviceType_status = proc.wait()
            if DeviceType.strip() == "E: DEVTYPE=partition":
                #print ("drive : %s" % drive)
                self.hi_there = tk.Button(self)
                self.hi_there["text"] = drive
                self.hi_there["command"] = self.say_hi
                self.hi_there.pack(side="top")
                #self.hi_there.pack(expand=1)
                self.quit = tk.Button(self, text="QUIT", fg="red",
                                      command=self.master.destroy)
                self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
