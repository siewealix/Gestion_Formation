# Application de gestion d'un établissement de formation

## Présentation

Ce projet est une application de bureau réalisée en **Python** avec **Tkinter** pour l’interface graphique et **SQLite** pour la base de données.

L’objectif de l’application est de gérer :

- les **étudiants**
- les **formations**
- les **inscriptions**

La partie **formateurs** n’a pas été traitée, comme cela était indiqué dans le TP.

---

## Fonctionnalités

### 1. Gestion des étudiants
Cette partie permet de :

- ajouter un étudiant
- afficher la liste des étudiants
- sélectionner un étudiant dans le tableau
- modifier ses informations
- supprimer un étudiant
- rechercher un étudiant par nom ou par email

### 2. Gestion des formations
Cette partie permet de :

- ajouter une formation
- afficher la liste des formations
- sélectionner une formation dans le tableau
- modifier ses informations
- supprimer une formation
- rechercher une formation par code, intitulé ou langue

### 3. Gestion des inscriptions
Cette partie permet de :

- inscrire un étudiant à une formation
- désinscrire un étudiant d’une formation
- afficher les formations d’un étudiant
- afficher les étudiants inscrits à une formation

---

## Technologies utilisées

- **Python**
- **Tkinter** pour l’interface graphique
- **SQLite** pour la base de données

---

## Structure du projet

```text
gestion_formation/
│
├── db.py
├── init_db.py
├── main.py
├── etudiants_gui.py
├── formations_gui.py
└── inscriptions_gui.py
````

---

## Rôle de chaque fichier

### `db.py`

Ce fichier sert à faire la connexion à la base de données SQLite.

### `init_db.py`

Ce fichier sert à créer les tables de la base de données :

* `etudiants`
* `formations`
* `inscription`

Il doit être exécuté une première fois avant de lancer l’application.

### `main.py`

C’est le fichier principal.
Il lance la fenêtre principale de l’application et permet d’accéder aux différents volets :

* gestion des étudiants
* gestion des formations
* gestion des inscriptions

### `etudiants_gui.py`

Ce fichier contient toute l’interface graphique et les traitements liés aux étudiants :

* formulaire
* tableau d’affichage
* ajout
* modification
* suppression
* recherche

### `formations_gui.py`

Ce fichier contient toute l’interface graphique et les traitements liés aux formations :

* formulaire
* tableau d’affichage
* ajout
* modification
* suppression
* recherche

### `inscriptions_gui.py`

Ce fichier contient toute l’interface graphique et les traitements liés aux inscriptions :

* choix d’un étudiant
* choix d’une formation
* inscription
* désinscription
* affichage des formations d’un étudiant
* affichage des étudiants d’une formation

---

## Méthodologie utilisée

Le travail a été fait progressivement, étape par étape.

### Étape 1

Création de la base de données avec SQLite.

### Étape 2

Mise en place des fichiers Python selon les différents volets du projet.

### Étape 3

Création d’une première version en mode console pour comprendre la logique du projet et tester les requêtes SQL.

### Étape 4

Passage à l’interface graphique avec Tkinter.

### Étape 5

Création de la fenêtre principale avec navigation entre les différents espaces.

### Étape 6

Création du volet **étudiants** avec :

* formulaire
* tableau
* boutons d’action
* liaison avec la base de données

### Étape 7

Création du volet **formations** avec le même principe.

### Étape 8

Création du volet **inscriptions** pour relier les étudiants et les formations.

### Étape 9

Amélioration du code en séparant les différentes parties dans plusieurs fichiers pour rendre le projet plus clair et plus facile à gérer.

---

## Fonctionnement général

L’application fonctionne de la manière suivante :

1. l’utilisateur lance le projet
2. la fenêtre principale s’ouvre
3. il choisit un volet dans le menu
4. il remplit le formulaire correspondant
5. les données sont enregistrées dans la base SQLite
6. les informations sont affichées dans un tableau
7. il peut ensuite modifier, supprimer ou rechercher les données

---

## Base de données

La base de données contient 3 tables :

### Table `etudiants`

Contient les informations des étudiants :

* INE
* nom
* prénom
* email
* adresse
* ville

### Table `formations`

Contient les informations des formations :

* code
* intitulé
* langue
* niveau
* objectif

### Table `inscription`

Contient les liens entre étudiants et formations :

* id_inscription
* ine_etudiant
* code_formation
* date_inscription

---

## Comment exécuter le projet

### 1. Créer la base de données

```bash
python init_db.py
```

### 2. Lancer l’application

```bash
python main.py
```

---

## Points importants

* les champs obligatoires sont contrôlés
* l’email de l’étudiant est vérifié
* les doublons sont évités pour l’INE et le code formation
* la suppression d’un étudiant ou d’une formation supprime aussi les inscriptions liées
* l’interface a été faite avec Tkinter pour respecter le TP

---

## Résultat

À la fin, on obtient une application de bureau simple, organisée et fonctionnelle, capable de gérer les étudiants, les formations et les inscriptions dans un établissement de formation.

---

## Auteur

Projet réalisé dans le cadre d’un TP de Python avec interface graphique Tkinter.

```
