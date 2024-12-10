import requests
from tkinter import messagebox

def simulate_sql_injection(url, payload):
    try:
        response = requests.post(url, data={'username': payload, 'password': 'password'})
        print(f"Statut de la requête: {response.status_code}")
        print(f"Contenu de la réponse:\n{response.text}")

        if "Erreur SQL" in response.text or "database" in response.text.lower():
            messagebox.showinfo("Résultat", "Injection SQL réussie !")
            with open("extracted_data.txt", "w") as f:
                f.write("Contenu extrait :\n")
                f.write(response.text)
        else:
            messagebox.showinfo("Résultat", "Pas de vulnérabilité détectée.")
    except requests.RequestException as e:
        messagebox.showerror("Erreur", f"Problème avec la requête : {e}")
