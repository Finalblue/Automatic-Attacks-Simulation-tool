from tkinter import Tk
from GUI.gui import show_home_menu

def main():
    root = Tk()
    root.title("Simulateur d'attaques")
    root.geometry("400x300")

    # lauch home page
    show_home_menu(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
