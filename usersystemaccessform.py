import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Added for calendar widget
import psycopg2
from config import DB_CONFIG
import datetime

def create_connection():
    """Establish and return a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )


class UserSystemAccessForm(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # Title
        nav_frame = tk.Frame(self)
        nav_frame.pack(side="top", fill="x", padx=10, pady=5)
        tk.Label(nav_frame, text="User System Access Form", font=("Arial", 14, "bold")).pack(side="left", padx=10)

        # Scrollable canvas
        canvas = tk.Canvas(self, borderwidth=0)
        vsb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(canvas)
        canvas.create_window((4, 4), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Company Information
        comp_frame = ttk.LabelFrame(self.inner_frame, text="Company Information")
        comp_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(comp_frame, text="Company:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.com_entry = ttk.Entry(comp_frame, width=50)
        self.com_entry.grid(row=0, column=1, padx=5, pady=5)
        self.com_entry.insert(0, "Cantal Switchgear Pte Ltd")

        # Personal Particulars
        personal_frame = ttk.LabelFrame(self.inner_frame, text="(A) Personal Particulars")
        personal_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(personal_frame, text="Name in Full:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.fullname_entry = ttk.Entry(personal_frame, width=50)
        self.fullname_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(personal_frame, text="Dept:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        retrieve_btn = ttk.Button(personal_frame, text="Retrieve", command=self.retrieve_record)
        retrieve_btn.grid(row=0, column=2, padx=5)
        self.dept_entry = ttk.Entry(personal_frame, width=30)
        self.dept_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(personal_frame, text="Designation:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.designation_entry = ttk.Entry(personal_frame, width=30)
        self.designation_entry.grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(personal_frame, text="Mobile No:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.mobileno_entry = ttk.Entry(personal_frame, width=30)
        self.mobileno_entry.grid(row=2, column=1, padx=5, pady=5)

        # Staff Account Creation
        account_frame = ttk.LabelFrame(self.inner_frame, text="(B) Staff Account Creation")
        account_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.door_access_var = tk.BooleanVar()
        self.infotech_var = tk.BooleanVar()
        self.smile_var = tk.BooleanVar()
        self.pts_var = tk.BooleanVar()
        self.email_var = tk.BooleanVar()

        checks = [
            ("Door Access", self.door_access_var),
            ("Infotech Account", self.infotech_var),
            ("SMILE Account", self.smile_var),
            ("PTS Account", self.pts_var),
            ("Email Account", self.email_var),
        ]
        for i, (txt, var) in enumerate(checks):
            ttk.Checkbutton(account_frame, text=txt, variable=var).grid(row=i, column=0, sticky="w", padx=5, pady=2)

        auth_frame = ttk.LabelFrame(account_frame, text="Authorization")
        auth_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=10, sticky="ew")
        ttk.Label(auth_frame, text="Authorizer Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.authorizer_entry = ttk.Entry(auth_frame, width=50)
        self.authorizer_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(auth_frame, text="Signature:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.auth_signature_entry = ttk.Entry(auth_frame, width=20)
        self.auth_signature_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(auth_frame, text="Date:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.auth_date_entry = DateEntry(auth_frame, width=20, date_pattern='yyyy-mm-dd')
        self.auth_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Staff Termination Request
        termination_req_frame = ttk.LabelFrame(self.inner_frame, text="(D) Staff Termination Request")
        termination_req_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(termination_req_frame, text="Authorizer Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.terminate_authorizer_entry = ttk.Entry(termination_req_frame, width=30)
        self.terminate_authorizer_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(termination_req_frame, text="Signature:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.terminate_signature_entry = ttk.Entry(termination_req_frame, width=30)
        self.terminate_signature_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(termination_req_frame, text="Date:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.terminate_date_entry = DateEntry(termination_req_frame, width=20, date_pattern='yyyy-mm-dd')
        self.terminate_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # IT Dept Termination
        termination_it_frame = ttk.LabelFrame(self.inner_frame, text="(E) IT Dept Termination (IT Dept Only)")
        termination_it_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(termination_it_frame, text="Terminated By:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.terminated_by_entry = ttk.Entry(termination_it_frame, width=30)
        self.terminated_by_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(termination_it_frame, text="Date:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.terminated_date_entry = DateEntry(termination_it_frame, width=20, date_pattern='yyyy-mm-dd')
        self.terminated_date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Button
        submit_button = ttk.Button(self.inner_frame, text="Submit", command=self.submit_form)
        submit_button.grid(row=5, column=0, padx=10, pady=10)

    def submit_form(self):
        # Gather values
        fullname         = self.fullname_entry.get().strip()
        dept             = self.dept_entry.get().strip()
        designation      = self.designation_entry.get().strip()
        try:
            mobileno     = int(self.mobileno_entry.get().strip())
        except ValueError:
            mobileno     = None

        com              = self.com_entry.get().strip()       # maps to `com`
        company          = com                                # or use a separate entry if you add one

        dooraccess       = self.door_access_var.get()
        infotech         = self.infotech_var.get()
        smile            = self.smile_var.get()
        pts              = self.pts_var.get()
        email_acc        = self.email_var.get()

        # Authorization
        authorizer       = self.authorizer_entry.get().strip()
        signature        = self.auth_signature_entry.get().strip()
        auth_date        = self.auth_date_entry.get_date().isoformat()  # maps to `date`

        # Termination Request
        terminate_name      = self.terminate_authorizer_entry.get().strip()
        terminate_signature = self.terminate_signature_entry.get().strip()
        terminate_date      = self.terminate_date_entry.get_date().isoformat()

        # IT Dept Termination
        terminate_it        = self.terminated_by_entry.get().strip()
        it_date             = self.terminated_date_entry.get_date().isoformat()

        try:
            conn = create_connection()
            cur  = conn.cursor()
            cur.execute(
                """
                INSERT INTO smbe.soitua
                  (fullname,
                   dept,
                   mobileno,
                   com,
                   dooraccess,
                   infotech,
                   smile,
                   pts,
                   email,
                   authorizername,
                   signature,
                   date,
                   designation,
                   company,
                   terminate_name,
                   terminate_signature,
                   terminate_date,
                   terminate_it,
                   it_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (fullname,
                 dept,
                 mobileno,
                 com,
                 dooraccess,
                 infotech,
                 smile,
                 pts,
                 email_acc,
                 authorizer,
                 signature,
                 auth_date,
                 designation,
                 company,
                 terminate_name,
                 terminate_signature,
                 terminate_date,
                 terminate_it,
                 it_date)
            )
            conn.commit()
            messagebox.showinfo("DB", "Data inserted successfully!")
            self.reset_form()
        except Exception as error:
            messagebox.showerror("DB Error", f"Error while connecting to PostgreSQL:\n{error}")
        finally:
            if conn:
                cur.close()
                conn.close()
    
    def reset_form(self):
        # Text entries
        for entry in (
            self.com_entry,
            self.fullname_entry,
            self.dept_entry,
            self.designation_entry,
            self.mobileno_entry,
            self.authorizer_entry,
            self.auth_signature_entry,
            self.terminate_authorizer_entry,
            self.terminate_signature_entry,
            self.terminated_by_entry,
        ):
            entry.delete(0, tk.END)

        # Date pickers → reset to today
        today = datetime.date.today().isoformat()
        self.auth_date_entry.set_date(today)
        self.terminate_date_entry.set_date(today)
        self.terminated_date_entry.set_date(today)

        # Checkboxes → uncheck all
        for var in (
            self.door_access_var,
            self.infotech_var,
            self.smile_var,
            self.pts_var,
            self.email_var,
        ):
            var.set(False)

    def retrieve_record(self):
        name = self.fullname_entry.get().strip()
        if not name:
            messagebox.showwarning("Input needed", "Please enter a full name to retrieve.")
            return

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT
                  fullname, dept, mobileno, com,
                  dooraccess, infotech, smile, pts, email,
                  authorizername, signature, date, designation, company,
                  terminate_name, terminate_signature, terminate_date,
                  terminate_it, it_date
                FROM smbe.soitua
                WHERE fullname ILIKE %s
                LIMIT 1
            """, (f"%{name}%",))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if not row:
                messagebox.showinfo("No match", f"No record found for '{name}'.")
                return

            # unpack into distinct variables
            (
                fullname, dept, mobileno, com,
                dooraccess, infotech, smile, pts, email_acc,
                authorizer, signature, auth_date, designation, company,
                terminate_name, terminate_signature, terminate_date,
                terminate_it, it_date
            ) = row

            # populate all fields:
            self.fullname_entry.delete(0, tk.END)
            self.fullname_entry.insert(0, fullname)

            self.dept_entry.delete(0, tk.END)
            self.dept_entry.insert(0, dept)

            self.mobileno_entry.delete(0, tk.END)
            self.mobileno_entry.insert(0, str(mobileno) if mobileno is not None else "")

            self.com_entry.delete(0, tk.END)
            self.com_entry.insert(0, com)

            self.door_access_var.set(dooraccess)
            self.infotech_var.set(infotech)
            self.smile_var.set(smile)
            self.pts_var.set(pts)
            self.email_var.set(email_acc)

            self.authorizer_entry.delete(0, tk.END)
            self.authorizer_entry.insert(0, authorizer)

            self.auth_signature_entry.delete(0, tk.END)
            self.auth_signature_entry.insert(0, signature)

            self.auth_date_entry.set_date(auth_date)

            self.designation_entry.delete(0, tk.END)
            self.designation_entry.insert(0, designation)

            self.terminate_authorizer_entry.delete(0, tk.END)
            self.terminate_authorizer_entry.insert(0, terminate_name)

            self.terminate_signature_entry.delete(0, tk.END)
            self.terminate_signature_entry.insert(0, terminate_signature)

            self.terminate_date_entry.set_date(terminate_date)

            self.terminated_by_entry.delete(0, tk.END)
            self.terminated_by_entry.insert(0, terminate_it)

            self.terminated_date_entry.set_date(it_date)

        except Exception as e:
            messagebox.showerror("DB Error", f"Error retrieving record:\n{e}")






if __name__ == "__main__":
    root = tk.Tk()
    root.title("User System Access Form")
    root.geometry("1100x900")
    UserSystemAccessForm(root, None).pack(fill="both", expand=True)
    root.mainloop()