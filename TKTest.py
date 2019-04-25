import tkinter as tk
import random

root = tk.Tk()
root.title("WOW")
# width x height + x_offset + y_offset:
root.geometry("480x320+0+0")

languages = ['Python','Perl','C++','Java','Tcl/Tk']
labels = range(5)
for i in range(5):
   ct = [random.randrange(256) for x in range(3)]
   brightness = int(round(0.299*ct[0] + 0.587*ct[1] + 0.114*ct[2]))
   ct_hex = "%02x%02x%02x" % tuple(ct)
   bg_colour = '#' + "".join(ct_hex)
   l = tk.Label(root,
                text=languages[i],
                fg='White' if brightness < 120 else 'Black',
                bg=bg_colour)
   l.place(x = 20, y = 30 + i*30, width=120, height=25)

l = tk.Label(root,
            text="Synk",
            fg='White' if brightness < 120 else 'Black',
            bg='Blue')
l.place(x = 240, y = 30, width=120, height=25)

l= tk.Button(root, text="Quit")
l.place(x = 250, y = 270, width=120, height=50)

root.mainloop()
