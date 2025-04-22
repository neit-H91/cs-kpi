import commands
import matplotlib.pyplot as plt

# --- BAR CHART : Ratios liés aux objectifs de round ---

# Récupération et traitement des données
data = commands.get_bomb_perf()
labels, ratios = zip(*[(d[0], float(d[1])) for d in data])

# Création du bar chart
plt.figure(figsize=(8, 5))
plt.bar(range(len(data)), ratios, color='mediumseagreen')

# Affichage des valeurs sur les barres
for i, val in enumerate(ratios):
    plt.text(i, val + 0.02, str(val)[:5], ha='center', color='b', weight='bold')

# Ajustement de l'axe Y
plt.ylim(top=max(ratios) + 0.1)

# Personnalisation des labels
plt.xticks(range(len(data)), labels=labels)

# Titre et légendes
plt.title("Ratios d'exécution et de réussite des objectifs")
plt.ylabel("Ratio moyen par round")
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Affichage
plt.tight_layout()
plt.show()
