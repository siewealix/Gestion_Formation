import tkinter as tk
from tkinter import ttk, messagebox
from db import connexion_bd

def email_valide(email):
    return "@" in email and "." in email

def vider_contenu(frame_contenu):
    for widget in frame_contenu.winfo_children():
        widget.destroy()

def ouvrir_etudiants(frame_contenu):
    vider_contenu(frame_contenu)

    titre = tk.Label(
        frame_contenu,
        text="GESTION DES ETUDIANTS",
        font=("Arial", 18, "bold"),
        bg="#0d6efd",
        fg="white",
        pady=10
    )
    titre.pack(fill="x")

    frame_principal = tk.Frame(frame_contenu, bg="white")
    frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

    frame_gauche = tk.Frame(frame_principal, bg="#f2f2f2", bd=2, relief="groove")
    frame_gauche.pack(side="left", fill="y", padx=(0, 10))

    frame_droite = tk.Frame(frame_principal, bg="white", bd=2, relief="groove")
    frame_droite.pack(side="right", fill="both", expand=True)

    ine_selectionne = tk.StringVar(value="")

    tk.Label(
        frame_gauche,
        text="Formulaire étudiant",
        font=("Arial", 14, "bold"),
        bg="#f2f2f2",
        fg="darkblue"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_gauche, text="INE", font=("Arial", 11), bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_ine = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_ine.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Nom", font=("Arial", 11), bg="#f2f2f2").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_nom = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_nom.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Prénom", font=("Arial", 11), bg="#f2f2f2").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_prenom = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_prenom.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Email", font=("Arial", 11), bg="#f2f2f2").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_email = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_email.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Adresse", font=("Arial", 11), bg="#f2f2f2").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_adresse = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_adresse.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Ville", font=("Arial", 11), bg="#f2f2f2").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_ville = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_ville.grid(row=6, column=1, padx=10, pady=5)

    frame_recherche = tk.Frame(frame_droite, bg="white")
    frame_recherche.pack(fill="x", padx=10, pady=10)

    tk.Label(
        frame_recherche,
        text="Recherche par nom ou email",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(side="left", padx=5)

    entry_recherche = tk.Entry(frame_recherche, font=("Arial", 11), width=30)
    entry_recherche.pack(side="left", padx=5)

    frame_tableau = tk.Frame(frame_droite, bg="white")
    frame_tableau.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    colonnes = ("ine", "nom", "prenom", "email", "adresse", "ville")

    tableau = ttk.Treeview(frame_tableau, columns=colonnes, show="headings")

    tableau.heading("ine", text="INE")
    tableau.heading("nom", text="Nom")
    tableau.heading("prenom", text="Prénom")
    tableau.heading("email", text="Email")
    tableau.heading("adresse", text="Adresse")
    tableau.heading("ville", text="Ville")

    tableau.column("ine", width=100)
    tableau.column("nom", width=120)
    tableau.column("prenom", width=120)
    tableau.column("email", width=180)
    tableau.column("adresse", width=150)
    tableau.column("ville", width=120)

    scrollbar_y = tk.Scrollbar(frame_tableau, orient="vertical", command=tableau.yview)
    tableau.configure(yscrollcommand=scrollbar_y.set)

    tableau.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    def reinitialiser_couleurs():
        entry_ine.config(bg="white")
        entry_nom.config(bg="white")
        entry_prenom.config(bg="white")
        entry_email.config(bg="white")

    def vider_champs():
        entry_ine.delete(0, tk.END)
        entry_nom.delete(0, tk.END)
        entry_prenom.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_adresse.delete(0, tk.END)
        entry_ville.delete(0, tk.END)
        ine_selectionne.set("")

    def reinitialiser_formulaire():
        vider_champs()
        reinitialiser_couleurs()
        selection = tableau.selection()
        if selection:
            tableau.selection_remove(selection)

    def remplir_formulaire(event):
        selection = tableau.selection()

        if not selection:
            return

        valeurs = tableau.item(selection[0], "values")

        ine_selectionne.set(valeurs[0])

        entry_ine.delete(0, tk.END)
        entry_ine.insert(0, valeurs[0])

        entry_nom.delete(0, tk.END)
        entry_nom.insert(0, valeurs[1])

        entry_prenom.delete(0, tk.END)
        entry_prenom.insert(0, valeurs[2])

        entry_email.delete(0, tk.END)
        entry_email.insert(0, valeurs[3])

        entry_adresse.delete(0, tk.END)
        entry_adresse.insert(0, valeurs[4])

        entry_ville.delete(0, tk.END)
        entry_ville.insert(0, valeurs[5])

        reinitialiser_couleurs()

    def afficher_tous_etudiants():
        for ligne in tableau.get_children():
            tableau.delete(ligne)

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("""
            SELECT ine_etudiant, nom_etudiant, prenom_etudiant, email_etudiant, adresse_etudiant, ville_etudiant
            FROM etudiants
            ORDER BY nom_etudiant, prenom_etudiant
        """)

        etudiants = curseur.fetchall()
        connexion.close()

        for etudiant in etudiants:
            tableau.insert("", tk.END, values=etudiant)

    def enregistrer_etudiant():
        reinitialiser_couleurs()

        ine = entry_ine.get().strip()
        nom = entry_nom.get().strip()
        prenom = entry_prenom.get().strip()
        email = entry_email.get().strip()
        adresse = entry_adresse.get().strip()
        ville = entry_ville.get().strip()

        erreur = False

        if ine == "":
            entry_ine.config(bg="#ffdddd")
            erreur = True

        if nom == "":
            entry_nom.config(bg="#ffdddd")
            erreur = True

        if prenom == "":
            entry_prenom.config(bg="#ffdddd")
            erreur = True

        if email == "":
            entry_email.config(bg="#ffdddd")
            erreur = True

        if erreur:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        if not email_valide(email):
            entry_email.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Adresse email invalide.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("SELECT * FROM etudiants WHERE ine_etudiant = ?", (ine,))
        etudiant = curseur.fetchone()

        if etudiant is not None:
            connexion.close()
            entry_ine.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Un étudiant existe déjà avec cet INE.")
            return

        curseur.execute("""
            INSERT INTO etudiants (
                ine_etudiant,
                nom_etudiant,
                prenom_etudiant,
                email_etudiant,
                adresse_etudiant,
                ville_etudiant
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ine, nom, prenom, email, adresse, ville))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Étudiant enregistré avec succès.")
        reinitialiser_formulaire()
        afficher_tous_etudiants()

    def modifier_etudiant():
        reinitialiser_couleurs()

        ine_original = ine_selectionne.get()

        if ine_original == "":
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un étudiant dans la liste.")
            return

        nom = entry_nom.get().strip()
        prenom = entry_prenom.get().strip()
        email = entry_email.get().strip()
        adresse = entry_adresse.get().strip()
        ville = entry_ville.get().strip()

        erreur = False

        if entry_ine.get().strip() == "":
            entry_ine.config(bg="#ffdddd")
            erreur = True

        if nom == "":
            entry_nom.config(bg="#ffdddd")
            erreur = True

        if prenom == "":
            entry_prenom.config(bg="#ffdddd")
            erreur = True

        if email == "":
            entry_email.config(bg="#ffdddd")
            erreur = True

        if erreur:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        if not email_valide(email):
            entry_email.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Adresse email invalide.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("""
            UPDATE etudiants
            SET nom_etudiant = ?, prenom_etudiant = ?, email_etudiant = ?, adresse_etudiant = ?, ville_etudiant = ?
            WHERE ine_etudiant = ?
        """, (nom, prenom, email, adresse, ville, ine_original))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Étudiant modifié avec succès.")
        reinitialiser_formulaire()
        afficher_tous_etudiants()

    def supprimer_etudiant():
        ine_original = ine_selectionne.get()

        if ine_original == "":
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un étudiant dans la liste.")
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cet étudiant ?"
        )

        if not confirmation:
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("DELETE FROM inscription WHERE ine_etudiant = ?", (ine_original,))
        curseur.execute("DELETE FROM etudiants WHERE ine_etudiant = ?", (ine_original,))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Étudiant supprimé avec succès.")
        reinitialiser_formulaire()
        afficher_tous_etudiants()

    tableau.bind("<<TreeviewSelect>>", remplir_formulaire)

    frame_boutons = tk.Frame(frame_gauche, bg="#f2f2f2")
    frame_boutons.grid(row=7, column=0, columnspan=2, pady=15)

    btn_enregistrer = tk.Button(
        frame_boutons,
        text="Enregistrer",
        width=12,
        command=enregistrer_etudiant
    )
    btn_enregistrer.grid(row=0, column=0, padx=5, pady=5)

    btn_modifier = tk.Button(
        frame_boutons,
        text="Modifier",
        width=12,
        command=modifier_etudiant
    )
    btn_modifier.grid(row=0, column=1, padx=5, pady=5)

    btn_supprimer = tk.Button(
        frame_boutons,
        text="Supprimer",
        width=12,
        command=supprimer_etudiant
    )
    btn_supprimer.grid(row=1, column=0, padx=5, pady=5)

    btn_reinitialiser = tk.Button(
        frame_boutons,
        text="Réinitialiser",
        width=12,
        command=reinitialiser_formulaire
    )
    btn_reinitialiser.grid(row=1, column=1, padx=5, pady=5)

    btn_rechercher = tk.Button(
        frame_recherche,
        text="Rechercher",
        width=12
    )
    btn_rechercher.pack(side="left", padx=5)

    btn_afficher_tous = tk.Button(
        frame_recherche,
        text="Afficher tous",
        width=12,
        command=afficher_tous_etudiants
    )
    btn_afficher_tous.pack(side="left", padx=5)

    afficher_tous_etudiants()
