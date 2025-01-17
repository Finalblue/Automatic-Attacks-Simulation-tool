# gui.py
import tkinter as tk
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import ttk, messagebox, filedialog
from AttackManager import AttackManager
from Alexis.JuiceShopVulnerabilities import JuiceShopVulnerabilities 
from Alexis.XSSAttacks import XSSAttacks
from Alexis.ForgedJWT import ForgedJWT
from Alexis.XXE_Attacks import XXEAttacks
from Alexis.Spider import Spider
from Alexis.JuiceShopCouponExploit import JuiceShopCouponExploit
import logging

class AutoPentestGUI:
    def __init__(self, root):
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
        self.root = root
        self.root.title("Automated Pentest Tool")
        self.logger = logging.getLogger(__name__)
        self.attack_manager = AttackManager()
        self.completed_attacks = []
        self.setup_gui()

    def setup_gui(self):
        self.setup_styles()
        self.create_main_frame()
        self.create_target_config()
        self.create_attack_buttons()
        self.create_progress_bar()
        self.create_log_area()

    def setup_styles(self):
        self.style = ttk.Style()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(sticky='nsew')

    def create_target_config(self):
        config_frame = ttk.LabelFrame(self.main_frame, text="Target Configuration")
        config_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        self.url_var = tk.StringVar(value="http://45.76.47.218:3000")
        ttk.Label(config_frame, text="Target URL:").grid(row=0, column=0)
        ttk.Entry(config_frame, textvariable=self.url_var, width=50).grid(row=0, column=1)

    def create_attack_buttons(self):
        attacks_frame = ttk.LabelFrame(self.main_frame, text="Available Attacks")
        attacks_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        for btn_config in self.attack_manager.get_button_config():
            btn = ttk.Button(
                attacks_frame,
                text=f"{btn_config['name']}\n{btn_config['description']}",
                command=lambda n=btn_config["name"]: self.run_single_attack(n)
            )
            btn.grid(row=btn_config["row"], column=btn_config["column"], padx=5, pady=5)

        ttk.Button(
            attacks_frame,
            text="Run All Attacks",
            command=self.run_all_attacks
        ).grid(row=99, column=0, columnspan=3, pady=10)

    def create_progress_bar(self):
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(
            self.main_frame,
            variable=self.progress_var,
            maximum=100
        ).grid(row=2, column=0, sticky='ew', padx=5, pady=5)

    def create_log_area(self):
        self.log_text = tk.Text(self.main_frame, height=10, width=70)
        self.log_text.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.main_frame, command=self.log_text.yview)
        scrollbar.grid(row=3, column=1, sticky='ns')
        self.log_text['yscrollcommand'] = scrollbar.set

    def log(self, message):
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.root.update()
        self.logger.debug(message)

    def run_single_attack(self, attack_name):
        if not self.attack_manager.can_run_attack(attack_name, self.completed_attacks):
            self.log(f"[!] Cannot run {attack_name} - prerequisites not met")
            return

        self.log(f"[+] Starting {attack_name} attack...")
        attack = self.attack_manager.attacks[attack_name]

        try:
            result = getattr(self, attack.function)()
            if result and result.get("status") == "success":
                self.completed_attacks.append(attack_name)  # Ajoutez l'attaque terminée ici
                self.log(f"[+] {attack_name} result: success")
            else:
                self.log(f"[-] {attack_name} result: failed")
        except Exception as e:
            self.log(f"[!] Error in {attack_name}: {str(e)}")


    def run_all_attacks(self):
        self.completed_attacks = []
        self.log("[+] Starting full attack sequence...")
        
        results = {}
        attack_sequence = self.attack_manager.get_attack_sequence()
        total_attacks = len(attack_sequence)
        
        for i, attack in enumerate(attack_sequence):
            self.progress_var.set((i / total_attacks) * 100)
            result = self.run_single_attack(attack.name)
            if result:
                results[attack.name] = result
            
        self.progress_var.set(100)
        self.log("[+] Attack sequence completed")
        self.save_results(results)

    def run_spider(self):
        spider = Spider(self.url_var.get())
        results = spider.crawl()
        return {"status": "success", "endpoints": results}

    def run_jwt_attack(self):
        jwt = ForgedJWT(self.url_var.get())
        return jwt.run_attack()

    def run_sql_injection(self):
        juice = JuiceShopVulnerabilities(self.url_var.get())
        return juice.test_sql_injection()

    def run_captcha_bypass(self):
        juice = JuiceShopVulnerabilities(self.url_var.get())
        result = juice.test_captcha_bypass()
        if result.get("status") == "success":
            self.log("[+] Successfully bypassed CAPTCHA")
        return result

    def run_coupon_exploit(self):
        try:
            exploit = JuiceShopCouponExploit(self.url_var.get())
            success = exploit.run_exploit()
            if success:
                self.log("[+] COUPON result: success")
                return {"status": "success"}
            else:
                self.log("[-] COUPON result: failed")
                return {"status": "failed"}
        except Exception as e:
            self.log(f"[!] COUPON error: {str(e)}")
            return {"status": "failed", "error": str(e)}


    def run_xss_attacks(self):
        xss = XSSAttacks(self.url_var.get())
        results = xss.run_all_xss_attacks()
        return {"status": "success" if any(r["status"] == "success" for r in results.values()) else "failed"}

    def run_xxe_attack(self):
        xxe = XXEAttacks(self.url_var.get())
        try:
            results = xxe.run_all_xxe_attacks()
            return {"status": "success" if any(r["status"] == "success" for r in results.values()) else "failed"}
        except Exception as e:
            self.log(f"[!] XXE attack error: {str(e)}")
            return {"status": "failed", "error": str(e)}

    def save_results(self, results):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Attack Results",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(results, f, indent=4)
                self.log(f"[+] Results saved to {file_path}")
        except Exception as e:
            self.log(f"[!] Error saving results: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoPentestGUI(root)
    root.mainloop()