import tkinter as tk
from tkinter import ttk, messagebox
from GUI.AttackManager import AttackManager
from threading import Thread

class PentestGUI:
    def __init__(self, attack_manager: AttackManager):
        self.attack_manager = attack_manager
        self.root = tk.Tk()
        self.root.title("Pentest Tool")
        self.root.geometry("1000x600")  # Adjusted size for logs

        self._create_main_layout()
        self._create_url_frame()
        self._create_attacks_frame()
        self._create_logs_frame()

    def _create_main_layout(self):
        """Create the main layout with a PanedWindow to separate buttons and logs."""
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame for buttons
        self.left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, weight=3)

        # Right frame for logs
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, weight=2)

    def _create_url_frame(self):
        url_frame = ttk.LabelFrame(self.left_frame, text="Target Configuration", padding=10)
        url_frame.pack(pady=10, padx=10, fill=tk.X)
        ttk.Label(url_frame, text="Target URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.url_entry.insert(tk.END, "http://45.76.47.218:3000")

    def _create_attacks_frame(self):
        """Create tabs for direct and proxy attacks."""
        notebook = ttk.Notebook(self.left_frame)
        notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Tab for direct attacks
        self._create_attack_tab(
            notebook,
            "Direct Attacks",
            self.attack_manager.direct_attacks,
            self._run_direct_attack,
            self._run_all_direct_attacks
        )

        # Tab for proxy attacks
        self._create_attack_tab(
            notebook,
            "Proxy Attacks",
            self.attack_manager.proxy_attacks,
            self._run_proxy_attack,
            self._run_all_proxy_attacks
        )

    def _create_attack_tab(self, notebook, title, attacks, single_handler, all_handler):
        """Create an attack tab."""
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=title)

        for name in attacks:
            ttk.Button(
                frame,
                text=f"Run {name}",
                command=lambda n=name: single_handler(n)
            ).pack(pady=2, fill=tk.X)

        if title == "Direct Attacks" and all_handler:
            ttk.Button(
                frame,
                text=f"Run All {title}",
                command=all_handler
            ).pack(pady=(10, 2), fill=tk.X)

    def _create_logs_frame(self):
        """Create the logs panel."""
        logs_frame = ttk.LabelFrame(self.right_frame, text="Logs", padding=10)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.logs_text = tk.Text(logs_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.logs_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(logs_frame, command=self.logs_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.logs_text.config(yscrollcommand=scrollbar.set)

    def _log(self, message: str):
        """Display a message in the logs area."""
        try:
            self.logs_text.config(state=tk.NORMAL)
            self.logs_text.insert(tk.END, message + "\n")
            self.logs_text.see(tk.END)
            self.logs_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"[LOG ERROR] {e}")

    def _validate_url(self) -> str:
        """Validate the entered URL."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a target URL")
            return None
        return url

    def _run_direct_attack(self, name: str) -> None:
        """Run a direct attack in a separate thread."""
        def attack_thread():
            url = self._validate_url()
            if url:
                try:
                    self.attack_manager.execute_attack(name, url, use_proxy=False, callback=self._log)
                except Exception as e:
                    self._log(f"Error: {str(e)}")
                    messagebox.showerror("Error", str(e))

        Thread(target=attack_thread).start()

    def _run_proxy_attack(self, name: str) -> None:
        """Run a proxy attack in a separate thread."""
        def attack_thread():
            url = self._validate_url()
            if url:
                try:
                    self.attack_manager.execute_attack(name, url, use_proxy=True, callback=self._log)
                except Exception as e:
                    self._log(f"Error: {str(e)}")
                    messagebox.showerror("Error", str(e))

        Thread(target=attack_thread).start()

    def _run_all_direct_attacks(self) -> None:
        """Run all direct attacks."""
        url = self._validate_url()
        if url:
            for name in self.attack_manager.direct_attacks:
                self._run_direct_attack(name)

    def _run_all_proxy_attacks(self) -> None:
        """Run all proxy attacks."""
        url = self._validate_url()
        if url:
            for name in self.attack_manager.proxy_attacks:
                self._run_proxy_attack(name)

    def run(self) -> None:
        """Launch the GUI."""
        self.root.mainloop()
