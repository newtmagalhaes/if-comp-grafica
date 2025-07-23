from matplotlib import pyplot as plt

from src.objetos.segmento_de_reta import SegmentoDeReta
from src.objetos.solidos import Cilindro, Cubo, ISolido, Tetraedro, Triangulo
from src.objetos.vertice import Vertice3D
from src.pipeline import Pipeline
from src.temp.pipeline import plot3D

# Objetos no SCM
r1 = SegmentoDeReta(Vertice3D(1, 0, 0), str_cor="red")
r2 = SegmentoDeReta(Vertice3D(0, 1, 0), str_cor='green')
t1 = Triangulo(
    Vertice3D(0, 0, 0),
    Vertice3D(0, 0.5, 0),
    Vertice3D(0.5, 0, 0),
)
t2 = Tetraedro(
    Vertice3D(1, 0, 0),
    Vertice3D(1, 1, 0),
    Vertice3D(1, 0, 1),
    Vertice3D(2, 1, 1.5),
)
c = Cubo.criar_em(Vertice3D(0, 0, 0), 1)  # type: ignore
c2 = Cilindro(0.5, 2, origem=Vertice3D(3, 0, 0), cor_arestas='black')

solidos: list[ISolido] = [
    c,
    c2,
    # t2,
    # r1,
    # r2,
    # t1,
]
new_eye = Vertice3D(-3, -3, -5)

resolucoes = [
    (300, 300),
    (600, 600),
    (900, 900),
]
fig, ax = plt.subplots(1, 3, figsize=(12, 4))
for i, r in enumerate(resolucoes):
    pipe = Pipeline()
    img = pipe.render(solidos, new_eye, resolucao=r)
    ax[i].imshow(img)

plot3D([(s.get_vertices(), s.get_arestas(), s.get_faces()) for s in [c, c2]])
plt.tight_layout()
plt.show()
fig.savefig('temp.png')
