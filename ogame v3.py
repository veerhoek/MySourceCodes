import tkinter
from tkinter import *
from tkinter import messagebox
import keyboard as kb

COL_PLAYER = 'white'
COL_AI = 'black'
COL_EMPTY = 'grey'


def do_nothing():
    x = 0


def do_about():
    messagebox.showinfo("oGame", "oGame application\n\nby Jaap on Mac\nDate Aug-2021\nVersion 0.3")


def do_tutorial():
    messagebox.showinfo("oGame",
                        "Objective:\nconnect three sides with colors from the same color\n\n" +
                        "Left click is white disk, right click is black disk\n\n" +
                        "The AI will take the other color and try to beat you\n" +
                        "A 'hint' option is under development\n\n" +
                        "Game is completed if objective is reached!"
                        )


def do_new():
    f.create()
    f.draw()


def do_check_button():
    print("set_debug=" + str(set_debug.get()))
    f.draw()


def do_level_button():
    print("set_level=" + str(set_level.get()))


# Disk class to store basic disk info like position and color
class Disk:
    def __init__(self):
        self.ix = 0
        self.iy = 0
        self.color = COL_EMPTY
        self.sides = []  # array of (up to 6) side disks
        self.start = False  # this indicates edge, will be removed, not used
        self.dist = 0  # indicated distance from target disk

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
        self.rows = 11
        self.width = 500
        self.height = 500
        self.gridx = min(self.width, self.height) / self.rows
        self.gridy = self.gridx * 0.9
        self.size = self.gridy
        # disk variables
        self.disks = []  # array of all disks
        self.l_edge = []  # array of all disks on the left side
        self.r_edge = []  # array of all disks on the right side
        self.b_edge = []  # array of all disks on the bottom side

    def set_wh(self, w, h):
        self.width = w
        self.height = h
        self.gridx = min(self.width, self.height) / self.rows
        self.gridy = self.gridx * 0.9
        self.size = self.gridy

    def create(self):
        # this functions creates (or recreates) the arrays and indices (NOT the graphics part)
        self.disks.clear()
        self.disks = []
        for y in range(self.rows):
            for x in range(y):
                d = Disk()
                d.ix = x
                d.iy = y
                d.index = len(self.disks)
                if x == 0 or x == (y - 1) or y == (self.rows - 1):
                    d.start = True
                if x == 0:
                    self.l_edge.append(d)
                if x == (y - 1):
                    self.r_edge.append(d)
                if y == (self.rows - 1):
                    self.b_edge.append(d)

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

    def get_gx(self, ix, iy):
        gx = (ix + 0.5 - iy / 2) * self.gridx + (self.rows / 2) * self.gridx
        return gx

    def get_gy(self, ix, iy):
        gy = (iy + 0.5) * self.gridy
        return gy

    def draw(self):
        global set_debug
        global canvas
        self.set_wh(self.width, self.height)
        # create background
        b = 1
        canvas.create_rectangle(b, b, self.width - b, self.height - b, outline="black", fill="lightgrey")
        # draw disks
        size2 = self.size / 2
        for d in self.disks:
            gx = (d.ix + 0.5 - d.iy / 2) * self.gridx + (self.rows / 2) * self.gridx
            gy = (d.iy + 0.5) * self.gridy
            canvas.create_oval(gx - size2, gy - size2, gx + size2, gy + size2, outline="purple", fill=d.color)
            if set_debug.get() == "1":
                s = str(d.index) + "=" + str(d.start) + "\n"
                i = 0
                for ds in d.sides:
                    s = s + str(ds.index) + ","
                    i = i + 1
                    if i == 3:
                        s = s + "\n"

                s = s + "\ndist=" + str(d.dist)
                if d.color == COL_PLAYER:
                    canvas.create_text(gx, gy, text=s, fill="blue", font=("San Serif", 7))
                else:
                    canvas.create_text(gx, gy, text=s, fill="white", font=("San Serif", 7))


# create main variables, Filed and Tk application window.
f = Field()
f.create()

root = Tk()
root.title("oGame")

# status_text2 = StringVar()
# status_text2.set("Status bar ...")
# status_bar2 = Label(root, textvariable=status_text2, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
# status_bar2.pack(side=tkinter.TOP, fill=tkinter.X)

# button_bar = Frame(root, bd=1, relief=tkinter.SUNKEN, height=25)
button1 = Button(root, text="New")
# button2 = Button(button_bar, text="Play")
# button3 = Button(button_bar, text="Help")
# button4 = Button(button_bar, text="Quit")

canvas = Canvas(root, width=f.width, height=f.height)
canvas.pack(fill="both", expand=True)

status_text = StringVar()
status_text.set("Status bar ...")
status_bar = Label(root, textvariable=status_text, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
status_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)


set_debug = StringVar()
set_debug.set(0)
set_level = StringVar()
set_level.set(2)

menu_bar = Menu(root)
menu_file = Menu(menu_bar, tearoff=0)
menu_file.add_command(label="New", command=do_new)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=menu_file)

menu_edit = Menu(menu_bar, tearoff=0)
menu_edit.add_command(label="Hint", command=do_nothing)
menu_edit.add_command(label="Undo", command=do_nothing)
menu_bar.add_cascade(label="Edit", menu=menu_edit)

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


def statusbar_text(text):
    status_text.set(text)


def resize(event):
    global f
    f.width = event.width
    f.height = event.height
    print("resize " + str(f.width) + "x" + str(f.height))
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
            if d.color == COL_EMPTY:
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
        if d.color == COL_EMPTY:
            d.color = color
            calc(d)
            sc = score()
            if sc == m:
                c = c + 1
            if sc < m:
                m = sc
                index = d.index
                c = 1
            d.color = COL_EMPTY
            print("index=" + str(d.index) + " score=" + str(sc) + " best=" + str(index) + " count=" + str(c))
    return index


def play(color):
    global f
    if color == COL_PLAYER:
        o = COL_AI
    else:
        o = COL_PLAYER

    index = -1
    m = 999
    m1 = 999
    m2 = 999
    for d1 in f.disks:
        # look for other color
        if d1.color == o:
            for d2 in d1.sides:
                # check sides
                if d2.color == COL_EMPTY:
                    d2.color = color
                    calc(d2)
                    sc = score()
                    if sc < m2:
                        m2 = sc
                        index = d2.index
                    d2.color = COL_EMPTY
    # now make move
    if index < 0:
        pass
    else:
        print("play index " + str(index))
        d = f.disks[index]
        d.color = color
        calc(d)


def play2(color):
    global f
    if color == COL_PLAYER:
        o = COL_AI
    else:
        o = COL_PLAYER

    index = 0
    m = 999
    m1 = 999
    for d1 in f.disks:
        if d1.color == COL_EMPTY:
            print("Play index1 " + str(d1.index))
            d1.color = color
            calc(d1)
            sc = score()
            if sc <= m1:
                m1 = sc
                for d2 in f.disks:
                    if d2.color == COL_EMPTY:
                        print("  Play index2 " + str(d2.index))
                        d2.color = o
                        for d3 in f.disks:
                            if d3.color == COL_EMPTY:
                                d3.color = color
                                calc(d3)
                                sc = score()
                                print("    Play index3 " + str(sc) + " < " + str(m))
                                if sc < m:
                                    m = sc
                                    index = d1.index
                                d3.color = COL_EMPTY
                        d2.color = COL_EMPTY
            d1.color = COL_EMPTY
    # now make move
    print("play index " + str(index))
    d = f.disks[index]
    d.color = color
    calc(d)


def left_click(event):
    print("left-Click")
    if kb.is_pressed("ctrl"):
        ctrl = True
    else:
        ctrl = False

    x = event.x
    y = event.y
    for d in f.disks:
        gx = (d.ix + 0.5 - d.iy / 2) * f.gridx + (f.rows / 2) * f.gridx
        gy = (d.iy + 0.5) * f.gridy
        if pow(pow(x - gx, 2) + pow(y - gy, 2), 0.5) < f.size / 2:
            if d.color == COL_EMPTY:
                d.color = COL_PLAYER
                calc(d)
                if ctrl:
                    d.color = COL_EMPTY
    f.draw()
    status_text.set("Score=" + str(score()))
    if not ctrl:
        score()
        play(COL_AI)
        f.draw()


def center_click(event):
    print("center-Click")
    get_hint(COL_PLAYER)


def right_click(event):
    print("right-Click")
    x = event.x
    y = event.y
    for d in f.disks:
        gx = (d.ix + 0.5 - d.iy / 2) * f.gridx + (f.rows / 2) * f.gridx
        gy = (d.iy + 0.5) * f.gridy
        if pow(pow(x - gx, 2) + pow(y - gy, 2), 0.5) < f.size / 2:
            if d.color == COL_EMPTY:
                d.color = COL_AI
    f.draw()


canvas.bind("<Configure>", resize)
canvas.bind("<Button-1>", left_click)
canvas.bind("<Button-2>", center_click)
canvas.bind("<Button-3>", right_click)

f.draw()

root.config(menu=menu_bar)
root.mainloop()
