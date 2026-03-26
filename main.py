import tkinter as tk
from etudiants_gui import ouvrir_etudiants
from formations_gui import ouvrir_formations
from inscriptions_gui import ouvrir_inscriptions

def vider_contenu(frame_contenu):
    for widget in frame_contenu.winfo_children():
        widget.destroy()

def afficher_accueil(frame_contenu):
    vider_contenu(frame_contenu)

    titre = tk.Label(
        frame_contenu,
        text="Bienvenue dans l'application de gestion de formation",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="darkblue"
    )
    titre.pack(pady=30)

    texte = tk.Label(
        frame_contenu,
        text="Choisissez un volet dans le menu du haut.",
        font=("Arial", 12),
        bg="white"
    )
    texte.pack(pady=10)

fenetre = tk.Tk()
fenetre.title("Gestion d'un établissement de formation")
fenetre.geometry("1100x650")
fenetre.config(bg="white")

label_titre = tk.Label(
    fenetre,
    text="Système de gestion d'un établissement de formation",
    font=("Arial", 20, "bold"),
    bg="#0d6efd",
    fg="white",
    pady=15
)
label_titre.pack(fill="x")

frame_menu = tk.Frame(fenetre, bg="#d9e6f2", pady=10)
frame_menu.pack(fill="x")

frame_contenu = tk.Frame(fenetre, bg="white")
frame_contenu.pack(fill="both", expand=True)

btn_etudiants = tk.Button(
    frame_menu,
    text="Gestion des étudiants",
    font=("Arial", 12),
    width=20,
    command=lambda: ouvrir_etudiants(frame_contenu)
)
btn_etudiants.pack(side="left", padx=10)

btn_formations = tk.Button(
    frame_menu,
    text="Gestion des formations",
    font=("Arial", 12),
    width=20,
    command=lambda: ouvrir_formations(frame_contenu)
)
btn_formations.pack(side="left", padx=10)

btn_inscriptions = tk.Button(
    frame_menu,
    text="Gestion des inscriptions",
    font=("Arial", 12),
    width=20,
    command=lambda: ouvrir_inscriptions(frame_contenu)
)
btn_inscriptions.pack(side="left", padx=10)

btn_accueil = tk.Button(
    frame_menu,
    text="Accueil",
    font=("Arial", 12),
    width=12,
    command=lambda: afficher_accueil(frame_contenu)
)
btn_accueil.pack(side="right", padx=10)

afficher_accueil(frame_contenu)

fenetre.mainloop()