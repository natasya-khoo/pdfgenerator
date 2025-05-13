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
        self.network_var = tk.BooleanVar()

        checks = [
            ("Door Access", self.door_access_var),
            ("Infotech Account", self.infotech_var),
            ("SMILE Account", self.smile_var),
            ("PTS Account", self.pts_var),
            ("Email Account", self.email_var),
            ("Network Account", self.network_var)
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
        fullname      = self.fullname_entry.get().strip()
        com           = self.com_entry.get().strip()
        dept          = self.dept_entry.get().strip()
        designation   = self.designation_entry.get().strip()
        try:
            mobileno      = int(self.mobileno_entry.get().strip())
        except ValueError:
            mobileno = None
        dooraccess    = self.door_access_var.get()
        infotech      = self.infotech_var.get()
        smile         = self.smile_var.get()
        pts           = self.pts_var.get()
        email_acc     = self.email_var.get()
        network       = self.network_var.get()
        authorizer    = self.authorizer_entry.get().strip()
        signature     = self.auth_signature_entry.get().strip()
        auth_date     = self.auth_date_entry.get_date().isoformat()
        terminate_auth= self.terminate_authorizer_entry.get().strip()
        terminate_sig = self.terminate_signature_entry.get().strip()
        terminate_date= self.terminate_date_entry.get_date().isoformat()
        terminated_by = self.terminated_by_entry.get().strip()
        terminated_dt = self.terminated_date_entry.get_date().isoformat()

        # Build PDF fields
        pdf_fields = {
            "Full Name": fullname,
            "Company": com,
            "Dept": dept,
            "Designation": designation,
            "Mobile No": mobileno,
            "Door Access": dooraccess,
            "Infotech Account": infotech,
            "SMILE Account": smile,
            "PTS Account": pts,
            "Email Account": email_acc,
            "Network Account": network,
            "Authorizer": authorizer,
            "Auth Signature": signature,
            "Auth Date": auth_date,
            "Terminate Authorizer": terminate_auth,
            "Terminate Signature": terminate_sig,
            "Terminate Date": terminate_date,
            "Terminated By": terminated_by,
            "Terminated Date": terminated_dt
        }
        pdf_name = f"{fullname}.pdf"
        try:
            out_path = autosave_form_pdf("pdf_output", pdf_name, pdf_fields)
            messagebox.showinfo("Saved", f"PDF saved to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("PDF Error", f"Could not save PDF:\n{e}")

        try:
            conn = create_connection()
            cur  = conn.cursor()
            cur.execute(
                """
                INSERT INTO smbe.soitua
                (fullname, dept, mobileno, com, dooraccess, infotech, smile, pts, email, network,
                 authorizername, signature, date, designation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (fullname, dept, mobileno, com, dooraccess, infotech, smile, pts,
                 email_acc, network, authorizer, signature, auth_date, designation)
            )
            conn.commit()
            messagebox.showinfo("DB", "Data inserted successfully!")
        except Exception as error:
            messagebox.showerror("DB Error", f"Error while connecting to PostgreSQL:\n{error}")
        finally:
            if conn:
                cur.close()
                conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("User System Access Form")
    root.geometry("1100x900")
    UserSystemAccessForm(root, None).pack(fill="both", expand=True)
    root.mainloop()