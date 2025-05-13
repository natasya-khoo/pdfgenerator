import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
import smtplib
from email.message import EmailMessage
from config import DB_CONFIG
import datetime
import threading

def create_connection():
    """Establish and return a connection to the PostgreSQL database."""
    connection = psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    return connection

class IssueFormFrame(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        # Remove unwanted options (e.g., 'menu')
        kwargs.pop('menu', None)
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.attachment_path = ""  # Holds file path for the optional attachment

        # Initialize category_var early so it's available when generating the ticket number.
        self.category_var = tk.StringVar(value="Software")
        # Generate the base part of the ticket number (year + running number) once.
        self.generated_ticket_base = self.generate_ticket_base()

        # Create a canvas with a vertical scrollbar for scrollable form content
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.form_frame = tk.Frame(self.canvas)
        vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.form_frame, anchor="nw")
        self.form_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/100)), "units"))

        self.create_widgets()
        self.configure_grid()

    def configure_grid(self):
        # Increase vertical spacing between rows
        for i in range(9):
            self.form_frame.rowconfigure(i, pad=10)
        self.form_frame.columnconfigure(1, weight=1)

    def open_ticket_view(self):
        import ticket2  # Make sure ticket2.py is in your PYTHONPATH or same directory.
        ticket_window = tk.Toplevel(self)
        ticket_window.title("IT Ticketing System")
        ticket_window.geometry("1100x900")
        ticket_app = ticket2.ITTicketingSystem(ticket_window)


    def create_widgets(self):
        # --- Ticket Number ---
        # Display the full ticket number: base + suffix (e.g., "25001SW" or "25001HW").
        self.ticket_label = ttk.Label(
            self.form_frame,
            text=self.generate_ticket_number(),
            font=("Arial", 15, "bold")
        )
        self.ticket_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        # --- Basic Information Group ---
        basic_frame = ttk.LabelFrame(self.form_frame, text="Basic Information")
        basic_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        ttk.Label(basic_frame, text="Name:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(basic_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(basic_frame, text="Department:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.department_entry = ttk.Entry(basic_frame, width=40)
        self.department_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # --- Issue Information Group ---
        issue_frame = ttk.LabelFrame(self.form_frame, text="Issue Information")
        issue_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        # Issue Category
        ttk.Label(issue_frame, text="Issue Category:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        cat_frame = ttk.Frame(issue_frame)
        cat_frame.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # Radio buttons will call update_details() when clicked.
        hw_rb = ttk.Radiobutton(cat_frame, text="Hardware", variable=self.category_var, value="Hardware", command=self.update_details)
        sw_rb = ttk.Radiobutton(cat_frame, text="Software", variable=self.category_var, value="Software", command=self.update_details)
        hw_rb.pack(side="left", padx=5)
        sw_rb.pack(side="left", padx=5)

        # Issue Detail
        ttk.Label(issue_frame, text="Issue Detail:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.detail_cb = ttk.Combobox(issue_frame, state="readonly", width=37)
        self.detail_cb.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Priority Section
        ttk.Label(issue_frame, text="Priority:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Low")
        priority_frame = ttk.Frame(issue_frame)
        priority_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        rb_high = ttk.Radiobutton(priority_frame, text="High", variable=self.priority_var, value="High")
        rb_medium = ttk.Radiobutton(priority_frame, text="Medium", variable=self.priority_var, value="Medium")
        rb_low = ttk.Radiobutton(priority_frame, text="Low", variable=self.priority_var, value="Low")
        rb_high.pack(side="left", padx=5)
        rb_medium.pack(side="left", padx=5)
        rb_low.pack(side="left", padx=5)
        
        # Summary
        ttk.Label(issue_frame, text="Summary:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.summary_entry = ttk.Entry(issue_frame, width=40)
        self.summary_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        # Description
        ttk.Label(issue_frame, text="Description:", font=("Arial", 10)).grid(row=4, column=0, sticky="nw", padx=5, pady=5)
        self.description_text = tk.Text(issue_frame, width=40, height=5)
        self.description_text.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        # Attachment (Optional)
        ttk.Label(issue_frame, text="Attachment (optional):", font=("Arial", 10)).grid(row=5, column=0, sticky="w", padx=5, pady=5)
        attach_frame = ttk.Frame(issue_frame)
        attach_frame.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.attachment_label = ttk.Label(attach_frame, text="No file selected", width=30)
        self.attachment_label.pack(side="left", padx=5)
        attach_btn = ttk.Button(attach_frame, text="Browse", command=self.browse_attachment)
        attach_btn.pack(side="left", padx=5)

         # --- Submit Button ---

        # Frame to center the buttons
        button_container = tk.Frame(self.form_frame)
        button_container.grid(row=3, column=0, columnspan=2, pady=20)

        # Submit Button
        submit_btn = tk.Button(button_container, text="Submit", command=self.submit_form)
        submit_btn.pack(side="left", padx=10)

        # Check Button
        check_btn = tk.Button(button_container, text="Check Open Ticket", command=self.open_ticket_view)
        check_btn.pack(side="left", padx=10)

    def generate_ticket_base(self):
        """Generate the base ticket number (year + running number) from the database."""
        connection = None
        try:
            year = datetime.datetime.now().year % 100  # e.g., 2025 -> 25
            connection = create_connection()
            cursor = connection.cursor()
            like_pattern = f"{year:02d}%"
            query = "SELECT MAX(ticket_id) FROM smbe.ticket WHERE ticket_id LIKE %s;"
            cursor.execute(query, (like_pattern,))
            result = cursor.fetchone()[0]
            if result is None:
                running_number = 1
            else:
                # Running number is extracted from index 2 to 5 (e.g., "25001HW" → "001")
                running_number = int(result[2:5]) + 1
            # Return base without the suffix (e.g., "25001")
            return f"{year:02d}{str(running_number).zfill(3)}"
        except Exception as e:
            messagebox.showerror("Error", f"Error generating ticket number: {e}")
            return f"{year:02d}001"
        finally:
            if connection:
                cursor.close()
                connection.close()

    def generate_ticket_number(self):

        """Append the correct suffix (SW/HW) to the pre-generated ticket base."""
        category = self.category_var.get() if self.category_var.get() else "Software"
        suffix = "HW" if category.lower() == "hardware" else "SW"
        return f"Ticket Number : " + self.generated_ticket_base + suffix

    def update_details(self):
        category = self.category_var.get()
        if category == "Hardware":
            details = ["Plotter", "Printer", "Laptop", "Desktop", "Keyboard", "Mouse", "Cable", "Others"]
        elif category == "Software":
            details = ["Printer issue", "Server system (SMILE, CSPTS)", "Software (SOLIDWORKS, ARESCAD)", "License", "One Drive/Share Drive", "Others"]
        else:
            details = []
        self.detail_cb['values'] = details
        if details:
            self.detail_cb.current(0)
        else:
            self.detail_cb.set("")
        # Update the ticket number label based on the newly selected category.
        self.ticket_label.config(text = self.generate_ticket_number())

    def browse_attachment(self):
        filepath = filedialog.askopenfilename(title="Select Attachment")
        if filepath:
            self.attachment_path = filepath
            self.attachment_label.config(text=filepath.split("/")[-1])
        else:
            self.attachment_path = ""
            self.attachment_label.config(text="No file selected")

    def send_notification_email(self, ticket_no, name, department, category, detail, priority, summary, description):
        try:
            msg = EmailMessage()
            msg['Subject'] = f"New IT Ticket: {ticket_no}"
            msg['From'] = "itteam764@gmail.com"
            msg['To'] = "IT_Test@cantalelectric.com"
            body = f"""A new IT ticket has been submitted.

Ticket Number: {ticket_no}
Name: {name}
Department: {department}
Category: {category}
Detail: {detail}
Priority: {priority}
Summary: {summary}
Description: {description}
"""
            msg.set_content(body)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "itteam764@gmail.com"
            smtp_password = "ayeh lybl qhfy zmca"

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                all_recipients = msg.get_all('To', []) + msg.get_all('Cc', [])
                server.send_message(msg, from_addr=msg['From'], to_addrs=all_recipients)
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send notification email: {e}")

    def submit_form(self):
        # Gather data from the form.
        ticket_no   = self.ticket_label.cget("text").split(":")[-1].strip()
        name        = self.name_entry.get().strip()
        department  = self.department_entry.get().strip()
        category    = self.category_var.get().strip()
        detail      = self.detail_cb.get().strip()
        priority    = self.priority_var.get().strip()
        summary     = self.summary_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        attachment  = self.attachment_path
        status      = "Open"
        date        = datetime.datetime.now().strftime("%Y-%m-%d")

        # Validate required fields.
        if not all([name, department, category, detail, priority, summary, description]):
            messagebox.showerror("Error", "Please complete all required fields.")
            return

        connection = None
        try:
            connection = create_connection()
            cursor     = connection.cursor()
            insert_query = """
                INSERT INTO smbe.ticket 
                (ticket_id, name, department, category, detail, priority, summary, description, attachment, status, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING ticket_id;
            """
            cursor.execute(insert_query, (
                ticket_no, name, department, category, detail,
                priority, summary, description, attachment,
                status, date
            ))
            returned_ticket = cursor.fetchone()[0]
            returned_ticket = returned_ticket.strip() 
            connection.commit()

            messagebox.showinfo("Success", f"Ticket {returned_ticket} submitted successfully!")

            self.reset_form()


            threading.Thread(
                target=self.send_notification_email,
                args=(
                    returned_ticket, name, department,
                    category, detail, priority,
                    summary, description
                ),
                daemon=True
            ).start()

        except Exception as error:
            messagebox.showerror("Database Error", f"Error while inserting data: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()


    def reset_form(self):
        # Create a new ticket base and update the ticket label.
        self.generated_ticket_base = self.generate_ticket_base()
        self.ticket_label.config(text=self.generate_ticket_number())
        self.name_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        self.category_var.set("Software")
        self.detail_cb.set("")
        self.detail_cb['values'] = []
        self.priority_var.set("Low")
        self.summary_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        self.attachment_path = ""
        self.attachment_label.config(text="No file selected")

# For testing and standalone usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("IT Ticketing System")
    root.geometry("1100x900")
    frame = IssueFormFrame(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()
