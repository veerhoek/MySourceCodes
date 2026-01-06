from tkinter import *
from tkinter import messagebox


def do_nothing():
    x = 0


def do_about():
    messagebox.showinfo("oGame", "oGame application\n\nby Jaap on Mac\nDate Aug-2021\nVersion 0.1aaa")


def do_tutorial():
    messagebox.showinfo("oGame",
                        "Objective:\nconnect three sides with colors from the same color\n\n" +
                        "Left click is white disk, right click is black disk\n\n" +
                        "The AI will take the other color and try to beat you\n" +
                        "A 'hint' option is under development\n\n" +
                        "Game is completed if objective is reached!"
                        )


def do_check():
    print("set_debug=" + str(set_debug.get()))
    plot_field()


root = Tk()
root.title("oGame")

set_debug = StringVar()
set_debug.set(1)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=do_nothing)
filemenu.add_command(label="Open", command=do_nothing)
filemenu.add_command(label="Save", command=do_nothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

toolsmenu = Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Settings", command=do_nothing)
toolsmenu.add_command(label="Advanced", command=do_nothing)
toolsmenu.add_checkbutton(label="Debug", onvalue=1, offvalue=0, variable=set_debug, command=do_check)
menubar.add_cascade(label="Tools", menu=toolsmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=do_nothing)
helpmenu.add_command(label="Tutorial", command=do_tutorial)
helpmenu.add_command(label="About...", command=do_about)
menubar.add_cascade(label="Help", menu=helpmenu)

# global variables
c_width = 500
c_height = 500
disks = []
d_size = 1
n_rows = 10

cv = Canvas(root,
            width=c_width,
            height=c_height)
cv.pack(fill="both", expand=True)


# Disk class to store basic disk info like position and color
class Disk:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = "grey"
        self.sides = []
        self.start = False
        self.dist = 0

    def lowest(self):
        m = 999
        for d in self.sides:
            if d.dist < m:
                m = d.dist
        return m


def create_triangle():
    print("create_triangle:")
    global disks
    disks.clear()
    disks = []
    sg = d_size * 0.9
    for y in range(n_rows):
        yy = d_size + y * sg
        for x in range(y):
            xx = 6 * d_size + x * d_size - y * d_size / 2
            d = Disk()
            d.x = xx
            d.y = yy
            d.index = len(disks)
            if x == 0 or x == (y - 1) or y == (n_rows - 1):
                d.start = True
            if y > 1:
                if x > 0:
                    # left up
                    d.sides.append(disks[d.index - y])
                if x < y - 1:
                    # right up
                    d.sides.append(disks[d.index - y + 1])
                if x > 0:
                    # left
                    d.sides.append(disks[d.index - 1])
                if x > 0:
                    # right
                    disks[d.index - 1].sides.append(d)
                if x < y - 1:
                    # left down
                    disks[d.index - y + 1].sides.append(d)
                if x > 0:
                    # right down
                    disks[d.index - y].sides.append(d)
            disks.append(d)


def update_triangle():
    print("update_triangle:")
    global disks
    sg = d_size * 0.9
    i = 0
    for y in range(n_rows):
        yy = d_size + y * sg - sg / 2
        for x in range(y):
            xx = ((n_rows + 1) / 2) * d_size + x * d_size - y * d_size / 2
            d = disks[i]
            i = i + 1
            d.gx = xx
            d.gy = yy


def plot_field():
    global set_debug
    print("plot_field")
    sd = d_size * 0.9 / 2
    for d in disks:
        cv.create_oval(d.gx - sd, d.gy - sd, d.gx + sd, d.gy + sd, outline="purple", fill=d.color)
        if set_debug.get() == "1":
            s = str(d.index) + "=" + str(d.start) + "\n"
            for ds in d.sides:
                s = s + str(ds.index) + ","
            s = s + "\ndist=" + str(d.dist)
            if d.color == "white":
                cv.create_text(d.gx, d.gy, text=s, fill="blue", font=("San Serif", 8))
            else:
                cv.create_text(d.gx, d.gy, text=s, fill="white", font=("San Serif", 8))


def resize(event):
    global d_size
    global c_width
    global c_height
    c_width = event.width
    c_height = event.height
    print("resize " + str(c_width) + "x" + str(c_height))
    draw_field()


def draw_field():
    global d_size
    # create background
    b = 1
    cv.create_rectangle(b, b, c_width - b, c_height - b, outline="black", fill="lightgrey")
    d_size = min(c_width, c_height) / n_rows
    update_triangle()
    plot_field()


def calc(disk):
    global disks
    # set starting positions
    for d in disks:
        d.dist = 999
    disk.dist = 0

    # calculate
    change = True
    loop = 0
    while change:
        loop = loop + 1
        print("loop " + str(loop))
        change = False
        for d in disks:
            if d.color == 'grey':
                m = d.lowest() + 1
                if d.dist != m:
                    d.dist = m
                    change = True
            if d.color == disk.color and d.index != disk.index:
                m = d.lowest()
                if d.dist != m:
                    d.dist = m
                    change = True


def left_click(event):
    global disks
    global d_size
    print("left-Click")
    x = event.gx
    y = event.gy
    for d in disks:
        if pow(pow(x - d.gx, 2) + pow(y - d.gy, 2), 0.5) < d_size / 2:
            if d.color == "grey":
                d.color = "white"
                calc(d)
    draw_field()


def center_click(event):
    print("center-Click")


def right_click(event):
    global disks
    global d_size
    print("right-Click")
    x = event.gx
    y = event.gy
    for d in disks:
        if pow(pow(x - d.gx, 2) + pow(y - d.gy, 2), 0.5) < d_size / 2:
            if d.color == "grey":
                d.color = "black"
    draw_field()


cv.bind("<Configure>", resize)
cv.bind("<Button-1>", left_click)
cv.bind("<Button-2>", center_click)
cv.bind("<Button-3>", right_click)

create_triangle()

root.config(menu=menubar)
root.mainloop()
