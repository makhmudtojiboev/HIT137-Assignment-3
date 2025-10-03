# utils.py
from tkinter import filedialog, messagebox

def choose_image_file():
    """Opens a dialog to choose an image file."""
    return filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])

def show_error(msg):
    """Displays an error message box."""
    messagebox.showerror("Error", msg)