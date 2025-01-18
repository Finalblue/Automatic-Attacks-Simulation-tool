import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from AttackManager import AttackManager

class PentestGUI:
    def __init__(self, attack_manager: AttackManager):
        self.attack_manager = attack_manager
        self.root = tk.Tk()
        self.root.title("Pentest Tool")
        
        url_frame = tk.Frame(self.root)
        url_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(url_frame, text="Target URL:").pack(side=tk.LEFT)
        self.url_entry = tk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        self.attacks_frame = tk.Frame(self.root)
        self.attacks_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Button(
            self.root,
            text="Run All Attacks",
            command=self._run_all_attacks
        ).pack(pady=(0, 10), padx=10)
        
        self._create_attack_buttons()

    def _create_attack_buttons(self) -> None:
        for name in self.attack_manager.attack_names:
            btn = tk.Button(
                self.attacks_frame,
                text=f"Run {name}",
                command=lambda n=name: self._run_single_attack(n)
            )
            btn.pack(pady=2, fill=tk.X)

    def _run_single_attack(self, name: str) -> None:
        url = self.url_entry.get().strip()
        if url:
            self.attack_manager.execute_attack(name, url)
        else:
            print("Please enter a target URL")

    def _run_all_attacks(self) -> None:
        url = self.url_entry.get().strip()
        if url:
            self.attack_manager.execute_all(url)
        else:
            print("Please enter a target URL")

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    gui = PentestGUI(AttackManager())
    gui.run()