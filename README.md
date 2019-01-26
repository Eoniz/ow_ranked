# ow_ranked
Simple application web permettant de pouvoir avoir un suivi de son rang sur Overwatch.

## Données et algorithme
Toutes les données ont étés récoltés "à la main" afin de trouver des corrélations entre les
valeurs et le rang.
Ainsi, avec l'algorithme du classement Elo, on arrive à obtenir une courbe parfaite de prédiction, ainsi, on peut déterminer la valeur de la MMR pour un joueur.

Toutes les données sont disponibles ici sur la feuille 2 : https://docs.google.com/spreadsheets/d/1vwVGdyboEKtpaqpl8585BxpYN4fdMvPgQGZqQqU43Ks/edit?usp=sharing

## Technos
Python, Flask, Pytest, SQLAlchemy, SQLite, Bootstrap

## Tests
Les tests sont disponibles dans le dossier tests/