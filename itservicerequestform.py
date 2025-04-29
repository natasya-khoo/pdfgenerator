import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry 
import psycopg2
from config import DB_CONFIG
import tkinter.messagebox as messagebox

def create_connection():
    """Establish and return a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

class ITServiceRequestForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Top navigation
        nav_frame = tk.Frame(self)
        nav_frame.pack(side="top", fill="x", padx=10, pady=5)
        tk.Label(nav_frame, text="IT Service Request Form", font=("Arial", 14, "bold"))\
            .pack(side="left", padx=10)

        # ─── SCROLLABLE FORM CONTAINER ────────────────────────────────────────────
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.vsb    = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # create a window inside canvas, keep its ID to resize later
        self.form_frame = tk.Frame(self.canvas)
        self._win = self.canvas.create_window((0,0),
                                              window=self.form_frame,
                                              anchor="nw")

        # 1) update scrollregion when the inner frame grows
        self.form_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        # 2) stretch the inner window’s width to match the canvas’s width
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self._win, width=e.width)
        )

        # bind/unbind mousewheel on hover
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.form_frame.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.form_frame.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        # ─────────────────────────────────────────────────────────────────────────

        # (A) Basic Information
        basic = ttk.LabelFrame(self.form_frame, text="(A) Basic Information")
        basic.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(basic, text="Requestor Name:").grid(row=0, column=0, sticky="w")
        self.requestor_name_entry = ttk.Entry(basic, width=40)
        self.requestor_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(basic, text="Company:").grid(row=1, column=0, sticky="w")
        self.company_entry = ttk.Entry(basic, width=40)
        self.company_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(basic, text="Requested Date:").grid(row=2, column=0, sticky="w")
        self.requested_date_entry = DateEntry(basic, width=18, date_pattern='yyyy-mm-dd')
        self.requested_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(basic, text="Computer Name:").grid(row=3, column=0, sticky="w")
        self.computer_name_entry = ttk.Entry(basic, width=40)
        self.computer_name_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(basic, text="Priority:").grid(row=4, column=0, sticky="w")
        self.priority_combobox = ttk.Combobox(
            basic, values=["High","Normal","Low"], state="readonly", width=18
        )
        self.priority_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.priority_combobox.current(1)

        # (B) System & Network
        sysnet = ttk.LabelFrame(
            self.form_frame, text="(B) System & Network Maintenance Services"
        )
        sysnet.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.comp_purchases_var   = tk.BooleanVar()
        self.hardware_failure_var = tk.BooleanVar()
        self.user_access_var      = tk.BooleanVar()
        self.data_recovery_var    = tk.BooleanVar()
        self.pc_peripheral_var    = tk.BooleanVar()
        self.email_service_var    = tk.BooleanVar()
        self.antivirus_var        = tk.BooleanVar()
        self.other_it_var         = tk.BooleanVar()

        checks = [
            ("Computer Purchases (H/W & S/W)", self.comp_purchases_var),
            ("Hardware Failure/Damage",          self.hardware_failure_var),
            ("User Access Maintenance",          self.user_access_var),
            ("Data Recovery",                    self.data_recovery_var),
            ("PC & Peripheral",                  self.pc_peripheral_var),
            ("Email Service",                    self.email_service_var),
            ("Antivirus & Security",             self.antivirus_var),
            ("Other IT Services",                self.other_it_var),
        ]
        for i, (txt, var) in enumerate(checks):
            ttk.Checkbutton(sysnet, text=txt, variable=var)\
                .grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)

        # (C) Smile
        smile = ttk.LabelFrame(self.form_frame, text="(C) Smile Maintenance Services")
        smile.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.smile_system_var        = tk.BooleanVar()
        self.smile_new_module_var    = tk.BooleanVar()
        self.smile_troubleshoot_var  = tk.BooleanVar()
        self.smile_new_reports_var   = tk.BooleanVar()
        self.smile_other_var         = tk.BooleanVar()
        self.smile_report_custom_var = tk.BooleanVar()

        checks = [
            ("System & DB Maintenance", self.smile_system_var),
            ("New Module Creation",     self.smile_new_module_var),
            ("Troubleshooting",         self.smile_troubleshoot_var),
            ("New Reports",             self.smile_new_reports_var),
            ("Other Issues",            self.smile_other_var),
            ("Report Customization",    self.smile_report_custom_var),
        ]
        for i, (txt, var) in enumerate(checks):
            ttk.Checkbutton(smile, text=txt, variable=var)\
                .grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)

        # (D) PTS
        pts = ttk.LabelFrame(self.form_frame, text="(D) PTS Maintenance Services")
        pts.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.pts_system_var        = tk.BooleanVar()
        self.pts_new_module_var    = tk.BooleanVar()
        self.pts_troubleshoot_var  = tk.BooleanVar()
        self.pts_new_reports_var   = tk.BooleanVar()
        self.pts_other_var         = tk.BooleanVar()
        self.pts_report_custom_var = tk.BooleanVar()

        checks = [
            ("System & DB Maintenance", self.pts_system_var),
            ("New Module Creation",     self.pts_new_module_var),
            ("Troubleshooting",         self.pts_troubleshoot_var),
            ("New Reports",             self.pts_new_reports_var),
            ("Other Issues",            self.pts_other_var),
            ("Report Customization",    self.pts_report_custom_var),
        ]
        for i, (txt, var) in enumerate(checks):
            ttk.Checkbutton(pts, text=txt, variable=var)\
                .grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)

        # (E) Remarks
        remarks = ttk.LabelFrame(self.form_frame, text="(E) Other Requests / Software Needed")
        remarks.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.remarks_text = tk.Text(remarks, width=80, height=4)
        self.remarks_text.grid(row=0, column=0, padx=5, pady=5)

        # (F) IT Office Details
        office = ttk.LabelFrame(self.form_frame, text="(F) IT Office Details")
        office.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(office, text="Office Name:").grid(row=0, column=0, sticky="w")
        self.it_office_name_entry      = ttk.Entry(office, width=30)
        self.it_office_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(office, text="Signature:").grid(row=0, column=2, sticky="w")
        self.it_office_signature_entry = ttk.Entry(office, width=30)
        self.it_office_signature_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(office, text="Date:").grid(row=0, column=4, sticky="w")
        self.it_office_date_entry      = DateEntry(office, width=18, date_pattern='yyyy-mm-dd')
        self.it_office_date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.certified_completed_var   = tk.BooleanVar()
        self.to_be_followed_up_var     = tk.BooleanVar()
        ttk.Checkbutton(office, text="Certified Completed", variable=self.certified_completed_var)\
            .grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Checkbutton(office, text="To Be Followed-Up", variable=self.to_be_followed_up_var)\
            .grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # (G) Requestor Confirmation
        req = ttk.LabelFrame(self.form_frame, text="(G) Requestor Confirmation")
        req.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        self.requestor_signature_entry = ttk.Entry(req, width=60)
        self.requestor_signature_entry.grid(row=0, column=0, padx=5, pady=5)

        # (H) Official Use
        off = ttk.LabelFrame(self.form_frame, text="(H) Official Use")
        off.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(off, text="Verified by:").grid(row=0, column=0, sticky="w")
        self.verified_by_entry = ttk.Entry(off, width=30)
        self.verified_by_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(off, text="HOD Approval:").grid(row=0, column=2, sticky="w")
        self.hod_approval_entry = ttk.Entry(off, width=30)
        self.hod_approval_entry.grid(row=0, column=3, padx=5, pady=5)

        # Submit
        submit_btn = ttk.Button(self.form_frame, text="Submit", command=self.submit_form)
        submit_btn.grid(row=8, column=0, padx=10, pady=10)


    
    def submit_form(self):
        # build and execute your INSERT here...
        vals = [
            self.requestor_name_entry.get(),
            self.company_entry.get(),
            self.requested_date_entry.get(),
            self.computer_name_entry.get(),
            self.priority_combobox.get(),
            self.comp_purchases_var.get(),
            self.hardware_failure_var.get(),
            self.user_access_var.get(),
            self.data_recovery_var.get(),
            self.pc_peripheral_var.get(),
            self.email_service_var.get(),
            self.antivirus_var.get(),
            self.other_it_var.get(),
            self.smile_system_var.get(),
            self.smile_new_module_var.get(),
            self.smile_troubleshoot_var.get(),
            self.smile_new_reports_var.get(),
            self.smile_other_var.get(),
            self.smile_report_custom_var.get(),
            self.pts_system_var.get(),
            self.pts_new_module_var.get(),
            self.pts_troubleshoot_var.get(),
            self.pts_new_reports_var.get(),
            self.pts_other_var.get(),
            self.pts_report_custom_var.get(),
            self.remarks_text.get("1.0", tk.END).strip(),
            self.it_office_name_entry.get(),
            self.it_office_signature_entry.get(),
            self.it_office_date_entry.get(),
            self.certified_completed_var.get(),
            self.to_be_followed_up_var.get(),
            self.requestor_signature_entry.get(),
            self.verified_by_entry.get(),
            self.hod_approval_entry.get(),
        ]
        placeholders = ", ".join(["%s"] * len(vals))
        cols = ", ".join([
            "requestor_name", "company", "requested_date", "computer_name", "priority",
            "comp_purchases", "hardware_failure", "user_access", "data_recovery", "pc_peripheral",
            "email_service", "antivirus", "other_it",
            "smile_system", "smile_new_module", "smile_troubleshoot", "smile_new_reports",
            "smile_other", "smile_report_custom",
            "pts_system", "pts_new_module", "pts_troubleshoot", "pts_new_reports",
            "pts_other", "pts_report_custom",
            "remarks",
            "it_office_name", "it_office_signature", "it_office_date",
            "certified_completed", "to_be_followed_up",
            "requestor_signature", "verified_by", "hod_approval"
        ])
        query = f"INSERT INTO smbe.soitsr ({cols}) VALUES ({placeholders})"

        try:
            conn = create_connection()
            cur  = conn.cursor()
            cur.execute(query, vals)
            conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            print("Data inserted successfully!")
        except Exception as err:
            print("Error while connecting to PostgreSQL:", err)
            messagebox.showinfo("Error", "Failed to insert data into the database.", err)
        finally:
            if conn:
                cur.close()
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("IT Service Request Form")
    root.geometry("1100x900")
    ITServiceRequestForm(root, None).pack(fill="both", expand=True)
    root.mainloop()
