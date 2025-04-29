import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import psycopg2
from config import DB_CONFIG
import tkinter.messagebox as messagebox


def create_connection():
    """Establish and return a connection to the PostgreSQL database."""
    connection = psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    return connection


class NotebookIssueForm(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the Notebook Issue Form frame.

        Parameters:
            parent (tk.Widget): The parent container.
            controller (object): The controller (e.g. main application) used for navigation.
        """
        super().__init__(parent)
        self.controller = controller

        # ------------------ Title Label in the navigation bar ------------------
        nav_frame = tk.Frame(self)
        nav_frame.pack(side="top", fill="x", padx=10, pady=5)
        nav_title = tk.Label(nav_frame, text="Notebook Issue Form", font=("Arial", 14, "bold"))
        nav_title.pack(side="left", padx=10)

        # ------------------ Canvas and Scrollbar for Form ------------------
        canvas = tk.Canvas(self, borderwidth=0)
        form_frame = tk.Frame(canvas)
        vsb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # create_window returns an ID for resizing
        canvas_frame_id = canvas.create_window((0, 0), window=form_frame, anchor="nw")

        # 1) Update scrollregion when the interior frame changes size
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        form_frame.bind("<Configure>", on_frame_configure)

        # 2) Make the interior frame always as wide as the canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_frame_id, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)

        # 3) Scoped mouse-wheel binding to prevent Notebook from grabbing events
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        canvas.bind("<Enter>", _bind_to_mousewheel)
        canvas.bind("<Leave>", _unbind_from_mousewheel)

        # ------------------ Group 1: Basic Information ------------------
        basic_frame = ttk.LabelFrame(form_frame, text="Basic Information")
        basic_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(basic_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(basic_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(basic_frame, text="Asset ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.asset_id_entry = ttk.Entry(basic_frame, width=30)
        self.asset_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(basic_frame, text="Date of Issue (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.date_of_issue_entry = DateEntry(
            basic_frame, width=20, background='darkblue',
            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd'
        )
        self.date_of_issue_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(basic_frame, text="Brand/Model:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.brand_model_entry = ttk.Entry(basic_frame, width=40)
        self.brand_model_entry.grid(row=3, column=1, padx=5, pady=5)

        # ------------------ Group 2: Issued Items ------------------
        issued_frame = ttk.LabelFrame(form_frame, text="ISSUED ITEMS")
        issued_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.issued_notebook_var = tk.BooleanVar()
        self.issued_mouse_var = tk.BooleanVar()
        self.issued_power_cable_var = tk.BooleanVar()
        self.issued_power_supply_bag_var = tk.BooleanVar()

        ttk.Checkbutton(
            issued_frame, text="Notebook", variable=self.issued_notebook_var
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(
            issued_frame, text="Mouse", variable=self.issued_mouse_var
        ).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(
            issued_frame, text="Power Cable", variable=self.issued_power_cable_var
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(
            issued_frame, text="Power Supply Bag", variable=self.issued_power_supply_bag_var
        ).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(issued_frame, text="Remarks:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.issued_remarks_text = tk.Text(issued_frame, width=60, height=3)
        self.issued_remarks_text.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(issued_frame, text="Issued Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.issued_date_entry = DateEntry(
            issued_frame, width=20, background='darkblue',
            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd'
        )
        self.issued_date_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(issued_frame, text="Received Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.received_date_entry = DateEntry(
            issued_frame, width=20, background='darkblue',
            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd'
        )
        self.received_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(issued_frame, text="Issued By (IT/HR Dept):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.issued_by_entry = ttk.Entry(issued_frame, width=30)
        self.issued_by_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(issued_frame, text="Received By:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.received_by_entry = ttk.Entry(issued_frame, width=30)
        self.received_by_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(issued_frame, text="Issued Signature:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.issued_signature_entry = ttk.Entry(issued_frame, width=30)
        self.issued_signature_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(issued_frame, text="Received Signature:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.received_signature_entry = ttk.Entry(issued_frame, width=30)
        self.received_signature_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")


        # ------------------ Group 3: Returned Items ------------------
        returned_frame = ttk.LabelFrame(form_frame, text="RETURNED ITEMS")
        returned_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.returned_notebook_var = tk.BooleanVar()
        self.returned_mouse_var = tk.BooleanVar()
        self.returned_power_cable_var = tk.BooleanVar()
        self.returned_power_supply_bag_var = tk.BooleanVar()

        ttk.Checkbutton(returned_frame, text="Notebook", variable=self.returned_notebook_var)\
            .grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(returned_frame, text="Mouse", variable=self.returned_mouse_var)\
            .grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(returned_frame, text="Power Cable", variable=self.returned_power_cable_var)\
            .grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(returned_frame, text="Power Supply Bag", variable=self.returned_power_supply_bag_var)\
            .grid(row=1, column=1, sticky="w", padx=5, pady=2)
    
        ttk.Label(returned_frame, text="Remarks:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.returned_remarks_text = tk.Text(returned_frame, width=60, height=3)
        self.returned_remarks_text.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(returned_frame, text="Returned Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.returned_date_entry = DateEntry(returned_frame, width=20, background='darkblue',
                                             foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.returned_date_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(returned_frame, text="Verified Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.verified_date_entry = DateEntry(returned_frame, width=20, background='darkblue',
                                             foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.verified_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(returned_frame, text="Returned By:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.returned_by_entry = ttk.Entry(returned_frame, width=30)
        self.returned_by_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(returned_frame, text="Verified By (IT/HR Dept):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.verified_by_entry = ttk.Entry(returned_frame, width=30)
        self.verified_by_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(returned_frame, text="Returned Signature:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.returned_signature_entry = ttk.Entry(returned_frame, width=30)
        self.returned_signature_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(returned_frame, text="Verified Signature:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.verified_signature_entry = ttk.Entry(returned_frame, width=30)
        self.verified_signature_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # ------------------ Submit Button ------------------
        submit_button = ttk.Button(form_frame, text="Submit", command=self.submit_form)
        submit_button.grid(row=3, column=0, padx=10, pady=10)

    def submit_form(self):
        """
        Collect data from the form fields and insert it into the database.
        """
        # Retrieve Basic Information
        name = self.name_entry.get()
        asset_id = self.asset_id_entry.get()
        date_of_issue = self.date_of_issue_entry.get()  # format 'YYYY-MM-DD'
        brand_model = self.brand_model_entry.get()

        # Retrieve Issued Items Data
        issued_notebook = self.issued_notebook_var.get()
        issued_mouse = self.issued_mouse_var.get()
        issued_power_cable = self.issued_power_cable_var.get()
        issued_power_supply_bag = self.issued_power_supply_bag_var.get()
        issued_remarks = self.issued_remarks_text.get("1.0", tk.END).strip()
        issued_date = self.issued_date_entry.get()      
        received_date = self.received_date_entry.get()    
        issued_by = self.issued_by_entry.get()            
        received_by = self.received_by_entry.get()
        issued_signature = self.issued_signature_entry.get()
        received_signature = self.received_signature_entry.get()

        # Retrieve Returned Items Data
        returned_notebook = self.returned_notebook_var.get()
        returned_mouse = self.returned_mouse_var.get()
        returned_power_cable = self.returned_power_cable_var.get()
        returned_power_supply_bag = self.returned_power_supply_bag_var.get()
        returned_remarks = self.returned_remarks_text.get("1.0", tk.END).strip()
        returned_date = self.returned_date_entry.get()
        verified_date = self.verified_date_entry.get()
        returned_by = self.returned_by_entry.get()
        verified_by = self.verified_by_entry.get()        
        returned_signature = self.returned_signature_entry.get()
        verified_signature = self.verified_signature_entry.get()

        try:
            connection = create_connection()
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO smbe.soitni
                (name, asset_id, date_of_issue, brand_model,
                 issued_notebook, issued_mouse, issued_power_cable, issued_power_supply_bag,
                 issued_remarks, issued_date, received_date, issued_by, received_by, issued_signature, received_signature,
                 returned_notebook, returned_mouse, returned_power_cable, returned_power_supply_bag,
                 returned_remarks, returned_date, verified_date, returned_by, verified_by, returned_signature, verified_signature)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """
            cursor.execute(insert_query, (
                name, asset_id, date_of_issue, brand_model,
                issued_notebook, issued_mouse, issued_power_cable, issued_power_supply_bag,
                issued_remarks, issued_date, received_date, issued_by, received_by, issued_signature, received_signature,
                returned_notebook, returned_mouse, returned_power_cable, returned_power_supply_bag,
                returned_remarks, returned_date, verified_date, returned_by, verified_by, returned_signature, verified_signature
            ))
            inserted_row = cursor.fetchone()
            connection.commit()
            print("Data inserted successfully!")
            messagebox.showinfo("Success", "Data inserted successfully!")
            print("Inserted row:", inserted_row)
        except Exception as error:
            print("Error while connecting to PostgreSQL:", error)
            messagebox.showerror("Error", f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

# For testing the frame independently:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Notebook Issue Form")
    root.geometry("1100x900")
    app = NotebookIssueForm(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()