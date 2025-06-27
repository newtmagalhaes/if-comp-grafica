from src.objetos.segmento_de_reta import SegmentoDeReta
from src.objetos.vertice import Vertice3D

r1 = SegmentoDeReta(Vertice3D(1, 0, 0), str_cor="red")
r2 = SegmentoDeReta(Vertice3D(0, 1, 0), str_cor='green')

at = Vertice3D(0.5, 0.5, 0)
eye = Vertice3D(-2, 0, 2)
# vetores
up_auxiliar = Vertice3D(0, 1, 0)
n = (at - eye).normalizado()
u = n.produto_vetorial(up_auxiliar).normalizado()
v = u.produto_vetorial(n)

print(f'u: {u}\nv: {v}\nn: {n}')
