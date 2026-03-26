import sqlite3

def connexion_bd():
    return sqlite3.connect("gestion_formation.db")