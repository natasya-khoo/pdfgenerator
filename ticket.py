import tkinter as tk
from tkinter import ttk, messagebox

# A simple Ticket class to encapsulate ticket details.
class Ticket:
    def __init__(self, ticket_id, title, description, status="Open"):
        self.id = ticket_id
        self.title = title
        self.description = description
        self.status = status

# Global list to store tickets in memory.
tickets = []

class TicketFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Left Frame: List of tickets
        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text="Tickets", font=("Arial", 12, "bold")).pack(pady=5)
        self.ticket_listbox = tk.Listbox(left_frame, width=40)
        self.ticket_listbox.pack(fill="y", expand=True)
        self.ticket_listbox.bind("<<ListboxSelect>>", self.display_ticket_details)

        # Right Frame: Ticket details and ticket creation form
        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Ticket Details Area
        details_frame = ttk.LabelFrame(right_frame, text="Ticket Details")
        details_frame.pack(fill="both", expand=True)
        self.details_text = tk.Text(details_frame, wrap="word")
        self.details_text.pack(fill="both", expand=True, padx=5, pady=5)

        # New Ticket Creation Form
        form_frame = ttk.LabelFrame(right_frame, text="Create New Ticket")
        form_frame.pack(fill="x", pady=10, padx=5)

        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(form_frame, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.description_entry = ttk.Entry(form_frame, width=50)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Add Ticket", command=self.add_ticket)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_ticket(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()

        if not title:
            messagebox.showerror("Error", "Title cannot be empty.")
            return

        # Create a new ticket with a unique ID formatted as IT001, IT002, etc.
        ticket_id = "IT" + str(len(tickets) + 1).zfill(3)
        new_ticket = Ticket(ticket_id, title, description)
        tickets.append(new_ticket)

        # Update the ticket list
        self.ticket_listbox.insert("end", f"{new_ticket.id}: {new_ticket.title}")

        # Clear the input fields
        self.title_entry.delete(0, "end")
        self.description_entry.delete(0, "end")

    def display_ticket_details(self, event):
        selected_indices = self.ticket_listbox.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        ticket = tickets[index]
        # Display ticket details
        self.details_text.delete("1.0", "end")
        details = (
            f"Ticket ID: {ticket.id}\n"
            f"Title: {ticket.title}\n"
            f"Description: {ticket.description}\n"
            f"Status: {ticket.status}\n"
        )
        self.details_text.insert("end", details)

# For standalone testing, create a root window and embed the frame.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cantal IT Ticketing System")
    root.geometry("1100x900")
    frame = TicketFrame(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()
