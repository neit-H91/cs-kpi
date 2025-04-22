import commands
import matplotlib.pyplot as plt

# --- BAR CHART : Efficacité de l'utilitaire (grenades) ---

# Récupération et préparation des données
data = commands.get_grenade_kpis()
labels, ratios = zip(*[(d[0], float(d[1])) for d in data])

# Création du bar chart
plt.figure(figsize=(8, 5))
plt.bar(range(len(data)), ratios, color='darkorange')

# Affichage des valeurs sur les barres
for i, val in enumerate(ratios):
    plt.text(i, val + 0.2, str(val)[:5], ha='center', color='b', weight='bold')

# Ajustement de l'axe Y pour meilleure lisibilité
plt.ylim(top=max(ratios) + 5)

# Labels de l'axe X
plt.xticks(range(len(data)), labels=labels)

# Titre du graphique
plt.title("Efficacité de l'utilitaire (grenades)")
plt.ylabel("Valeur moyenne par match")
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Affichage
plt.tight_layout()
plt.show()
