import commands
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# --- SCATTER PLOT : Performance individuelle des joueurs ---
data = commands.get_indiv_kpi()

# Extraction des colonnes
steam_ids = [row[0] for row in data]
match_counts = [int(row[1]) for row in data]
avg_kd = [float(row[2]) for row in data]
avg_hs = [float(row[3]) for row in data]

# Création de la figure pour le scatter plot
fig1, ax1 = plt.subplots(figsize=(10, 6))

# Scatter plot avec color mapping sur le nombre de matchs
scatter = ax1.scatter(avg_kd, avg_hs, c=match_counts, cmap='viridis', s=10, alpha=0.8, edgecolors='black')

# Colorbar pour le nombre de matchs
cbar = plt.colorbar(scatter, ax=ax1)
cbar.set_label('Nombre de matchs')

# Moyenne générale
mean_kd = np.mean(avg_kd)
mean_hs = np.mean(avg_hs)
scatter_center = ax1.scatter(mean_kd, mean_hs, color='red', s=100)


# Labels et légende
ax1.set_xlabel('K/D moyen')
ax1.set_ylabel('% Headshots moyen')
ax1.set_title('Performance individuelle des joueurs')
ax1.legend([scatter_center], [f'Centre de Gravité ({mean_kd:.2f}, {mean_hs:.2f})'], loc='upper right')

# Affichage du premier graphe
plt.tight_layout()
plt.show()


# --- HISTOGRAMME : Distribution des éliminations par joueur ---
data_elim = commands.get_elim_distrib()
flat_data = [item[0] for item in data_elim]

# Stats
mode_result = stats.mode(flat_data, keepdims=True)
mode = mode_result.mode[0]
median = np.median(flat_data)
mean = np.mean(flat_data)

# Création de la figure pour l'histogramme
fig2, ax2 = plt.subplots(figsize=(10, 6))

# Histogramme
ax2.hist(flat_data, bins=range(0, max(flat_data)+2), color='skyblue', edgecolor='black', align='left')

# Lignes de stats
ax2.axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f'Moyenne: {mean:.2f}')
ax2.axvline(median, color='green', linestyle='dashed', linewidth=2, label=f'Médiane: {median:.2f}')
ax2.axvline(mode, color='orange', linestyle='dashed', linewidth=2, label=f'Mode: {mode}')

# Labels, titre, légende
ax2.set_xlabel("Kills par joueur dans un match")
ax2.set_ylabel("Fréquence")
ax2.set_title("Distribution des éliminations par joueur (par match)")
ax2.legend()
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# Affichage du deuxième graphe
plt.tight_layout()
plt.show()


# Récupérer les données
data = commands.get_clutch_ratios()

# Transformer les données
labels = [f'1v{row[0]}' for row in data]
values = [row[3] for row in data] 

plt.figure(figsize=(8, 5))
plt.bar(labels, values)
plt.yscale('log')  # échelle logarithmique
plt.ylabel('Ratio de victoire (log)')
for i, d in enumerate(values):
    plt.text(i, d, str(d), ha='center', weight='bold')
plt.title('Ratio de victoire en situation de clutch (log scale)')
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.show()