from tkinter import *
from tkinter import messagebox

# color constants
COL_PLAYER = 'white'
COL_AI     = 'black'
COL_EMPTY  = 'grey'


def do_nothing():
    x = 0


def do_about():
    messagebox.showinfo("oGame", "oGame application\n\nby Jaap on Mac\nDate Aug-2021\nVersion 0.2")


def do_tutorial():
    messagebox.showinfo("oGame",
                        "Objective:\nconnect three sides with colors from the same color\n\n" +
                        "Left click is white disk, right click is black disk\n\n" +
                        "The AI will take the other color and try to beat you\n" +
                        "A 'hint' option is under development\n\n" +
                        "Game is completed if objective is reached!"
                        )


def do_check_button():
    print("set_debug=" + str(set_debug.get()))
    f.draw()


def do_level_button():
    print("set_level=" + str(set_level.get()))


# Disk class to store basic disk info like position and color
class Disk:
    def __init__(self):
        self.ix = 0  # index x
        self.iy = 0  # index y
        self.gx = 0  # graphic x
        self.gy = 0  # graphic y
        self.color = COL_EMPTY
        self.sides = []
        self.start = False
        self.dist = 0

    # calculate the lowest dist from all neighbors/sides
    def lowest(self):
        m = 999
        for d in self.sides:
            if d.dist < m:
                m = d.dist
        return m


class Field:
    def __init__(self):
        # size variables
        self.width = 500
        self.height = 500
        self.rows = 10
        self.size = min(self.width, self.height) / self.rows
        self.grid = self.size * 0.9
        # disk arrays
        self.disks = []
        self.l_edge = []
        self.r_edge = []
        self.b_edge = []

    def create(self):
        self.disks.clear()
        self.disks = []
        self.size = min(self.width, self.height) / self.rows
        self.grid = self.size * 0.9
        for y in range(self.rows):
            yy = self.size + y * self.grid
            for x in range(y):
                xx = ((self.rows + 1) / 2) * self.size + x * self.size - y * self.size / 2
                d = Disk()
                d.ix = x
                d.iy = y
                d.gx = xx
                d.gy = yy
                d.index = len(self.disks)
                if x == 0 or x == (y - 1) or y == (self.rows - 1):
                    d.start = True
                if y > 1:
                    if x > 0:  # left up
                        d.sides.append(self.disks[d.index - y])
                    if x < y - 1:  # right up
                        d.sides.append(self.disks[d.index - y + 1])
                    if x > 0:  # left
                        d.sides.append(self.disks[d.index - 1])
                    if x > 0:  # right
                        self.disks[d.index - 1].sides.append(d)
                    if x < y - 1:  # left down
                        self.disks[d.index - y + 1].sides.append(d)
                    if x > 0:  # right down
                        self.disks[d.index - y].sides.append(d)
                self.disks.append(d)

    def update(self):
        print("update")
        self.size = min(self.width, self.height) / self.rows
        self.grid = self.size * 0.9
        i = 0
        for y in range(self.rows):
            yy = self.size + y * self.grid - self.grid / 2
            for x in range(y):
                d = self.disks[i]
                i = i + 1
                xx = ((self.rows + 1) / 2) * self.size + x * self.size - y * self.size / 2
                d.gx = xx
                d.gy = yy

    def draw(self):
        global set_debug
        global canvas
        # create background
        b = 1
        canvas.create_rectangle(b, b, self.width - b, self.height - b, outline="black", fill="lightgrey")
        # draw disks
        sd = self.size * 0.9 / 2
        for d in self.disks:
            canvas.create_oval(d.gx - sd, d.gy - sd, d.gx + sd, d.gy + sd, outline="purple", fill=d.color)
            if set_debug.get() == "1":
                s = str(d.index) + "=" + str(d.start) + "\n"
                i = 0
                for ds in d.sides:
                    s = s + str(ds.index) + ","
                    i = i + 1
                    if i == 3:
                        s = s + "\n"

                s = s + "\ndist=" + str(d.dist)
                if d.color == self.player:
                    canvas.create_text(d.gx, d.gy, text=s, fill="blue", font=("San Serif", 7))
                else:
                    canvas.create_text(d.gx, d.gy, text=s, fill="white", font=("San Serif", 7))


# create main variables, Filed and Tk application window.
f = Field()
f.create()

root = Tk()
root.title("oGame")

canvas = Canvas(root, width=f.width, height=f.height)
canvas.pack(fill="both", expand=True)

set_debug = StringVar()
set_debug.set(1)
set_level = StringVar()
set_level.set(2)

menu_bar = Menu(root)
menu_file = Menu(menu_bar, tearoff=0)
menu_file.add_command(label="New", command=do_nothing)
menu_file.add_command(label="Open", command=do_nothing)
menu_file.add_command(label="Save", command=do_nothing)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=menu_file)

menu_tools = Menu(menu_bar, tearoff=0)
menu_tools.add_command(label="Settings", command=do_nothing)
menu_tools.add_command(label="Advanced", command=do_nothing)
menu_tools.add('separator')
menu_tools.add_checkbutton(label="Debug", onvalue=1, offvalue=0, variable=set_debug, command=do_check_button)
menu_tools.add('separator')
menu_tools.add_radiobutton(label="Expert", value=1, variable=set_level, command=do_level_button)
menu_tools.add_radiobutton(label="Normal", value=2, variable=set_level, command=do_level_button)
menu_tools.add_radiobutton(label="Novice", value=3, variable=set_level, command=do_level_button)
menu_bar.add_cascade(label="Tools", menu=menu_tools)

menu_help = Menu(menu_bar, tearoff=0)
menu_help.add_command(label="Help Index", command=do_nothing)
menu_help.add_command(label="Tutorial", command=do_tutorial)
menu_help.add_command(label="About...", command=do_about)
menu_bar.add_cascade(label="Help", menu=menu_help)


def resize(event):
    global f
    f.width = event.width
    f.height = event.height
    print("resize " + str(f.width) + "x" + str(f.height))
    f.update()
    f.draw()


def calc(disk):
    # set starting positions
    for d in f.disks:
        d.dist = 999
    disk.dist = 0
    # calculate
    change = True
    loop = 0
    while change:
        loop = loop + 1
        # print("loop " + str(loop))
        change = False
        for d in f.disks:
            if d.color == f.empty:
                m = d.lowest() + 1
                if d.dist != m:
                    d.dist = m
                    change = True
            if d.color == disk.color and d.index != disk.index:
                m = d.lowest()
                if d.dist != m:
                    d.dist = m
                    change = True


def score():
    l_score = 0
    r_score = 0
    b_score = 0
    # find minimal values
    l_min = 999
    r_min = 999
    b_min = 999
    i = 0
    for y in range(f.rows):
        for x in range(y):
            d = f.disks[i]
            i = i + 1
            if x == 0 and d.dist < l_min:
                l_min = d.dist
            if x == y - 1 and d.dist < r_min:
                r_min = d.dist
            if y == f.rows - 1 and d.dist < b_min:
                b_min = d.dist
    # print("l_min=" + str(l_min))
    # print("r_min=" + str(r_min))
    # print("b_min=" + str(b_min))
    return l_min + r_min + b_min


def get_hint(color):
    index = 0
    m = 999
    c = 0
    for d in f.disks:
        if d.color == f.empty:
            d.color = color
            calc(d)
            sc = score()
            if sc == m:
                c = c + 1
            if sc < m:
                m = sc
                index = d.index
                c = 1
            d.color = f.empty
            print("index=" + str(d.index) + " score=" + str(sc) + " best=" + str(index) + " count=" + str(c))
    return index


def left_click(event):
    print("left-Click")
    x = event.gx
    y = event.gy
    for d in f.disks:
        if pow(pow(x - d.gx, 2) + pow(y - d.gy, 2), 0.5) < f.size / 2:
            if d.color == f.empty:
                d.color = f.player
                calc(d)
    f.draw()
    score()
    # play ai
    ai = get_hint(f.ai)
    print("ai hint=" + str(ai))
    d = f.disks[ai]
    d.color = f.ai
    calc(d)
    f.draw()


def center_click(event):
    print("center-Click")
    get_hint(f.player)


def right_click(event):
    print("right-Click")
    x = event.gx
    y = event.gy
    for d in f.disks:
        if pow(pow(x - d.gx, 2) + pow(y - d.gy, 2), 0.5) < f.size / 2:
            if d.color == f.empty:
                d.color = f.ai
    f.draw()


canvas.bind("<Configure>", resize)
canvas.bind("<Button-1>", left_click)
canvas.bind("<Button-2>", center_click)
canvas.bind("<Button-3>", right_click)

f.draw()

root.config(menu=menu_bar)
root.mainloop()
