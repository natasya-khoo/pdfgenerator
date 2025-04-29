import tkinter as tk
from tkinter import font

def toggle_tag(tag_name):
    """Toggle the specified tag on the currently selected text."""
    try:
        # Get the range of selected text
        selection_start = text.index("sel.first")
        selection_end = text.index("sel.last")
    except tk.TclError:
        # If no text is selected, do nothing
        return

    # If the selected text already has the tag applied, remove it.
    if tag_name in text.tag_names("sel.first"):
        text.tag_remove(tag_name, selection_start, selection_end)
    else:
        text.tag_add(tag_name, selection_start, selection_end)

# Initialize the main window
root = tk.Tk()
root.title("Simple Text Editor")

# Create a frame for the buttons (toolbar)
toolbar = tk.Frame(root, padx=5, pady=5)
toolbar.pack(anchor="nw", fill="x")

# Create buttons for Bold, Italic, and Underline
bold_button = tk.Button(toolbar, text="Bold", command=lambda: toggle_tag("bold"))
bold_button.pack(side="left", padx=2)

italic_button = tk.Button(toolbar, text="Italic", command=lambda: toggle_tag("italic"))
italic_button.pack(side="left", padx=2)

underline_button = tk.Button(toolbar, text="Underline", command=lambda: toggle_tag("underline"))
underline_button.pack(side="left", padx=2)

# Create a Text widget for writing content
text = tk.Text(root, wrap="word", undo=True)
text.pack(expand=1, fill="both", padx=5, pady=5)

# Retrieve the default font from the Text widget for consistency
default_font = font.nametofont(text.cget("font"))

# Create modified fonts for each text style
bold_font = default_font.copy()
bold_font.configure(weight="bold")

italic_font = default_font.copy()
italic_font.configure(slant="italic")

underline_font = default_font.copy()
underline_font.configure(underline=1)

# Configure tags with the new font styles
text.tag_configure("bold", font=bold_font)
text.tag_configure("italic", font=italic_font)
text.tag_configure("underline", font=underline_font)

# Start the main application loop
root.mainloop()
