# objective of this file is to define al imports, basic classes and global variables
from tkinter import *
from tkinter import messagebox


class Colors:
    def __init__(self):
        self.PLAYER = 'white'
        self.AI = 'black'
        self.EMPTY = 'grey'
        self.BACK = 'lightblue'


colors = Colors()

# setup root
root = Tk()
# setup canvas
canvas = Canvas(root, width=500, height=500)


set_bool = BooleanVar()
set_bool.set(True)

set_debug = StringVar()
set_debug.set("0")

set_level = StringVar()
set_level.set("Normal")

set_player = StringVar()
set_player.set("White")

set_first = StringVar()
set_first.set("AI")

status_text = StringVar()
status_text.set("Status bar ...")


# def not_implemented():
#     messagebox.showinfo("oGame", "Not implemented yet!")

