import numpy as np
from matplotlib import pyplot as plt

from src.objetos.solidos import Cilindro, Cubo, ISolido
from src.objetos.vertice import Vertice3D
from src.pipeline import Pipeline

c = Cubo.criar_em(Vertice3D(0, 0, 0), 1)
c2 = Cilindro(0.5, 2, origem=Vertice3D(3, 0, 0), cor_arestas='black')

solidos: list[ISolido] = [
    c,
    c2,
]

angles = np.linspace(0, np.pi / 2, 10, endpoint=False)
radius = 8
x0, y0, z0 = 0, 0, 0
eyes = np.array([
    Vertice3D(x0 + radius * np.cos(a), y0 + radius * np.sin(a), z0)
    for a in angles
])

fig, ax = plt.subplots(1, len(eyes), figsize=(len(eyes) * 4, 4))
for i, temp_eye in enumerate(eyes):
    pipe = Pipeline()
    img = pipe.render(solidos, temp_eye, Vertice3D.ORIGEM(), (300, 300))
    ax[i].imshow(img)
    img.save(f'img/rotate-{i}.png')

plt.tight_layout()
plt.show()
