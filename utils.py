import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas

def get_btn(window, command, img,place_x, place_y, width, height,relief):
    #img0 = tk.PhotoImage(file =f"../assets/decrypt_btn_main.png")
    button = tk.Button(
        window,
        image = img,
        borderwidth= 0,
        width=width, height=height,
        highlightthickness=0,
        command = command,
        relief = relief,
    )
    return button.place(x= place_x, y=place_y)

def getCanvas(window, bg, img, place_x, place_y, width,height, center_x, center_y,relief):
    canvas = Canvas(
        window,
        bg=bg,
        width = width,
        height = height,
        bd = 0,
        highlightthickness= 0,
        relief = relief
    )
    canvas.create_image(center_x,center_y,image=img)
    canvas.place(x = place_x, y = place_y)

def getText(window, x, y, width, height):
    inputtxt = tk.Text(
        window,
        bd=0,
        bg="#d9d9d9",
        highlightthickness=0
    )
    inputtxt.place(x=x, y=y, width=width, height=height)
    return inputtxt

def getEntry(window, x, y, width, height):
    inputtxt = tk.Entry(
        window,
        bd=0,
        bg="#d9d9d9",
        highlightthickness=0
    )
    inputtxt.place(x=x, y=y, width=width, height=height)
    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)
