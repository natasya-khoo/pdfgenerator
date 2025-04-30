import tkinter as tk
from tkinter import ttk
import os
import sys
from notebookissueform import NotebookIssueForm
from itservicerequestform import ITServiceRequestForm
from usersystemaccessform import UserSystemAccessForm
from issue import IssueFormFrame
# add on other form for future usage here as well

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
selectionbar_color = '#eff5f6'
sidebar_color = '#F1FFFF'
visualisation_frame_color = "#ffffff"

def resource_path(relative_path):
    """
    Get absolute path to resource, works for development and for PyInstaller.
    """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# ------------------------------- ROOT WINDOW ----------------------------------
class TkinterApp(tk.Tk):
    """
    The class creates a sidebar for the application and creates submenus in the sidebar.
    It contains a multipage container where each page is a frame.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("IT Forms")

        # ------------- BASIC APP LAYOUT -----------------
        self.geometry("1100x900")
        self.resizable(1, 1)
        self.config(background=selectionbar_color)
        
        # Use resource_path to get the absolute path of favicon.png
        icon_path = resource_path("favicon.png")
        try:
            icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, icon)
        except Exception as e:
            print(f"Error loading icon from {icon_path}: {e}")

        # ---------------- SIDEBAR -----------------------
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # CANTAL LOGO
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        # Use a subsampled version of the icon for the logo
        try:
            self.logo = icon.subsample(18)
            logo = tk.Label(self.brand_frame, image=self.logo, bg=sidebar_color)
            logo.place(x=5, y=20)
        except Exception as e:
            print(f"Error setting up logo: {e}")

        # ---------------- SIDEBAR SUBMENU -----------------------
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.15, relwidth=0.7, relheight=0.85)
        submenu1 = SidebarSubMenu(self.submenu_frame,
                                  sub_menu_heading='IT Forms',
                                  sub_menu_options=["Notebook Issue Form",
                                                    "IT Service Request Form",
                                                    "User System Access Form",
                                                    "Submit New IT Ticket"
                                                   ]
                                 )
        submenu1.options["Notebook Issue Form"].config(
            command=lambda: self.show_frame(NotebookIssueForm)
        )
        submenu1.options["IT Service Request Form"].config(
            command=lambda: self.show_frame(ITServiceRequestForm)
        )
        submenu1.options["User System Access Form"].config(
            command=lambda: self.show_frame(UserSystemAccessForm)
        )
        submenu1.options["Submit New IT Ticket"].config(
            command=lambda: self.show_frame(IssueFormFrame)
        )
        submenu1.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------
        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.01, relwidth=0.7, relheight=0.99)

        self.frames = {}
        for F in (NotebookIssueForm, ITServiceRequestForm, UserSystemAccessForm, IssueFormFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(NotebookIssueForm)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# ------------------------ OTHER MULTIPAGE FRAMES ------------------------------------
class Frame2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='IT Service Request Form', font=("Arial", 15))
        label.pack(pady=20)


class Frame3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='User System Access Form', font=("Arial", 15))
        label.pack(pady=20)

class Frame4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='IT ticket', font=("Arial", 15))
        label.pack(pady=20)


# ----------------------------- CUSTOM WIDGETS ---------------------------------
class SidebarSubMenu(tk.Frame):
    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(
            self,
            text=sub_menu_heading,
            bg=sidebar_color,
            fg="#333333",
            font=("Arial", 10)
        )
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        """
        # calculate position of each button in the sidebar ,
        # n =1 (at pixel 45) , n=2 (at pixel 90) , n=3 (at pixel 135) and so on
        """
        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(
                self,
                text=x,
                bg=sidebar_color,
                font=("Arial", 9, "bold"),
                bd=0,
                cursor='hand2',
                activebackground='#ffffff',
            )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")
    

if __name__ == "__main__":
    app = TkinterApp()
    app.mainloop()
