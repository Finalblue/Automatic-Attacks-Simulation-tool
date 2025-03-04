import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread

from GUI.AttackManager import AttackManager

class PentestGUI:
    def __init__(self, attack_manager: AttackManager):
        self.attack_manager = attack_manager
        self.root = tk.Tk()
        self.root.title("Pentest Tool")
        self.root.geometry("1000x600")

        self._create_main_layout()
        self._create_url_frame()
        self._create_attacks_frame()
        self._create_logs_frame()

    def _create_main_layout(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew")

        # Set minimum size for frames
        self.left_frame = ttk.Frame(self.paned_window, width=400, height=600)
        self.left_frame.pack_propagate(False)
        self.left_frame.grid_propagate(False)
        
        self.right_frame = ttk.Frame(self.paned_window, width=200, height=600)
        self.right_frame.pack_propagate(False)
        self.right_frame.grid_propagate(False)

        # Add frames to paned window
        self.paned_window.add(self.left_frame, weight=3)
        self.paned_window.add(self.right_frame, weight=2)

        # Configure sash position to enforce minimum widths
        def enforce_min_size(event):
            if self.paned_window.sashpos(0) < 400:
                self.paned_window.sashpos(0, 400)
        
        self.paned_window.bind('<Configure>', enforce_min_size)
        self.paned_window.sashpos(0, 400)

    def _create_url_frame(self):
        url_frame = ttk.LabelFrame(self.left_frame, text="Target Configuration", padding=10)
        url_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(url_frame, text="Target URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.url_entry.insert(tk.END, "http://45.76.47.218:3000")

    def _create_attacks_frame(self):
        notebook = ttk.Notebook(self.left_frame)
        notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self._create_attack_tab(
            notebook, 
            "Direct Attacks",
            self.attack_manager.direct_attacks,
            self._run_direct_attack,
            self._run_all_direct_attacks
        )

        self._create_attack_tab(
            notebook,
            "Proxy Attacks",
            self.attack_manager.proxy_attacks,
            self._run_proxy_attack,
            None
        )

    def _create_attack_tab(self, notebook, title, attacks, single_handler, all_handler):
        outer_frame = ttk.Frame(notebook, padding=10)
        notebook.add(outer_frame, text=title)

        canvas = tk.Canvas(outer_frame, width=350)  # Set minimum width
        canvas.grid_propagate(False)
        scrollbar = ttk.Scrollbar(outer_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        outer_frame.columnconfigure(0, weight=1)
        outer_frame.rowconfigure(0, weight=1)
        
        inner_frame = ttk.Frame(canvas)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        for name in attacks:
            btn = ttk.Button(
                inner_frame,
                text=f"Run {name}",
                command=lambda n=name: single_handler(n)
            )
            btn.grid(row=len(inner_frame.grid_slaves()), column=0, pady=2, sticky="ew")
            inner_frame.grid_columnconfigure(0, weight=1)

        if title == "Direct Attacks" and all_handler:
            btn = ttk.Button(
                inner_frame,
                text=f"Run All {title}",
                command=all_handler
            )
            btn.grid(row=len(inner_frame.grid_slaves()), column=0, pady=(10, 2), sticky="ew")

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def _create_logs_frame(self):
        logs_frame = ttk.LabelFrame(self.right_frame, text="Logs", padding=10)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.logs_text = tk.Text(logs_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.logs_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(logs_frame, command=self.logs_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.logs_text.config(yscrollcommand=scrollbar.set)

    def _log(self, message: str):
        try:
            self.logs_text.config(state=tk.NORMAL)
            self.logs_text.insert(tk.END, message + "\n")
            self.logs_text.see(tk.END)
            self.logs_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Log error: {e}")

    def _validate_url(self) -> str:
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a target URL")
            return None
        return url

    def _run_direct_attack(self, name: str) -> None:
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
        url = self._validate_url()
        if url:
            for name in self.attack_manager.direct_attacks:
                self._run_direct_attack(name)

    def run(self) -> None:
        self.root.mainloop()