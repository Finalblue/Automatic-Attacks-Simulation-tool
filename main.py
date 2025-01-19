from tkinter import Tk
from GUI.AttackManager import AttackManager
from GUI.gui import PentestGUI
import os
import re
import subprocess
import sys



def find_imports(directory="."):
    """
    Scans all Python files in the given directory to detect imported libraries.
    """
    imports = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        # Search for imports in Python files
                        match = re.match(r"^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)", line)
                        if match:
                            imports.add(match.group(1).split(".")[0])
    return imports


def get_installed_packages():
    """
    Lists all libraries installed in the current environment.
    """
    output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], encoding="utf-8")
    installed = {}
    for line in output.splitlines():
        if "==" in line:  # Format: name==version
            name, version = line.split("==")
            installed[name] = version
    return installed


def generate_requirements(directory="."):
    """
    Generates a requirements.txt file based on the imported libraries.
    """
    print("Analyzing Python files to find imports...")
    imported_libraries = find_imports(directory)
    installed_packages = get_installed_packages()

    # Filter libraries that are actually installed (ignore standard modules)
    required_packages = {lib: installed_packages[lib] for lib in imported_libraries if lib in installed_packages}

    # Write to requirements.txt
    with open("requirements.txt", "w") as f:
        for lib, version in required_packages.items():
            f.write(f"{lib}=={version}\n")

    print("requirements.txt file successfully updated!")
    print("Contents of requirements.txt:")
    for lib, version in required_packages.items():
        print(f"  {lib}=={version}")


def install_requirements():
    """
    Automatically installs missing libraries from requirements.txt.
    """
    if not os.path.exists("requirements.txt"):
        print("No requirements.txt file found. Automatically generating...")
        generate_requirements()

    print("Installing libraries from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def main():
    generate_requirements()
    install_requirements()
    gui = PentestGUI(AttackManager())
    gui.run()

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

