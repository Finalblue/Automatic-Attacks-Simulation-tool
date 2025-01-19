from tkinter import Tk
from GUI.gui import show_home_menu
from Utils.AttackManager import AttackManager
from ATTACKS.Attacks.AdminSectionAccess import AdminSectionAccess
def main():
    root = Tk()
    root.title("Simulateur d'attaques")
    root.geometry("400x300")

    # lauch home page
    show_home_menu(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()

attack_manager = AttackManager()

print("Available Attacks:")
for attack_name, attack in attack_manager.get_attacks().items():
    print(f" - {attack.name} ({attack.attack_type})")


selected_attack = input("Enter the attack name: ")
target_url = input("Enter the target URL: ")

if selected_attack in attack_manager.get_attacks():
    attack = attack_manager.get_attacks()[selected_attack]
    attack.run_function(target_url, callback=print)
else:
    print(f"Attack '{selected_attack}' not found!")

