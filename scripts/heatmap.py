import commands
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.ndimage import gaussian_filter

# scatter pour position mort ct sur inferno
#preparation img
img = mpimg.imread("assets/inferno.jpg")

# Points de calibration
game_coords = np.array([
    [-1520.06, 430.89],
    [-569.97, 909.97],
    [400.04, 2119.97],
    [2298.03, 1328.04],
    [2076.03, -526.54],
    [279.03, -713.97]
])

pixel_coords = np.array([
    [96, 570],
    [249, 486],
    [408, 287],
    [721, 419],
    [685, 725],
    [388, 756]
])

# Résolution de la transformation affine
A = np.hstack((game_coords, np.ones((game_coords.shape[0], 1))))
B = pixel_coords
params, _, _, _ = np.linalg.lstsq(A, B, rcond=None)  # shape (3,2)
transform = lambda x, y: np.dot(np.array([x, y, 1]), params)

data = commands.get_inferno_ct_deaths()
data_transformed = [transform(x, y) for x, y in data]
x_pixel, y_pixel = zip(*data_transformed)

# Créer une heatmap vide de la taille de l'image
heatmap, _, _ = np.histogram2d(
    x_pixel, y_pixel,
    bins=[img.shape[1], img.shape[0]],
    range=[[0, img.shape[1]], [0, img.shape[0]]]
)

# Appliquer un flou gaussien
heatmap = gaussian_filter(heatmap, sigma=4)

# Normaliser la heatmap entre 0 et 1
heatmap_norm = heatmap / np.max(heatmap)

# Créer l'image RGBA à partir du colormap
cmap = plt.get_cmap('plasma')
heatmap_rgba = cmap(heatmap_norm)

# Masquer les valeurs faibles
heatmap_rgba[..., 3] = np.where(heatmap_norm > 0.0001, heatmap_norm, 0)

# Transposer pour corriger l’orientation
heatmap_rgba = np.transpose(heatmap_rgba, (1, 0, 2))

# Affichage
fig, ax = plt.subplots()
ax.imshow(img)
ax.imshow(heatmap_rgba, interpolation='nearest')
ax.set_xlim(0, img.shape[1])
ax.set_ylim(img.shape[0], 0)  # Inverser l'axe y
plt.title("Heatmap morts des défenseurs sur inferno")
plt.show()