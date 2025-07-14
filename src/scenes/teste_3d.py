from copy import deepcopy

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageDraw

from src.objetos.segmento_de_reta import SegmentoDeReta
from src.objetos.solidos import ISolido, Triangulo
from src.objetos.vertice import Vertice3D
from src.temp.rasterizar import rasterizar_objetos

at = Vertice3D(0.5, 0.5, 0)
eye = Vertice3D(-2, 0, 2)
# vetores
up_auxiliar = Vertice3D(0, 1, 0)
n = (at - eye).normalizado()
u = n.produto_vetorial(up_auxiliar).normalizado()
v = u.produto_vetorial(n)

print(f'u: {u}\nv: {v}\nn: {n}\n')

# Matrizes de transformação do SCM para SCC
R = np.identity(4)
R[0:3, 0:3] = np.array([
    u.get_coordenadas(),
    v.get_coordenadas(),
    n.get_coordenadas(),
])
print('R:\n', R)

T = np.identity(4)
T[:3, 3] = -1 * eye.get_coordenadas()
print('T:\n', T)

# Converter SCC para SCN
H = 2
W = 4
ASPECT_RATIO = W / H
D = 1
d_near = 1.5
d_far = 4
# D = cotangente(alfa_radianos / 2)
# tan(alfa_radianos / 2) = H / (2 * D)
alfa_radianos = 2 * np.arctan(H / (2 * D))
beta_radianos = 2 * np.arctan(W / (2 * D))


def converter_vertice_para_projecao_com_profundidade(
        vertice: Vertice3D,
        tan_alfa_sobre_dois_radiano: float,
        z_near,
        z_far
        ):
    assert z_near < z_far

    A = z_far / (z_far - z_near)
    B = -A * z_near
    T_COM_PROFUNDIDADE = np.array([
        [1 / tan_alfa_sobre_dois_radiano, 0, 0, 0],
        [0, 1 / tan_alfa_sobre_dois_radiano, 0, 0],
        [0, 0, A, B],
        [0, 0, 1, 0],
    ])
    coord = vertice.get_coordenadas_homogeneas()
    new_var = T_COM_PROFUNDIDADE.dot(coord.transpose())
    # divide valores por Z
    new_var /= coord[2]
    return Vertice3D(*new_var[:-1])


def converter_solido_para_projecao(solidos: list[ISolido]) -> list[ISolido]:
    result = []
    for s in solidos:
        copia = deepcopy(s)
        vertices = copia.get_vertices()
        for i, vert in enumerate(vertices):
            vertices[i] = converter_vertice_para_projecao_com_profundidade(vert, H / (2 * D), d_near, d_far)

        result.append(copia)

    return result


def converter_scm_scc(solidos: list[ISolido], R: NDArray[np.float64], T: NDArray[np.float64]) -> list[ISolido]:
    convertidos = []
    for elemento in solidos:
        copia = deepcopy(elemento)
        vertices: NDArray[np.float64] = np.array([v.get_coordenadas_homogeneas() for v in copia.get_vertices()]).transpose()
        resultado = R.dot(T).dot(vertices).transpose()
        for i, linha in enumerate(resultado):
            copia.get_vertices()[i]._coordenadas = linha

        convertidos.append(copia)
    return convertidos


# rasterizar
def rasterizar(elementos: list[ISolido], resolucao: tuple[int, int] = (300, 300)):
    # img = np.zeros(resolucao)
    # W, H = resolucao
    img = Image.new("RGB", resolucao)
    draw = ImageDraw.Draw(img)
    draw.line
    for e in elementos:
        # rasterizar arestas
        vertices = e.get_vertices()
        for aresta in e.get_arestas():
            v1 = vertices[aresta.vertice_inicial]
            v2 = vertices[aresta.vertice_final]
            xy = [
                v1.get_coordenadas()[:2],
                v2.get_coordenadas()[:2]
            ]
            draw.line(xy)
            
    return img


# Objetos no SCM
r1 = SegmentoDeReta(Vertice3D(1, 0, 0), str_cor="red")
r2 = SegmentoDeReta(Vertice3D(0, 1, 0), str_cor='green')
t1 = Triangulo(
    Vertice3D(0, 0, 0),
    Vertice3D(0, 0.5, 0),
    Vertice3D(0.5, 0, 0),
)

# r1_vertices = np.array([v.get_coordenadas_homogeneas() for v in r1.get_vertices()]).transpose()
# r1_scc = R.dot(T).dot(r1_vertices)
r1_scc = converter_scm_scc([r1, r2, t1], R, T)
r1_projetado = converter_solido_para_projecao(r1_scc)
# print(r1_projetado[0])
img = rasterizar_objetos([
        (np.array([v.get_coordenadas() for v in e.get_vertices()]), e.get_arestas(), e.get_faces())
        for e in r1_projetado
    ])

from matplotlib import pyplot as plt

plt.imshow(img)
img.save('temp_image.png')
