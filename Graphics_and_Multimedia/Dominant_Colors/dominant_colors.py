#!/usr/bin/env python3
"""An image analyser that finds the three most common colors in an image.

Title:
Dominant Colors

Description:
Develop a program that accepts an image
either via the devices's camera (if it has one)
or a file dialog.
Your program should intelligently determine
three of the most dominant colors in the image
and present it to the user.
The dominant colors in this case are the colors
that appear most in a given image.
For added complexity,
generate the RGB, HSB, CYMK and HEX color.
Also you can add the ability
to save the generated color palette with all the above information.
"""
import colorsys
import tkinter as tk
from tkinter import filedialog, ttk

from PIL import Image, ImageTk


class MainWindow(tk.Tk):
    """The class for interacting with tkinter."""

    def __init__(self):
        """Initialise window."""
        super().__init__()
        self.title("Dominant Colors")
        self.geometry()
        self.resizable(width=False, height=False)

        self.bands = tk.StringVar()
        self.color_images = []

        self.current_image_frame = ttk.Frame(self)
        self.bands_frame = ttk.Frame(self)
        self.colors_frame = ttk.Frame(self)

        self.current_image_label = ttk.Label(self.current_image_frame,
                                             text="Currently opened image")
        self.current_image_label2 = ttk.Label(self.current_image_frame,
                                              text="None")
        self.bands_label = ttk.Label(self.bands_frame,
                                     text="The bands of the image are")
        self.bands_entry = ttk.Entry(self.bands_frame,
                                     textvariable=self.bands,
                                     state="readonly",
                                     justify=tk.CENTER)
        self.dominant_colors_label = ttk.Label(self.colors_frame,
                                               text="Most common colors")
        self.dominant_color_treeview = ttk.Treeview(self.colors_frame,
                                                    columns=("RGB",
                                                             "HSL",
                                                             "HSV",
                                                             "HEX"))
        self.choose_image_button = ttk.Button(self,
                                              command=self.new_image,
                                              text="Choose a new image")

        self.dominant_color_treeview.column("#0", minwidth=40,
                                            width=40, stretch=0)
        self.dominant_color_treeview.column("RGB", minwidth=100,
                                            width=100, anchor=tk.CENTER)
        self.dominant_color_treeview.heading("RGB", text="RGB/RGBA")
        self.dominant_color_treeview.column("HSL", minwidth=100,
                                            width=100, anchor=tk.CENTER)
        self.dominant_color_treeview.heading("HSL", text="HSL")
        self.dominant_color_treeview.column("HSV", minwidth=100,
                                            width=100, anchor=tk.CENTER)
        self.dominant_color_treeview.heading("HSV", text="HSV")
        self.dominant_color_treeview.column("HEX", minwidth=100,
                                            width=100, anchor=tk.CENTER)
        self.dominant_color_treeview.heading("HEX", text="HEX")
        for item_id in range(0, 3):
            self.dominant_color_treeview.insert("", "end", item_id,
                                                values=("", "", ""))

        self.current_image_frame.grid(row=0, column=0, padx=5, pady=10)
        self.bands_frame.grid(row=1, column=0, padx=5, pady=10)
        self.colors_frame.grid(row=2, column=0, padx=5, pady=10)

        self.current_image_label.grid(row=0, column=0, padx=5, pady=2.5)
        self.current_image_label2.grid(row=1, column=0, padx=5, pady=5)
        self.bands_label.grid(row=0, column=0, padx=5, pady=2.5)
        self.bands_entry.grid(row=1, column=0, padx=5, pady=5)
        self.dominant_colors_label.grid(row=0, column=0, padx=5, pady=2.5,
                                        columnspan=3)
        self.dominant_color_treeview.grid(row=1, column=0)
        self.choose_image_button.grid(row=3, column=0, padx=10, pady=10)

    def new_image(self):
        """Get image path from user and display dominant colors."""
        image_path = filedialog.askopenfilename(parent=self,
                                                title="Please choose an image",
                                                defaultextension=".png",
                                                filetypes=[("Image", ("*.png", "*jpg")),
                                                           ("All files", "*.*")])
        if not image_path:
            return
        self.current_image_label2.config(text=image_path)

        image = load_image(image_path)
        colors = image.getcolors(maxcolors=image.size[0]*image.size[1])
        most_frequent_colors = dominant_colors(colors)
        color_dict_list = convert_to_color_dict_list(most_frequent_colors)

        self.color_images = []
        for item_id in range(0, 3):
            self.color_images.append(ImageTk.PhotoImage(Image.new("RGBA",
                                                                  (16, 16),
                                                                  color=color_dict_list[item_id]
                                                                  ["rgb"])))
            self.dominant_color_treeview.item(item_id,
                                              image=self.color_images[item_id],
                                              values=(color_dict_list[item_id]["rgb"],
                                                      color_dict_list[item_id]["hsl"],
                                                      color_dict_list[item_id]["hsv"],
                                                      "".join(color_dict_list[item_id]["hex"])))
        self.bands.set("".join(image.getbands()))


def load_image(image_path: str) -> Image.Image:
    """Return Image object of specified image."""
    image = Image.open(image_path)
    image.load()
    return image


def dominant_colors(colors: list) -> list:
    """Return the three most dominant colors."""
    most_frequent_colors = []
    color_dict = {color[0]: color[1] for color in colors}

    for _ in range(0, 3):
        most_frequent_color = max(color_dict.keys())
        most_frequent_colors.append(color_dict[most_frequent_color])
        del color_dict[most_frequent_color]
    return most_frequent_colors


def convert_to_color_dict_list(colors: list) -> list:
    """Return a list of dictionaries of colors in different formats."""
    color_dict_list = []

    for color in colors:
        hex_color = []
        for color_index in range(0, 3):
            hex_color_part = hex(color[color_index]).replace("0x", "")
            if len(hex_color_part) == 1:
                hex_color_part = "0" + hex_color_part
            hex_color.append(hex_color_part)

        color_dict_list.append({
            "rgb": color,
            "hsl": [round(color, 2) for color
                    in colorsys.rgb_to_hls(color[0], color[1], color[2])],
            "hsv": [round(color, 2) for color
                    in colorsys.rgb_to_hsv(color[0], color[1], color[2])],
            "hex": hex_color
        })
    return color_dict_list


def _start_gui():
    """Start the Graphical User Interface."""
    window = MainWindow()
    window.mainloop()


if __name__ == "__main__":
    _start_gui()
