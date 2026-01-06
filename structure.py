# structure file, contains classes
from init import *
import random


# Disk class to store basic disk info like position and color
class Disk:
    def __init__(self):
        self.ix = 0
        self.iy = 0
        self.color = colors.EMPTY
        self.icolor = 0
        self.sides = []  # array of (up to 6) side disks
        self.start = False  # this indicates edge, will be removed, not used
        self.dist = 0  # indicated distance from target disk
        #

    # calculate the lowest dist from all neighbors/sides
    # assumes a calc is done nad e.g. AI disks are 999
    def lowest(self):
        m = 999
        for d in self.sides:
            if d.dist < m:
                m = d.dist
        return m


class Field:
    def __init__(self):
        # assume root to be there!
        # size variables
        self.rows = 10 + 1
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
        # button
        self.aaa = Button(root, text="New", width=100, height=200)
        # self.aaa.pack(fill="both")
        # gui
        # button row
        # fr = Frame(root)
        # b1 = Button(fr, text="New")
        # b2 = Button(fr, text="Hint")
        # b3 = Button(fr, text="Undo")
        # p = 3
        # b1.grid(row=0, column=0, padx=(p, p), pady=(p, 0))
        # b2.grid(row=0, column=1, padx=(p, p), pady=(p, 0))
        # b3.grid(row=0, column=2, padx=(p, p), pady=(p, 0))
        # fr.grid(row=0, column=0, sticky="nw")

        # self.canvas = Canvas(root, width=self.width, height=self.height)
        # # self.canvas.pack(fill="both", expand=True)
        # self.canvas.grid(row=1, column=0, sticky="nswe")
        # # Status bar
        # self.status_text = StringVar()
        # self.status_text.set("Status bar ...")
        # self.status_bar = Label(root, textvariable=self.status_text, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
        # # self.status_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        # self.status_bar.grid(row=2, column=0, sticky="we")
        # root.grid_columnconfigure(0, weight=1)
        # root.grid_rowconfigure(0, weight=0)
        # root.grid_rowconfigure(1, weight=1)
        # root.grid_rowconfigure(2, weight=0)

    def set_wh(self, w, h):
        self.width = w
        self.height = h
        self.gridx = min(self.width, self.height) / self.rows
        self.gridy = self.gridx * 0.9
        self.size = self.gridy

    def get_gx(self, ix, iy):
        gx = (ix + 0.5 - iy / 2) * self.gridx + (self.rows / 2) * self.gridx
        return gx

    def get_gy(self, ix, iy):
        gy = (iy + 0.5) * self.gridy
        return gy

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
        ll = int(len(self.disks))
        l1 = int(ll/3)
        l2 = int(ll*2/3)
        if set_first.get() == "AI":
            i = random.randint(l1, l2)
            print(str(len(self.disks)) + " " + str(i))
            self.disks[i].color = colors.AI

    def draw(self):
        self.set_wh(self.width, self.height)
        # create background
        b = 0
        canvas.create_rectangle(b, b, self.width - b, self.height - b, fill=colors.BACK)
        b = 3
        canvas.create_rectangle(b, b, self.width - b, self.height - b, outline="black", fill=colors.BACK)
        # draw disks
        size2 = self.size / 2
        for d in self.disks:
            gx = self.get_gx(d.ix, d.iy)
            gy = self.get_gy(d.ix, d.iy)
            # gx = (d.ix + 0.5 - d.iy / 2) * self.gridx + (self.rows / 2) * self.gridx
            # gy = (d.iy + 0.5) * self.gridy
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
                # create disk with optional text string
                if d.color == colors.PLAYER:
                    canvas.create_text(gx, gy, text=s, fill="blue", font=("San Serif", 7))
                else:
                    canvas.create_text(gx, gy, text=s, fill="white", font=("San Serif", 7))

    def score(self):
        # l_score = 0
        # r_score = 0
        # b_score = 0
        # find minimal values
        l_min = 999
        r_min = 999
        b_min = 999
        i = 0
        for y in range(self.rows):
            for x in range(y):
                d = self.disks[i]
                i = i + 1
                if x == 0 and d.dist < l_min:
                    l_min = d.dist
                if x == y - 1 and d.dist < r_min:
                    r_min = d.dist
                if y == f.rows - 1 and d.dist < b_min:
                    b_min = d.dist
        return l_min + r_min + b_min

    def calc(self, disk):
        # set starting positions to 999 for all disks
        for d in self.disks:
            d.dist = 999

        # disk to 0 as starting point
        disk.dist = 0
        # calculate, loop through al disk at take maximum  of all surrounding disks (if != other) + 1
        # do this until no changes are being made
        change = True
        loop = 0
        while change:
            loop = loop + 1
            change = False
            for d in self.disks:
                if d.color == colors.EMPTY:
                    m = d.lowest() + 1
                    if d.dist != m:  # TODO why != and not <=?
                        d.dist = m
                        change = True
                if d.color == disk.color and d.index != disk.index:
                    m = d.lowest()
                    if d.dist != m:  # TODO why != and not <=?
                        d.dist = m
                        change = True

    def play(self, color):
        # determine other color
        if color == colors.PLAYER:
            other = colors.AI
        else:
            other = colors.PLAYER

        index = -1
        m = 999  # TODO remove not used?
        m1 = 999  # TODO remove not used?
        m2 = 999
        for d1 in self.disks:
            # look for other color
            if d1.color == other:
                for d2 in d1.sides:
                    # check sides
                    if d2.color == colors.EMPTY:
                        d2.color = color
                        self.calc(d2)
                        sc = self.score()
                        if sc < m2:
                            m2 = sc
                            index = d2.index
                        d2.color = colors.EMPTY
        # now make move
        if index < 0:
            pass
        else:
            print("play index " + str(index))
            d = self.disks[index]
            d.color = color
            self.calc(d)


# create field variable
f = Field()
