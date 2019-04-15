import subprocess
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.maxsize(480, 320)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        output = subprocess.run("ls /dev/", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        DriveDevices = output.stdout
        drives = DriveDevices.split()
        for drive in drives:
            if drive.find("sd") > -1:
                Command = "udevadm info --query=all --name=%s | grep DEVTYPE=" % drive
                output = subprocess.run(Command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
                DeviceType = output.stdout
                if DeviceType.strip() == "E: DEVTYPE=partition":
                    print ("drive : %s" % drive)
                    self.hi_there = tk.Button(self)
                    self.hi_there["text"] = drive
                    self.hi_there["command"] = self.say_hi()
                    self.hi_there.pack(side="top")
                    #self.hi_there.pack(expand=1)
                    self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
                    self.quit.pack(side="bottom")

    def say_hi(self):
        print("Drive chosen")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
