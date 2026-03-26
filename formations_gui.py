import tkinter as tk
from tkinter import ttk, messagebox
from db import connexion_bd

def vider_contenu(frame_contenu):
    for widget in frame_contenu.winfo_children():
        widget.destroy()

def ouvrir_formations(frame_contenu):
    vider_contenu(frame_contenu)

    titre = tk.Label(
        frame_contenu,
        text="GESTION DES FORMATIONS",
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

    code_selectionne = tk.StringVar(value="")

    tk.Label(
        frame_gauche,
        text="Formulaire formation",
        font=("Arial", 14, "bold"),
        bg="#f2f2f2",
        fg="darkblue"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_gauche, text="Code", font=("Arial", 11), bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_code = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_code.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Intitulé", font=("Arial", 11), bg="#f2f2f2").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_intitule = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_intitule.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Langue", font=("Arial", 11), bg="#f2f2f2").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_langue = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_langue.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Niveau", font=("Arial", 11), bg="#f2f2f2").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_niveau = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_niveau.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(frame_gauche, text="Objectif", font=("Arial", 11), bg="#f2f2f2").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_objectif = tk.Entry(frame_gauche, font=("Arial", 11), width=25)
    entry_objectif.grid(row=5, column=1, padx=10, pady=5)

    frame_recherche = tk.Frame(frame_droite, bg="white")
    frame_recherche.pack(fill="x", padx=10, pady=10)

    tk.Label(
        frame_recherche,
        text="Recherche par code, intitulé ou langue",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(side="left", padx=5)

    entry_recherche = tk.Entry(frame_recherche, font=("Arial", 11), width=30)
    entry_recherche.pack(side="left", padx=5)

    frame_tableau = tk.Frame(frame_droite, bg="white")
    frame_tableau.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    colonnes = ("code", "intitule", "langue", "niveau", "objectif")

    tableau = ttk.Treeview(frame_tableau, columns=colonnes, show="headings")

    tableau.heading("code", text="Code")
    tableau.heading("intitule", text="Intitulé")
    tableau.heading("langue", text="Langue")
    tableau.heading("niveau", text="Niveau")
    tableau.heading("objectif", text="Objectif")

    tableau.column("code", width=100)
    tableau.column("intitule", width=180)
    tableau.column("langue", width=120)
    tableau.column("niveau", width=120)
    tableau.column("objectif", width=220)

    scrollbar_y = tk.Scrollbar(frame_tableau, orient="vertical", command=tableau.yview)
    tableau.configure(yscrollcommand=scrollbar_y.set)

    tableau.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    def reinitialiser_couleurs():
        entry_code.config(bg="white")
        entry_intitule.config(bg="white")
        entry_langue.config(bg="white")
        entry_niveau.config(bg="white")

    def vider_champs():
        entry_code.delete(0, tk.END)
        entry_intitule.delete(0, tk.END)
        entry_langue.delete(0, tk.END)
        entry_niveau.delete(0, tk.END)
        entry_objectif.delete(0, tk.END)
        code_selectionne.set("")

    def reinitialiser_formulaire():
        vider_champs()
        reinitialiser_couleurs()
        entry_recherche.delete(0, tk.END)
        selection = tableau.selection()
        if selection:
            tableau.selection_remove(selection)

    def remplir_formulaire(event):
        selection = tableau.selection()

        if not selection:
            return

        valeurs = tableau.item(selection[0], "values")

        code_selectionne.set(valeurs[0])

        entry_code.delete(0, tk.END)
        entry_code.insert(0, valeurs[0])

        entry_intitule.delete(0, tk.END)
        entry_intitule.insert(0, valeurs[1])

        entry_langue.delete(0, tk.END)
        entry_langue.insert(0, valeurs[2])

        entry_niveau.delete(0, tk.END)
        entry_niveau.insert(0, valeurs[3])

        entry_objectif.delete(0, tk.END)
        entry_objectif.insert(0, valeurs[4])

        reinitialiser_couleurs()

    def vider_tableau():
        for ligne in tableau.get_children():
            tableau.delete(ligne)

    def afficher_toutes_formations():
        vider_tableau()

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("""
            SELECT code_formation, intitule_formation, langue_formation, niveau_formation, objectif_formation
            FROM formations
            ORDER BY intitule_formation
        """)

        formations = curseur.fetchall()
        connexion.close()

        for formation in formations:
            tableau.insert("", tk.END, values=formation)

    def rechercher_formations():
        mot_cle = entry_recherche.get().strip()

        if mot_cle == "":
            afficher_toutes_formations()
            return

        vider_tableau()

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("""
            SELECT code_formation, intitule_formation, langue_formation, niveau_formation, objectif_formation
            FROM formations
            WHERE code_formation LIKE ? OR intitule_formation LIKE ? OR langue_formation LIKE ?
            ORDER BY intitule_formation
        """, ("%" + mot_cle + "%", "%" + mot_cle + "%", "%" + mot_cle + "%"))

        formations = curseur.fetchall()
        connexion.close()

        for formation in formations:
            tableau.insert("", tk.END, values=formation)

        if len(formations) == 0:
            messagebox.showinfo("Information", "Aucune formation trouvée.")

    def enregistrer_formation():
        reinitialiser_couleurs()

        code = entry_code.get().strip()
        intitule = entry_intitule.get().strip()
        langue = entry_langue.get().strip()
        niveau = entry_niveau.get().strip()
        objectif = entry_objectif.get().strip()

        erreur = False

        if code == "":
            entry_code.config(bg="#ffdddd")
            erreur = True

        if intitule == "":
            entry_intitule.config(bg="#ffdddd")
            erreur = True

        if langue == "":
            entry_langue.config(bg="#ffdddd")
            erreur = True

        if niveau == "":
            entry_niveau.config(bg="#ffdddd")
            erreur = True

        if erreur:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("SELECT * FROM formations WHERE code_formation = ?", (code,))
        formation = curseur.fetchone()

        if formation is not None:
            connexion.close()
            entry_code.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Une formation existe déjà avec ce code.")
            return

        curseur.execute("""
            INSERT INTO formations (
                code_formation,
                intitule_formation,
                langue_formation,
                niveau_formation,
                objectif_formation
            )
            VALUES (?, ?, ?, ?, ?)
        """, (code, intitule, langue, niveau, objectif))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Formation enregistrée avec succès.")
        reinitialiser_formulaire()
        afficher_toutes_formations()

    def modifier_formation():
        reinitialiser_couleurs()

        code_original = code_selectionne.get()

        if code_original == "":
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner une formation dans la liste.")
            return

        if entry_code.get().strip() == "":
            entry_code.config(bg="#ffdddd")
            messagebox.showerror("Erreur", "Le code est obligatoire.")
            return

        intitule = entry_intitule.get().strip()
        langue = entry_langue.get().strip()
        niveau = entry_niveau.get().strip()
        objectif = entry_objectif.get().strip()

        erreur = False

        if intitule == "":
            entry_intitule.config(bg="#ffdddd")
            erreur = True

        if langue == "":
            entry_langue.config(bg="#ffdddd")
            erreur = True

        if niveau == "":
            entry_niveau.config(bg="#ffdddd")
            erreur = True

        if erreur:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("""
            UPDATE formations
            SET intitule_formation = ?, langue_formation = ?, niveau_formation = ?, objectif_formation = ?
            WHERE code_formation = ?
        """, (intitule, langue, niveau, objectif, code_original))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Formation modifiée avec succès.")
        reinitialiser_formulaire()
        afficher_toutes_formations()

    def supprimer_formation():
        code_original = code_selectionne.get()

        if code_original == "":
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner une formation dans la liste.")
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cette formation ?"
        )

        if not confirmation:
            return

        connexion = connexion_bd()
        curseur = connexion.cursor()

        curseur.execute("DELETE FROM inscription WHERE code_formation = ?", (code_original,))
        curseur.execute("DELETE FROM formations WHERE code_formation = ?", (code_original,))

        connexion.commit()
        connexion.close()

        messagebox.showinfo("Succès", "Formation supprimée avec succès.")
        reinitialiser_formulaire()
        afficher_toutes_formations()

    tableau.bind("<<TreeviewSelect>>", remplir_formulaire)

    frame_boutons = tk.Frame(frame_gauche, bg="#f2f2f2")
    frame_boutons.grid(row=6, column=0, columnspan=2, pady=15)

    btn_enregistrer = tk.Button(
        frame_boutons,
        text="Enregistrer",
        width=12,
        command=enregistrer_formation
    )
    btn_enregistrer.grid(row=0, column=0, padx=5, pady=5)

    btn_modifier = tk.Button(
        frame_boutons,
        text="Modifier",
        width=12,
        command=modifier_formation
    )
    btn_modifier.grid(row=0, column=1, padx=5, pady=5)

    btn_supprimer = tk.Button(
        frame_boutons,
        text="Supprimer",
        width=12,
        command=supprimer_formation
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
        width=12,
        command=rechercher_formations
    )
    btn_rechercher.pack(side="left", padx=5)

    btn_afficher_tous = tk.Button(
        frame_recherche,
        text="Afficher tous",
        width=12,
        command=afficher_toutes_formations
    )
    btn_afficher_tous.pack(side="left", padx=5)

    afficher_toutes_formations()