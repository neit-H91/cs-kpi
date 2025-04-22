# 🧠 Analyse de Performance Counter-Strike : KPIs & Data Visualisation

Bienvenue dans ce projet mêlant **data science**, **SQL**, **Python** et **e-sport** autour d’un jeu mythique : **Counter-Strike**.

## 🎯 Objectif

Ce projet vise à **extraire et analyser des données issues de près de 200 matchs professionnels** de Counter-Strike afin de produire des **KPIs** (indicateurs clés de performance) utiles à l’évaluation des performances :

- individuelles (skill brut, headshot rate, K/D…)
- collectives (exécution des objectifs, gestion économique…)
- contextuelles (zones dangereuses, efficacité des grenades…)

L’idée est de permettre à une équipe ou un joueur de se **positionner par rapport aux standards du haut niveau**, identifier ses faiblesses, et affiner son entraînement sur la base de données concrètes.

---

## 🛠️ Stack utilisée

- **Python 3**
  - `matplotlib` pour les visualisations
  - `psycopg2` pour la connexion PostgreSQL
- **PostgreSQL** pour le stockage et les requêtes SQL
- **CSDemoManager** pour l’extraction des données depuis les fichiers de démo
- **NumPy** (optionnel selon les fichiers)

---

## 📊 Contenu du dépôt

```bash
.
├── README.md                   # Ce fichier
├── assets/
│   └── inferno.png       # image utilisé dans heatmap.py
├── rapport/
│   └── Pro match analysis and KPIS.pdf       # Compte rendu avec les visuels + analyse
├── scripts/
│   ├── commands.py             # fichier avec toutes les requetes sql
│   ├── economy.py              # Analyse de l'économie
│   ├── grenades.py             # Analyse d'utilitaire
│   ├── heatmap.py              # Génération des heatmaps
│   ├── indiv.py                # Analyse individuelle
│   ├── objectives.py           # KPIs objectifs
