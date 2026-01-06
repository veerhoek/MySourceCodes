import tkinter
from structure import *
from actions import *


menu_bar = Menu(root)
menu_file = Menu(menu_bar, tearoff=0)
menu_file.add_command(label="New", command=do_new)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=do_quit)
menu_bar.add_cascade(label="File", menu=menu_file)

menu_edit = Menu(menu_bar, tearoff=0)
menu_edit.add_command(label="Hint", command=do_nothing)
menu_edit.add_command(label="Undo", command=do_nothing)
menu_bar.add_cascade(label="Edit", menu=menu_edit)

menu_tools = Menu(menu_bar, tearoff=0)
menu_tools.add_command(label="Settings", command=do_not_implemented)
menu_tools.add_command(label="Advanced", command=do_not_implemented)
menu_tools.add('separator')
menu_tools.add_checkbutton(label="Debug", onvalue=1, offvalue=0, variable=set_debug, command=do_check_button)
menu_tools.add('separator')
menu_tools_level = Menu(menu_tools, tearoff=0)
menu_tools_level.add_radiobutton(label="Expert", value="Expert", variable=set_level, command=do_level_button)
menu_tools_level.add_radiobutton(label="Normal", value="Normal", variable=set_level, command=do_level_button)
menu_tools_level.add_radiobutton(label="Novice", value="Novice", variable=set_level, command=do_level_button)
menu_tools.add_cascade(label="Level", menu=menu_tools_level)
menu_tools_player = Menu(menu_tools, tearoff=0)
menu_tools_player.add_radiobutton(label="White", value="White", variable=set_player, command=do_player_button)
menu_tools_player.add_radiobutton(label="Black", value="Black", variable=set_player, command=do_player_button)
menu_tools.add_cascade(label="Player", menu=menu_tools_player)
menu_tools_first = Menu(menu_tools, tearoff=0)
menu_tools_first.add_radiobutton(label="Player", value="Player", variable=set_first, command=do_first_button)
menu_tools_first.add_radiobutton(label="AI", value="AI", variable=set_first, command=do_first_button)
menu_tools.add_cascade(label="First", menu=menu_tools_first)

menu_bar.add_cascade(label="Tools", menu=menu_tools)

menu_help = Menu(menu_bar, tearoff=0)
menu_help.add_command(label="Help Index", command=do_not_implemented)
menu_help.add_command(label="Tutorial", command=do_tutorial)
menu_help.add_command(label="About...", command=do_about)
menu_bar.add_cascade(label="Help", menu=menu_help)

# setup button bar
fr = Frame(root)
p = 3
b1 = Button(fr, text="New", command=do_new).grid(row=0, column=0, padx=(p, p), pady=(p, 0))
b2 = Button(fr, text="Hint").grid(row=0, column=1, padx=(p, p), pady=(p, 0))
b3 = Button(fr, text="Undo").grid(row=0, column=2, padx=(p, p), pady=(p, 0))
fr.grid(row=0, column=0, sticky="nw")
# setup canvas
# canvas = Canvas(root, width=500, height=500)
canvas.grid(row=1, column=0, sticky="nswe")
# setup status bar
status_bar = Label(root, textvariable=status_text, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
status_bar.grid(row=2, column=0, sticky="we")
# set weights
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
