from matplotlib import pyplot as plt

from src.objetos.solidos import Cilindro, Cubo
from src.objetos.vertice import Vertice3D
from src.pipeline import Pipeline

EYE = Vertice3D(7, 7, -5)
RESOLUCOES = [
    (50, 50),
    (100, 100),
    (300, 300),
    (900, 900),
]

paralelepipedo = Cubo.criar_em(
    Vertice3D(0, 0, 0),
    largura=3,
    altura=4,
    profundidade=5,
    cor_faces='blue',
    cor_arestas='blue'
)
cilindro = Cilindro(
    raio=1,
    altura=3,
    segmentos=20,
    origem=Vertice3D(5, 5, 2),
)
SOLIDOS = [
    paralelepipedo,
    cilindro,
]
pipe = Pipeline()

n_resolucoes = len(RESOLUCOES)
fig, ax = plt.subplots(1, n_resolucoes, figsize=(n_resolucoes * 4, 4))
for i, r in enumerate(RESOLUCOES):
    img = pipe.render(SOLIDOS, EYE, resolucao=r)
    ax[i].imshow(img)
    ax[i].set_title('{} x {}'.format(*r))

fig.savefig('output/resolucoes.png')
plt.show()
