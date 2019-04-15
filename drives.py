import tkinter as tk
import subprocess
import psutil

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# create the application
myapp = App()

#
# here are method calls to the window manager class
#
myapp.master.title("My Do-Nothing Application")
myapp.master.maxsize(1000, 400)

myapp.master.hi_there = tk.Button(myapp.master)
myapp.master.hi_there["text"] = "Hello World\n(click me)"

myapp.master.hi_there.pack(side="top")
#self.hi_there.pack(expand=1)


# start the program
myapp.mainloop()
