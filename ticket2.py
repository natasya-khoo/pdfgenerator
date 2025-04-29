import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class ITTicketingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Ticketing System")
        self.root.geometry("1100x900")
        self.root.configure(bg="#f5f5f5")

        # --- TICKET TABLE (Top) ---
        self.tree = ttk.Treeview(root, columns=("ID", "Title", "Status", "Priority", "Date"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Date", text="Date")
        self.tree.column("ID", width=100)
        self.tree.column("Title", width=300)
        self.tree.column("Status", width=100)
        self.tree.column("Priority", width=100)
        self.tree.column("Date", width=100)
        self.tree.pack(pady=10, fill=tk.X, padx=20)
        self.tree.bind("<<TreeviewSelect>>", self.on_ticket_selected)

        # --- FILTER SECTION (Middle) ---
        filter_frame = tk.Frame(root, bg="#f5f5f5")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by ID:", bg="#f5f5f5").grid(row=0, column=0, padx=5)
        self.filter_id_entry = tk.Entry(filter_frame, width=15)
        self.filter_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Status:", bg="#f5f5f5").grid(row=0, column=2, padx=5)
        self.filter_status_cb = ttk.Combobox(filter_frame, values=["All", "Open", "In Progress", "Acknowledged", "Closed"], width=15)
        self.filter_status_cb.set("All")
        self.filter_status_cb.grid(row=0, column=3, padx=5)

        filter_button = tk.Button(filter_frame, text="Filter", command=self.apply_filter)
        filter_button.grid(row=0, column=4, padx=10)

        # --- DETAIL SECTION (Hidden by default) ---
        self.detail_frame = tk.LabelFrame(root, text="Ticket Details", bg="#f5f5f5")
        self.detail_frame.pack_forget()  # Start hidden

        self.detail_vars = {
            "ID": tk.StringVar(),
            "Title": tk.StringVar(),
            "Status": tk.StringVar(),
            "Priority": tk.StringVar(),
            "Date": tk.StringVar()
        }

        row = 0
        for key in self.detail_vars:
            tk.Label(self.detail_frame, text=f"{key}:", bg="#f5f5f5").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            if key == "Status":
                self.status_cb = ttk.Combobox(self.detail_frame, textvariable=self.detail_vars[key],
                                              values=["Open", "In Progress", "Acknowledged", "Closed"], width=20)
                self.status_cb.grid(row=row, column=1, sticky="w", padx=5)
            else:
                tk.Label(self.detail_frame, textvariable=self.detail_vars[key], bg="#f5f5f5").grid(row=row, column=1, sticky="w", padx=5)
            row += 1

        update_btn = tk.Button(self.detail_frame, text="Update Status", command=self.update_status)
        update_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # Load initial data
        self.load_tickets()

    def db_connect(self):
        return psycopg2.connect(
            host="172.16.30.120",
            dbname="CS",
            user="postgres",
            password="123456"
        )

    def load_tickets(self, filter_id=None, filter_status=None):
        self.tree.delete(*self.tree.get_children())
        try:
            conn = self.db_connect()
            cur = conn.cursor()

            query = """
                SELECT ticket_id, detail, status, priority, TO_CHAR(date, 'DD/MM/YYYY') AS diplay_date
                FROM smbe.ticket WHERE 1=1
            """
            params = []
            if filter_id:
                query += " AND ticket_id = %s"
                params.append(filter_id)
            if filter_status and filter_status != "All":
                query += " AND status = %s"
                params.append(filter_status)

            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)

            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading tickets: {e}")

    def apply_filter(self):
        filter_id = self.filter_id_entry.get().strip()
        filter_status = self.filter_status_cb.get()
        self.load_tickets(filter_id if filter_id else None, filter_status)

    def on_ticket_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        keys = list(self.detail_vars.keys())
        for i, key in enumerate(keys):
            self.detail_vars[key].set(values[i])
        self.detail_frame.pack(fill="x", padx=20, pady=10)  # Show detail section

    def update_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No ticket selected.")
            return

        ticket_id = self.detail_vars["ID"].get()
        new_status = self.status_cb.get()

        try:
            conn = self.db_connect()
            cur = conn.cursor()
            cur.execute("UPDATE smbe.ticket SET status = %s WHERE ticket_id = %s", (new_status, ticket_id))
            conn.commit()
            cur.close()
            conn.close()

            self.load_tickets()
            messagebox.showinfo("Success", f"Ticket {ticket_id.strip()} is {new_status}")

            if new_status.lower() == "closed":
                print(f"Sending closure email for ticket {ticket_id}")
                # TODO: Add email sending function

        except Exception as e:
            messagebox.showerror("Error", f"Error updating status: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ITTicketingSystem(root)
    root.mainloop()
