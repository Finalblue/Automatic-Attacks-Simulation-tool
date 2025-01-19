import tkinter as tk
from tkinter import messagebox
from ATTACKS.Attacks.AdminSectionAccess import AdminSectionAccess
from ATTACKS.Attacks.ExposeScoreBoard import ExposeScoreBoard
from ATTACKS.Attacks.ForgedFeedback import ForgedFeedback
from ATTACKS.Attacks.RetrieveOrders import RetrieveOrders
from Utils.utils import validate_url  # Validation d'URL

# Fenêtre pour Admin Section Access
def open_admin_section_window(root):
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Section Access")

    # Entrée de l'URL
    tk.Label(admin_window, text="Target URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(admin_window, width=30)
    url_entry.grid(row=0, column=1)

    # Bouton pour lancer l'attaque
    def start_admin_access():
        url = url_entry.get()
        if not validate_url(url):
            messagebox.showerror("Error", "Invalid URL format.")
            return

        attack = AdminSectionAccess(url)
        attack.run_exploit()
        messagebox.showinfo("Finished", "Admin Section Access completed.")

    start_button = tk.Button(admin_window, text="Launch Attack", command=start_admin_access, bg="red", fg="white")
    start_button.grid(row=2, columnspan=2, pady=10)

# Fenêtre pour Expose Score Board
def open_expose_score_board_window(root):
    expose_window = tk.Toplevel(root)
    expose_window.title("Expose Score Board")

    tk.Label(expose_window, text="Target URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(expose_window, width=30)
    url_entry.grid(row=0, column=1)

    def start_expose_score_board():
        url = url_entry.get()
        if not validate_url(url):
            messagebox.showerror("Error", "Invalid URL format.")
            return

        attack = ExposeScoreBoard(url)
        attack.run_exploit()
        messagebox.showinfo("Finished", "Expose Score Board completed.")

    start_button = tk.Button(expose_window, text="Launch Attack", command=start_expose_score_board, bg="red", fg="white")
    start_button.grid(row=2, columnspan=2, pady=10)

# Fenêtre pour Forged Feedback
def open_forged_feedback_window(root):
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Forged Feedback")

    tk.Label(feedback_window, text="Target URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(feedback_window, width=30)
    url_entry.grid(row=0, column=1)

    def start_forged_feedback():
        url = url_entry.get()
        if not validate_url(url):
            messagebox.showerror("Error", "Invalid URL format.")
            return

        attack = ForgedFeedback(url)
        attack.run_exploit()
        messagebox.showinfo("Finished", "Forged Feedback completed.")

    start_button = tk.Button(feedback_window, text="Launch Attack", command=start_forged_feedback, bg="red", fg="white")
    start_button.grid(row=2, columnspan=2, pady=10)

# Fenêtre pour Retrieve Orders
def open_retrieve_orders_window(root):
    orders_window = tk.Toplevel(root)
    orders_window.title("Retrieve Orders")

    tk.Label(orders_window, text="Target URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(orders_window, width=30)
    url_entry.grid(row=0, column=1)

    def start_retrieve_orders():
        url = url_entry.get()
        if not validate_url(url):
            messagebox.showerror("Error", "Invalid URL format.")
            return

        attack = RetrieveOrders(url)
        attack.run_exploit()
        messagebox.showinfo("Finished", "Retrieve Orders completed.")

    start_button = tk.Button(orders_window, text="Launch Attack", command=start_retrieve_orders, bg="red", fg="white")
    start_button.grid(row=2, columnspan=2, pady=10)

# Page d'accueil
def show_home_menu(root):
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Welcome to Automatic Attacks Simulator!", font=("Arial", 16)).pack(pady=10)

    tk.Button(main_frame, text="Admin Section Access", command=lambda: open_admin_section_window(root), width=20, bg="blue", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Expose Score Board", command=lambda: open_expose_score_board_window(root), width=20, bg="blue", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Forged Feedback", command=lambda: open_forged_feedback_window(root), width=20, bg="blue", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Retrieve Orders", command=lambda: open_retrieve_orders_window(root), width=20, bg="blue", fg="white").pack(pady=5)

    tk.Button(main_frame, text="Quit", command=root.quit, width=20, bg="red", fg="white").pack(pady=10)
