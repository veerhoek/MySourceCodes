from structure import *
from tkinter import messagebox


def do_nothing():
    x = 0


def do_not_implemented():
    messagebox.showinfo("oGame", "Not implemented yet!")


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


def do_exit():
    print("do something before Quit")
    do_quit()


def do_quit():
    root.quit()


def do_check_button():
    print("set_debug=" + str(set_debug.get()))
    f.draw()


def do_level_button():
    print("set_level=" + str(set_level.get()))


def do_player_button():
    print("set_player=" + str(set_player.get()))
    if set_player.get() == "1":
        colors.PLAYER = "white"
        colors.AI = "black"
    else:
        colors.PLAYER = "black"
        colors.AI = "white"
    do_new()
    f.draw()


def do_first_button():
    print("set_first=" + str(set_first.get()))


def resize(event):
    f.width = event.width
    f.height = event.height
    print("resize " + str(f.width) + "x" + str(f.height))
    f.draw()


def left_click(event):
    ctrl = False

    x = event.x
    y = event.y
    for d in f.disks:
        gx = f.get_gx(d.ix, d.iy)
        gy = f.get_gy(d.ix, d.iy)
        gx = (d.ix + 0.5 - d.iy / 2) * f.gridx + (f.rows / 2) * f.gridx
        gy = (d.iy + 0.5) * f.gridy
        if pow(pow(x - gx, 2) + pow(y - gy, 2), 0.5) < f.size / 2:
            if d.color == colors.EMPTY:
                d.color = colors.PLAYER
                f.calc(d)
                if ctrl:
                    d.color = colors.EMPTY
    sc_player = f.score()
    f.draw()
    if sc_player <= 0:
        messagebox.showinfo("oGame", "Player '" + colors.PLAYER + "' has won the game")
    if not ctrl:
        f.score()
        f.play(colors.AI)
        sc_ai = f.score()
        f.draw()
        if sc_ai <= 0:
            messagebox.showinfo("oGame", "Player '" + colors.AI + "' has won the game")
        status_text.set("Player Score=" + str(sc_player) + ", AI score=" + str(sc_ai))
    else:
        status_text.set("Player Score=" + str(sc_player))


def right_click(event):
    ctrl = False

    x = event.x
    y = event.y
    for d in f.disks:
        gx = f.get_gx(d.ix, d.iy)
        gy = f.get_gy(d.ix, d.iy)
        if pow(pow(x - gx, 2) + pow(y - gy, 2), 0.5) < f.size / 2:
            if d.color == colors.EMPTY:
                d.color = colors.AI
                f.calc(d)
    ai_player = f.score()
    f.draw()
    if ai_player <= 0:
        messagebox.showinfo("oGame", "Player '" + colors.PLAYER + "' has won the game")

