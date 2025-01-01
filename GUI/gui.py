import os
import sys
import tkinter as tk
from tkinter import messagebox

# Ajouter le dossier du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Attacks.ddos import simulate_ddos
from Attacks.couponattack import run_generic_coupon_attack
from Utils.utils import validate_url

# Fenêtre pour l'attaque DDoS
def open_ddos_window(root):
    ddos_window = tk.Toplevel(root)
    ddos_window.title("DDoS Simulator")
    
    tk.Label(ddos_window, text="URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(ddos_window, width=30)
    url_entry.grid(row=0, column=1)

    tk.Label(ddos_window, text="Number of Threads:").grid(row=1, column=0, sticky="e")
    threads_entry = tk.Entry(ddos_window, width=10)
    threads_entry.grid(row=1, column=1)

    tk.Label(ddos_window, text="Requests per Thread:").grid(row=2, column=0, sticky="e")
    requests_entry = tk.Entry(ddos_window, width=10)
    requests_entry.grid(row=2, column=1)

    def start_ddos():
        url = url_entry.get()
        try:
            num_threads = int(threads_entry.get())
            requests_per_thread = int(requests_entry.get())

            if not validate_url(url):
                messagebox.showerror("Error", "Invalid URL format.")
                return

            simulate_ddos(url, num_threads, requests_per_thread)
            messagebox.showinfo("Success", "DDoS attack simulation finished.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values.")

    tk.Button(ddos_window, text="Launch Attack", command=start_ddos, bg="red", fg="white").grid(row=3, columnspan=2, pady=10)

# Fenêtre pour l'attaque de Coupon Generic
def open_generic_coupon_window(root):
    coupon_window = tk.Toplevel(root)
    coupon_window.title("Generic Coupon Attack")

    tk.Label(coupon_window, text="Target URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(coupon_window, width=30)
    url_entry.grid(row=0, column=1)

    tk.Label(coupon_window, text="Discount Percentage (e.g., 80):").grid(row=1, column=0, sticky="e")
    discount_entry = tk.Entry(coupon_window, width=10)
    discount_entry.grid(row=1, column=1)

    def start_coupon_attack():
        url = url_entry.get()
        try:
            discount = int(discount_entry.get())
            if not validate_url(url):
                messagebox.showerror("Error", "Invalid URL format.")
                return

            run_generic_coupon_attack(url, discount)
            messagebox.showinfo("Success", "Coupon attack simulation finished.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric discount value.")

    tk.Button(coupon_window, text="Launch Attack", command=start_coupon_attack, bg="green", fg="white").grid(row=2, columnspan=2, pady=10)

# Accueil
def show_home_menu(root):
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Welcome to Automatic Attacks Simulator!", font=("Arial", 16)).pack(pady=10)

    tk.Button(main_frame, text="DDoS Attack", command=lambda: open_ddos_window(root), width=20, bg="blue", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Generic Coupon Attack", command=lambda: open_generic_coupon_window(root), width=20, bg="green", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Quit", command=root.quit, width=20, bg="red", fg="white").pack(pady=10)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Automatic Attacks Simulator")
    show_home_menu(root)
    root.mainloop()
