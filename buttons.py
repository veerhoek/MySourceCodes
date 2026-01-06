import tkinter
from tkinter import *

root = Tk()
root.title("Oskar Game")

fr = Frame(root)
b1 = Button(fr, text="Button1")
b2 = Button(fr, text="Button2")
b3 = Button(fr, text="Button3")
p = 3
b1.grid(row=0, column=0, padx=(p, p), pady=(p, 0))
b2.grid(row=0, column=1, padx=(p, p), pady=(p, 0))
b3.grid(row=0, column=2, padx=(p, p), pady=(p, 0))
fr.grid(row=0, column=0, sticky="nw")

cv = Canvas(root, width=400, height=400, bg="white")
cv.grid(row=1, column=0, sticky="nswe")

st_text = StringVar()
st_text.set("Status bar ...")
st = Label(root, textvariable=st_text, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
st.grid(row=2, column=0, sticky="we")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)


def draw():
    w = cv.winfo_width()
    h = cv.winfo_height()
    b = 3
    cv.create_rectangle(b, b, w - b, h - b, outline="black", fill="lightgreen")


def resize(event):
    width = event.width
    height = event.height
    print("resize " + str(width) + "x" + str(height))
    draw()


root.bind("<Configure>", resize)

draw()

root.mainloop()
