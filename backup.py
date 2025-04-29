import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import psycopg2
from config import DB_CONFIG
import tkinter.messagebox as messagebox
import datetime


def create_connection():
    """Establish and return a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )


class NotebookIssueForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        nav = tk.Frame(self)
        nav.pack(side="top", fill="x", padx=10, pady=5)
        ttk.Label(nav, text="Notebook Issue Form", font=("Arial", 14, "bold")).pack(side="left")

        # Scrollable canvas
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.form_frame = tk.Frame(self.canvas)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        frame_id = self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")

        self.form_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(frame_id, width=e.width))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self._build_form()
        self._configure_grid()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configure_grid(self):
        # Expand two columns
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=1)

    def _build_form(self):
        # Basic Information
        bf = ttk.LabelFrame(self.form_frame, text="Basic Information")
        bf.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        ttk.Label(bf, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = ttk.Entry(bf)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(bf, text="Asset ID:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.asset_id_entry = ttk.Entry(bf)
        self.asset_id_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(bf, text="Date of Issue:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.date_of_issue_entry = DateEntry(bf, date_pattern='yyyy-mm-dd')
        self.date_of_issue_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(bf, text="Brand/Model:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.brand_model_entry = ttk.Entry(bf)
        self.brand_model_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Issued Items
        issued = ttk.LabelFrame(self.form_frame, text="ISSUED ITEMS")
        issued.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.issued_notebook_var = tk.BooleanVar()
        self.issued_mouse_var = tk.BooleanVar()
        self.issued_power_cable_var = tk.BooleanVar()
        self.issued_power_supply_bag_var = tk.BooleanVar()
        ttk.Checkbutton(issued, text="Notebook", variable=self.issued_notebook_var).grid(row=0, column=0, padx=5, pady=2)
        ttk.Checkbutton(issued, text="Mouse", variable=self.issued_mouse_var).grid(row=0, column=1, padx=5, pady=2)
        ttk.Checkbutton(issued, text="Power Cable", variable=self.issued_power_cable_var).grid(row=1, column=0, padx=5, pady=2)
        ttk.Checkbutton(issued, text="Power Supply Bag", variable=self.issued_power_supply_bag_var).grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(issued, text="Remarks:").grid(row=2, column=0, sticky="ne", padx=5, pady=5)
        self.issued_remarks_text = tk.Text(issued, height=3)
        self.issued_remarks_text.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(issued, text="Issued Date:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.issued_date_entry = DateEntry(issued, date_pattern='yyyy-mm-dd')
        self.issued_date_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(issued, text="Received Date:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.received_date_entry = DateEntry(issued, date_pattern='yyyy-mm-dd')
        self.received_date_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(issued, text="Issued By:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.issued_by_entry = ttk.Entry(issued)
        self.issued_by_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(issued, text="Received By:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.received_by_entry = ttk.Entry(issued)
        self.received_by_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        # Returned Items
        returned = ttk.LabelFrame(self.form_frame, text="RETURNED ITEMS")
        returned.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.returned_notebook_var = tk.BooleanVar()
        self.returned_mouse_var = tk.BooleanVar()
        self.returned_power_cable_var = tk.BooleanVar()
        self.returned_power_supply_bag_var = tk.BooleanVar()
        ttk.Checkbutton(returned, text="Notebook", variable=self.returned_notebook_var).grid(row=0, column=0, padx=5, pady=2)
        ttk.Checkbutton(returned, text="Mouse", variable=self.returned_mouse_var).grid(row=0, column=1, padx=5, pady=2)
        ttk.Checkbutton(returned, text="Power Cable", variable=self.returned_power_cable_var).grid(row=1, column=0, padx=5, pady=2)
        ttk.Checkbutton(returned, text="Power Supply Bag", variable=self.returned_power_supply_bag_var).grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(returned, text="Remarks:").grid(row=2, column=0, sticky="ne", padx=5, pady=5)
        self.returned_remarks_text = tk.Text(returned, height=3)
        self.returned_remarks_text.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(returned, text="Returned Date:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.returned_date_entry = DateEntry(returned, date_pattern='yyyy-mm-dd')
        self.returned_date_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(returned, text="Verified Date:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.verified_date_entry = DateEntry(returned, date_pattern='yyyy-mm-dd')
        self.verified_date_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(returned, text="Returned By:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.returned_by_entry = ttk.Entry(returned)
        self.returned_by_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(returned, text="Verified By:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.verified_by_entry = ttk.Entry(returned)
        self.verified_by_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        # Submit button
        ttk.Button(self.form_frame, text="Submit", command=self.submit_form).grid(row=3, column=0, columnspan=2, pady=10)

    def submit_form(self):
        # gather all fields
        data = {
            'name': self.name_entry.get().strip(),
            'asset_id': self.asset_id_entry.get().strip(),
            'date_of_issue': self.date_of_issue_entry.get(),
            'brand_model': self.brand_model_entry.get().strip(),
            'issued_notebook': self.issued_notebook_var.get(),
            'issued_mouse': self.issued_mouse_var.get(),
            'issued_power_cable': self.issued_power_cable_var.get(),
            'issued_power_supply_bag': self.issued_power_supply_bag_var.get(),
            'issued_remarks': self.issued_remarks_text.get("1.0", tk.END).strip(),
            'issued_date': self.issued_date_entry.get(),
            'received_date': self.received_date_entry.get(),
            'issued_by': self.issued_by_entry.get().strip(),
            'received_by': self.received_by_entry.get().strip(),
            'returned_notebook': self.returned_notebook_var.get(),
            'returned_mouse': self.returned_mouse_var.get(),
            'returned_power_cable': self.returned_power_cable_var.get(),
            'returned_power_supply_bag': self.returned_power_supply_bag_var.get(),
            'returned_remarks': self.returned_remarks_text.get("1.0", tk.END).strip(),
            'returned_date': self.returned_date_entry.get(),
            'verified_date': self.verified_date_entry.get(),
            'returned_by': self.returned_by_entry.get().strip(),
            'verified_by': self.verified_by_entry.get().strip(),
        }
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO smbe.soitni (
                    name, asset_id, date_of_issue, brand_model,
                    issued_notebook, issued_mouse, issued_power_cable, issued_power_supply_bag,
                    issued_remarks, issued_date, received_date, issued_by, received_by,
                    returned_notebook, returned_mouse, returned_power_cable, returned_power_supply_bag,
                    returned_remarks, returned_date, verified_date, returned_by, verified_by
                ) VALUES (%(name)s, %(asset_id)s, %(date_of_issue)s, %(brand_model)s,
                          %(issued_notebook)s, %(issued_mouse)s, %(issued_power_cable)s, %(issued_power_supply_bag)s,
                          %(issued_remarks)s, %(issued_date)s, %(received_date)s, %(issued_by)s, %(received_by)s,
                          %(returned_notebook)s, %(returned_mouse)s, %(returned_power_cable)s, %(returned_power_supply_bag)s,
                          %(returned_remarks)s, %(returned_date)s, %(verified_date)s, %(returned_by)s, %(verified_by)s
                )
                RETURNING *;
                """, data
            )
            inserted = cur.fetchone()
            conn.commit()
            messagebox.showinfo("Success", f"Record inserted: {inserted}")
            self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            cur.close()
            conn.close()

    def reset_form(self):
        # clear all inputs
        self.name_entry.delete(0, tk.END)
        self.asset_id_entry.delete(0, tk.END)
        self.date_of_issue_entry.set_date(datetime.date.today())
        self.brand_model_entry.delete(0, tk.END)
        for var in [self.issued_notebook_var, self.issued_mouse_var,
                    self.issued_power_cable_var, self.issued_power_supply_bag_var]:
            var.set(False)
        self.issued_remarks_text.delete("1.0", tk.END)
        self.issued_date_entry.set_date(datetime.date.today())
        self.received_date_entry.set_date(datetime.date.today())
        self.issued_by_entry.delete(0, tk.END)
        self.received_by_entry.delete(0, tk.END)
        for var in [self.returned_notebook_var, self.returned_mouse_var,
                    self.returned_power_cable_var, self.returned_power_supply_bag_var]:
            var.set(False)
        self.returned_remarks_text.delete("1.0", tk.END)
        self.returned_date_entry.set_date(datetime.date.today())
        self.verified_date_entry.set_date(datetime.date.today())
        self.returned_by_entry.delete(0, tk.END)
        self.verified_by_entry.delete(0, tk.END)


# standalone test
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Notebook Issue Form")
    root.geometry("1100x900")
    NotebookIssueForm(root, None).pack(fill="both", expand=True)
    root.mainloop()
