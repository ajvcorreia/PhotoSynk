import tkinter as tk
import random

root = tk.Tk()
root.title("WOW")
# width x height + x_offset + y_offset:
root.geometry("480x320+0+0")

l = tk.Label(root, text="PhotoSynk Version 0.01", fg='Black', bg='Blue',  font=("Helvetica", 24))
l.place(x = 240, y = 30, width=120, height=25)

l= tk.Button(root, text="Quit")
l.place(x = 250, y = 270, width=120, height=50)

root.mainloop()
