# imports
from structure import *
from menu import *


root.title("Oskar Game")
root.config(menu=menu_bar)

# create main variables, Field and Tk application window.
f.create()
f.draw()

# add bindings, can this be done earlier
canvas.bind("<Configure>", resize)
canvas.bind("<Button-1>", left_click)
#  canvas.bind("<Button-2>", center_click)
canvas.bind("<Button-3>", right_click)

# run main loop
root.mainloop()

