import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\khakh\OneDrive\Desktop\projects\E_Commerce_data_Analysis_Dashb\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("999x551")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 551,
    width = 999,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    2.0,
    46.0,
    267.0,
    551.0,
    fill="#C9C9C9",
    outline="")

canvas.create_rectangle(
    1.0,
    47.0,
    266.0,
    552.0,
    fill="#F9F9F9",
    outline="")

canvas.create_rectangle(
    0.0,
    3.0,
    999.0,
    49.0,
    fill="#D7D7D7",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    543.5,
    98.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D1F1EB",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=319.0,
    y=83.0,
    width=449.0,
    height=29.0
)

canvas.create_rectangle(
    0.0,
    0.0,
    999.0,
    46.0,
    fill="#38BBD8",
    outline="")

canvas.create_rectangle(
    9.0,
    4.0,
    58.0,
    43.0,
    fill="#FFEBCD",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    33.0,
    23.0,
    image=image_image_1
)

canvas.create_text(
    72.0,
    11.0,
    anchor="nw",
    text="E-Commerence DataAnalysis Dashboard\n",
    fill="#21272A",
    font=("Righteous Regular", 22 * -1)
)

canvas.create_rectangle(
    318.0,
    150.0,
    531.0,
    324.0,
    fill="#C9C9C9",
    outline="")

canvas.create_rectangle(
    320.0,
    352.0,
    533.0,
    526.0,
    fill="#C9C9C9",
    outline="")

canvas.create_rectangle(
    320.0,
    352.0,
    533.0,
    526.0,
    fill="#C9C9C9",
    outline="")

canvas.create_rectangle(
    316.0,
    148.0,
    529.0,
    322.0,
    fill="#F9F9F9",
    outline="")

canvas.create_rectangle(
    318.0,
    350.0,
    531.0,
    524.0,
    fill="#F9F9F9",
    outline="")

canvas.create_rectangle(
    318.0,
    350.0,
    531.0,
    524.0,
    fill="#F9F9F9",
    outline="")

canvas.create_rectangle(
    555.0,
    151.0,
    971.0,
    324.0,
    fill="#C2C2C2",
    outline="")

canvas.create_rectangle(
    553.0,
    353.0,
    969.0,
    526.0,
    fill="#C2C2C2",
    outline="")

canvas.create_rectangle(
    553.0,
    149.0,
    969.0,
    322.0,
    fill="#F9F9F9",
    outline="")

canvas.create_rectangle(
    551.0,
    351.0,
    967.0,
    524.0,
    fill="#F9F9F9",
    outline="")

canvas.create_rectangle(
    797.0,
    551.0,
    1010.0,
    725.0,
    fill="#C2C2C2",
    outline="")

canvas.create_rectangle(
    794.0,
    546.0,
    1007.0,
    720.0,
    fill="#F9F9F9",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=777.0,
    y=83.0,
    width=56.0,
    height=31.0
)
window.resizable(False, False)
window.mainloop()
