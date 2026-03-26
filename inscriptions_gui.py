import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import connexion_bd

def vider_contenu(frame_contenu):
    for widget in frame_contenu.winfo_children():
        widget.destroy()

def ouvrir_inscriptions(frame_contenu):
    vider_contenu(frame_contenu)

    titre = tk.Label(
        frame_contenu,
        text="GESTION DES INSCRIPTIONS",
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

    tk.Label(
        frame_gauche,
        text="Formulaire inscription",
        font=("Arial", 14, "bold"),
        bg="#f2f2f2",
        fg="darkblue"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_gauche, text="INE étudiant", font=("Arial", 11), bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_ine = tk.Entry(frame_gauche, font=("Arial", 11), width=28)
    entry_ine.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Formation", font=("Arial", 11), bg="#f2f2f2").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    combo_formation = ttk.Combobox(frame_gauche, font=("Arial", 11), width=26, state="readonly")
    combo_formation.grid(row=2, column=1, padx=10, pady=5)

    label_info = tk.Label(
        frame_gauche,
        text="",
        font=("Arial", 10),
        bg="#f2f2f2",
        fg="green",
        justify="left"
    )
    label_info.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    frame_boutons = tk.Frame(frame_gauche, bg="#f2f2f2")
    frame_boutons.grid(row=4, column=0, columnspan=2, pady=10)

    frame_actions = tk.Frame(frame_droite, bg="white")
    frame_actions.pack(fill="x", padx=10, pady=10)

    btn_formations_etudiant = tk.Button(
        frame_actions,
        text="Formations de l'étudiant",
        width=22
    )
    btn_formations_etudiant.pack(side="left", padx=5)

    btn_etudiants_formation = tk.Button(
        frame_actions,
        text="Étudiants de la formation",
        width=22
    )
    btn_etudiants_formation.pack(side="left", padx=5)

    frame_tableau = tk.Frame(frame_droite, bg="white")
    frame_tableau.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    tableau = ttk.Treeview(frame_tableau, show="headings")
    scrollbar_y = tk.Scrollbar(frame_tableau, orient="vertical", command=tableau.yview)
    tableau.configure(yscrollcommand=scrollbar_y.set)

    tableau.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    def reinitialiser_couleurs():
        entry_ine.config(bg="white")

    def vider_tableau():
        for ligne in tableau.get_children():
            tableau.delete(ligne)

    def vider_entetes():
        tableau["columns"] = ()

    def configurer_tableau_formations_etudiant():
        vider_tableau()
        tableau["columns"] = ("id", "code", "intitule", "date")

        tableau.heading("id", text="ID inscription")
        tableau.heading("code", text="Code formation")
        tableau.heading("intitule", text="Intitulé")
        tableau.heading("date", text="Date inscription")

        tableau.column("id", width=100)
        tableau.column("code", width=120)
        tableau.column("intitule", width=220)
        tableau.column("date", width=140)

    def configurer_tableau_etudiants_formation():
        vider_tableau()
        tableau["columns"] = ("ine", "nom", "prenom", "email", "date")

        tableau.heading("ine", text="INE")
        tableau.heading("nom", text="Nom")
        tableau.heading("prenom", text="Prénom")
        tableau.heading("email", text="Email")
        tableau.heading("date", text="Date inscription")

        tableau.column("ine", width=120)
        tableau.column("nom", width=140)
        tableau.column("prenom", width=140)
        tableau.column("email", width=220)
        tableau.column("date", width=140)

    def charger_formations():
        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("""
            SELECT code_formation, intitule_formation
            FROM formations
            ORDER BY intitule_formation
        """)

        formations = curseur.fetchall()
        connexion.close()

        valeurs = []
        for formation in formations:
            valeurs.append(f"{formation[0]} - {formation[1]}")

        combo_formation["values"] = valeurs

    def obtenir_code_formation():
        valeur = combo_formation.get().strip()

        if valeur == "":
            return ""

        return valeur.split(" - ")[0]

    def reinitialiser_formulaire():
        entry_ine.delete(0, tk.END)
        combo_formation.set("")
        label_info.config(text="")
        reinitialiser_couleurs()
        vider_tableau()

    def afficher_formations_etudiant():
        reinitialiser_couleurs()

        ine = entry_ine.get().strip()

        if ine == "":
            entry_ine.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Veuillez saisir l'INE de l'étudiant.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("SELECT * FROM etudiants WHERE ine_etudiant = ?", (ine,))
        etudiant = curseur.fetchone()

        if etudiant is None:
            connexion.close()
            entry_ine.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Étudiant introuvable.")
            return

        configurer_tableau_formations_etudiant()

        curseur.execute("""
            SELECT i.id_inscription,
                   f.code_formation,
                   f.intitule_formation,
                   i.date_inscription
            FROM inscription i, formations f
            WHERE i.code_formation = f.code_formation
              AND i.ine_etudiant = ?
            ORDER BY i.date_inscription
        """, (ine,))

        inscriptions = curseur.fetchall()
        connexion.close()

        label_info.config(
            text="Étudiant : " + etudiant[1] + " " + etudiant[2] + "\nEmail : " + etudiant[3]
        )

        for inscription in inscriptions:
            tableau.insert("", tk.END, values=inscription)

        if len(inscriptions) == 0:
            messagebox.showinfo("Information", "Cet étudiant n'est inscrit à aucune formation.")

    def afficher_etudiants_formation():
        code = obtenir_code_formation()

        if code == "":
            messagebox.showerror("Erreur", "Veuillez choisir une formation.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("SELECT * FROM formations WHERE code_formation = ?", (code,))
        formation = curseur.fetchone()

        if formation is None:
            connexion.close()
            messagebox.showerror("Erreur", "Formation introuvable.")
            return

        configurer_tableau_etudiants_formation()

        curseur.execute("""
            SELECT e.ine_etudiant,
                   e.nom_etudiant,
                   e.prenom_etudiant,
                   e.email_etudiant,
                   i.date_inscription
            FROM inscription i, etudiants e
            WHERE i.ine_etudiant = e.ine_etudiant
              AND i.code_formation = ?
            ORDER BY e.nom_etudiant, e.prenom_etudiant
        """, (code,))

        etudiants = curseur.fetchall()
        connexion.close()

        label_info.config(
            text="Formation : " + formation[1] + "\nLangue : " + formation[2] + " | Niveau : " + formation[3]
        )

        for etudiant in etudiants:
            tableau.insert("", tk.END, values=etudiant)

        if len(etudiants) == 0:
            messagebox.showinfo("Information", "Aucun étudiant n'est inscrit à cette formation.")

    def inscrire_etudiant():
        reinitialiser_couleurs()

        ine = entry_ine.get().strip()
        code = obtenir_code_formation()

        if ine == "":
            entry_ine.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Veuillez saisir l'INE de l'étudiant.")
            return

        if code == "":
            messagebox.showerror("Erreur", "Veuillez choisir une formation.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("SELECT * FROM etudiants WHERE ine_etudiant = ?", (ine,))
        etudiant = curseur.fetchone()

        if etudiant is None:
            connexion.close()
            entry_ine.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Étudiant introuvable.")
            return

        curseur.execute("SELECT * FROM formations WHERE code_formation = ?", (code,))
        formation = curseur.fetchone()

        if formation is None:
            connexion.close()
            messagebox.showerror("Erreur", "Formation introuvable.")
            return

        curseur.execute("""
            SELECT * FROM inscription
            WHERE ine_etudiant = ? AND code_formation = ?
        """, (ine, code))
        inscription = curseur.fetchone()

        if inscription is not None:
            connexion.close()
            messagebox.showerror("Erreur", "Cet étudiant est déjà inscrit à cette formation.")
            return

        date_inscription = str(date.today())

        curseur.execute("""
            INSERT INTO inscription (ine_etudiant, code_formation, date_inscription)
            VALUES (?, ?, ?)
        """, (ine, code, date_inscription))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Inscription effectuée avec succès.")
        afficher_formations_etudiant()

    def desinscrire_etudiant():
        ine = entry_ine.get().strip()
        code = obtenir_code_formation()

        if ine == "":
            entry_ine.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Veuillez saisir l'INE de l'étudiant.")
            return

        if code == "":
            messagebox.showerror("Erreur", "Veuillez choisir une formation.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("""
            SELECT * FROM inscription
            WHERE ine_etudiant = ? AND code_formation = ?
        """, (ine, code))
        inscription = curseur.fetchone()

        if inscription is None:
            connexion.close()
            messagebox.showerror("Erreur", "Inscription introuvable.")
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment désinscrire cet étudiant de cette formation ?"
        )

        if not confirmation:
            connexion.close()
            return

        curseur.execute("""
            DELETE FROM inscription
            WHERE ine_etudiant = ? AND code_formation = ?
        """, (ine, code))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Désinscription effectuée avec succès.")
        afficher_formations_etudiant()

    btn_inscrire = tk.Button(
        frame_boutons,
        text="Inscrire",
        width=14,
        command=inscrire_etudiant
    )
    btn_inscrire.grid(row=0, column=0, padx=5, pady=5)

    btn_desinscrire = tk.Button(
        frame_boutons,
        text="Désinscrire",
        width=14,
        command=desinscrire_etudiant
    )
    btn_desinscrire.grid(row=0, column=1, padx=5, pady=5)

    btn_reinitialiser = tk.Button(
        frame_boutons,
        text="Réinitialiser",
        width=14,
        command=reinitialiser_formulaire
    )
    btn_reinitialiser.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    btn_formations_etudiant.config(command=afficher_formations_etudiant)
    btn_etudiants_formation.config(command=afficher_etudiants_formation)

    charger_formations()
    vider_entetes()