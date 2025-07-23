import numpy as np

from src.objetos.colorset import ColorName
from src.objetos.solidos.item_aresta import ItemAresta
from src.objetos.solidos.item_face import ItemFace
from src.objetos.vertice import IVertice, Vertice3D

from .isolido import ISolido


class Cilindro(ISolido):
    def __init__(
            self,
            raio: float,
            altura: float,
            segmentos: int = 20,
            origem: Vertice3D = Vertice3D.ORIGEM(),
            cor_arestas: ColorName = "purple",
            cor_faces: ColorName = "purple",
            ):
        self.raio = raio
        self.altura = altura
        self.segmentos = segmentos
        self.origem = origem
        self.cor_arestas = cor_arestas
        self.cor_faces = cor_faces

        x0, y0, z0 = self.origem.get_coordenadas()

        # Ângulos igualmente espaçados para os vértices circulares
        self.angles = np.linspace(0, 2 * np.pi, segmentos, endpoint=False)

        # Base inferior (z = z0)
        base = np.array([
            [x0 + raio * np.cos(a), y0 + raio * np.sin(a), z0]
            for a in self.angles
        ])
        # Base superior (z = z0 + altura)
        top = base.copy()
        top[:, 2] = z0 + altura

        self._vertices = [Vertice3D(*coords) for coords in np.vstack([base, top])]

        # Faces: base, topo, laterais (como quads)
        faces = [
            # face inferior
            ItemFace(list(range(0, 3 * segmentos, 3)), cor_faces),
            # face superior
            ItemFace(list(range(1, 3 * segmentos, 3)), cor_faces),
        ]
        # Arestas: círculo da base, círculo do topo, verticais
        arestas = []
        for vertice_atual in range(segmentos):
            vertice_seguinte = (vertice_atual + 1) % segmentos
            vertice_topo = (vertice_atual + segmentos)
            vertice_topo_seguinte = vertice_seguinte + segmentos
            arestas.append(ItemAresta(vertice_atual, vertice_seguinte, cor_arestas))  # base
            arestas.append(ItemAresta(vertice_topo, vertice_topo_seguinte, cor_arestas))  # topo
            arestas.append(ItemAresta(vertice_seguinte, vertice_topo_seguinte, cor_arestas))  # lateral

            posicao_aresta_base = 3 * vertice_atual
            faces.append(ItemFace([
                posicao_aresta_base,
                (posicao_aresta_base + 2) % (3 * segmentos),
                -1 * ((posicao_aresta_base + 1) % (3 * segmentos)),
                -1 * ((posicao_aresta_base - 1) % (3 * segmentos)),
            ], cor_faces))

        self._faces = faces
        self._arestas = arestas

    def get_vertices(self) -> list[IVertice]:
        return self._vertices

    def get_arestas(self) -> list[ItemAresta]:
        return self._arestas

    def get_faces(self) -> list[ItemFace]:
        return self._faces
