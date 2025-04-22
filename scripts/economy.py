import commands
import matplotlib.pyplot as plt

# Récupération et préparation des données
data0 = commands.get_eco_distrib()
data1 = commands.get_eco_kills()

labels0, ratios0 = zip(*[(d[0], float(d[1])) for d in data0])
labels1, ratios1 = zip(*[(d[0], float(d[1])) for d in data1])

# Fonction pour formater les pourcentages dans le camembert
def get_ratio(a):
    return str(a)[:4]

# --- Graphique 1 : Camembert de la distribution économique ---
fig1, ax1 = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax1.pie(
    ratios0,
    labels=labels0,
    autopct=get_ratio,
    normalize=True,
    textprops={'color': 'w', 'weight': 'bold'}
)
ax1.set_title("Distribution Économique", fontsize=14, weight='bold')
ax1.legend(wedges, labels0, title="Types d'Achat", loc='center left', bbox_to_anchor=(1, 0.5))

# Affichage du premier graphe
plt.tight_layout()
plt.show()

# --- Graphique 2 : Bar chart des kills par économie ---
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.bar(range(len(data1)), ratios1, width=0.4)

for i, d in enumerate(ratios1):
    ax2.text(i, d + 0.01, str(d), ha='center', weight='bold')

ax2.set_ylim(top=max(ratios1) + 0.1)
ax2.set_xticks(range(len(data1)))
ax2.set_xticklabels(labels1)
ax2.set_title("Eliminations moyennes en fonction de l'économie", fontsize=14, weight='bold')
ax2.set_ylabel("Ratio d'éliminations")

# Affichage du deuxième graphe
plt.tight_layout()
plt.show()
