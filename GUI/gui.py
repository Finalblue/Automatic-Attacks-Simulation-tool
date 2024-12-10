import tkinter as tk
from tkinter import messagebox
from Attacks.ddos import simulate_ddos
from Utils.utils import validate_url
from Attacks.sql_injection import simulate_sql_injection


#DDOS window
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

    #OnClick Start button, just a dummy prompt, for exemple
    #TODO Implement the DDoS attack later
    #TODO Add a report of the attack
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


# Add here other windows for other attacks

def open_sql_injection_window(root):
    sql_window = tk.Toplevel(root)
    sql_window.title("SQL Injection Simulator")
    
    tk.Label(sql_window, text="URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(sql_window, width=30)
    url_entry.grid(row=0, column=1)

    tk.Label(sql_window, text="Payload SQL:").grid(row=1, column=0, sticky="e")
    payload_entry = tk.Entry(sql_window, width=30)
    payload_entry.grid(row=1, column=1)

    def start_sql_injection():
        url = url_entry.get()
        payload = payload_entry.get()

        if not validate_url(url):
            messagebox.showerror("Erreur", "URL invalide.")
            return
        
        simulate_sql_injection(url, payload)

    start_button = tk.Button(sql_window, text="Lancer l'attaque", command=start_sql_injection, bg="red", fg="white")
    start_button.grid(row=2, columnspan=2, pady=10)


# Home page
def show_home_menu(root):
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Welcome to Automatic attacks simulator !", font=("Arial", 16)).pack(pady=10)
    tk.Button(main_frame, text="DDoS", command=lambda: open_ddos_window(root), width=20, bg="blue", fg="white").pack(pady=5)
    # Add here button for other attacks windows
    tk.Button(main_frame, text="Other attack", state=tk.DISABLED, width=20).pack(pady=5)
    tk.Button(main_frame, text="Quitter", command=root.quit, width=20, bg="red", fg="white").pack(pady=10)
    tk.Button(main_frame, text="SQL Injection", command=lambda: open_sql_injection_window(root), bg="blue", fg="white").pack(pady=5)
