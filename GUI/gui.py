import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Attacks.ddos import simulate_ddos
from Attacks.forged_coupon import simulate_forged_coupon
from Utils.utils import validate_url

# DDoS window
def open_ddos_window(root):
    ddos_window = tk.Toplevel(root)
    ddos_window.title("DDoS Simulator")
    
    # GUI labels and text entries
    tk.Label(ddos_window, text="URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(ddos_window, width=30)
    url_entry.grid(row=0, column=1)

    tk.Label(ddos_window, text="Nb threads:").grid(row=1, column=0, sticky="e")
    threads_entry = tk.Entry(ddos_window, width=10)
    threads_entry.grid(row=1, column=1)

    tk.Label(ddos_window, text="Nb request by thread").grid(row=2, column=0, sticky="e")
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

            print("Starting DDoS attack...")
            simulate_ddos(url, num_threads, requests_per_thread)
            print("DDoS attack finished.")
            messagebox.showinfo("Finish", "End of DDoS attack.")
        except ValueError:
            messagebox.showerror("Erreur", "Enter a valid number.")

    start_button = tk.Button(ddos_window, text="Launch attack", command=start_ddos, bg="red", fg="white")
    start_button.grid(row=3, columnspan=2, pady=10)

# Forged Coupon window
def open_forged_coupon_window(root):
    coupon_window = tk.Toplevel(root)
    coupon_window.title("Forged Coupon Simulator")

    # GUI labels and text entries
    tk.Label(coupon_window, text="API URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(coupon_window, width=30)
    url_entry.grid(row=0, column=1)

    tk.Label(coupon_window, text="Base String:").grid(row=1, column=0, sticky="e")
    base_entry = tk.Entry(coupon_window, width=20)
    base_entry.grid(row=1, column=1)

    tk.Label(coupon_window, text="Secrets (comma-separated):").grid(row=2, column=0, sticky="e")
    secrets_entry = tk.Entry(coupon_window, width=30)
    secrets_entry.grid(row=2, column=1)

    def start_forged_coupon():
        url = url_entry.get()
        base_string = base_entry.get()
        secrets = secrets_entry.get().split(',')

        if not url or not base_string or not secrets:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        print("Starting Forged Coupon attack...")
        result = simulate_forged_coupon(url, base_string, secrets)

        if result:
            messagebox.showinfo("Success", f"Valid coupon found: {result}")
        else:
            messagebox.showwarning("Failed", "No valid coupon found.")

    start_button = tk.Button(coupon_window, text="Launch attack", command=start_forged_coupon, bg="red", fg="white")
    start_button.grid(row=3, columnspan=2, pady=10)

# Home page
def show_home_menu(root):
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Welcome to Automatic attacks simulator!", font=("Arial", 16)).pack(pady=10)
    tk.Button(main_frame, text="DDoS", command=lambda: open_ddos_window(root), width=20, bg="blue", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Forged Coupon", command=lambda: open_forged_coupon_window(root), width=20, bg="green", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Quit", command=root.quit, width=20, bg="red", fg="white").pack(pady=10)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Automatic Attacks Simulator")
    show_home_menu(root)
    root.mainloop()
