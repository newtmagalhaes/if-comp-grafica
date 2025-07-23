import numpy as np

from src.objetos.colorset import ColorName
from src.objetos.solidos.item_aresta import ItemAresta
from src.objetos.solidos.item_face import ItemFace
from src.objetos.vertice import IVertice, Vertice3D

from .isolido import ISolido


class Cilindro(ISolido):
    def __init__(
            self,
            radius: float,
            height: float,
            segments: int = 20,
            origin: Vertice3D = Vertice3D.ORIGEM(),
            edge_color: ColorName = "purple",
            face_color: ColorName = "purple",
            ):
        self.radius = radius
        self.height = height
        self.segments = segments
        self.origin = origin
        self.edge_color = edge_color
        self.face_color = face_color

        x0, y0, z0 = self.origin.get_coordenadas()

        # Ângulos igualmente espaçados para os vértices circulares
        self.angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)

        # Base inferior (z = z0)
        base = np.array([
            [x0 + radius * np.cos(a), y0 + radius * np.sin(a), z0]
            for a in self.angles
        ])
        # Base superior (z = z0 + altura)
        top = base.copy()
        top[:, 2] = z0 + height

        self._vertices = [Vertice3D(*coords) for coords in np.vstack([base, top])]

        # Faces: base, topo, laterais (como quads)
        faces = [
            # face inferior
            ItemFace(list(range(0, 3 * segments, 3)), face_color),
            # face superior
            ItemFace(list(range(1, 3 * segments, 3)), face_color),
        ]
        # Arestas: círculo da base, círculo do topo, verticais
        arestas = []
        for vertice_atual in range(segments):
            vertice_seguinte = (vertice_atual + 1) % segments
            vertice_topo = (vertice_atual + segments)
            vertice_topo_seguinte = vertice_seguinte + segments
            arestas.append(ItemAresta(vertice_atual, vertice_seguinte, edge_color))  # base
            arestas.append(ItemAresta(vertice_topo, vertice_topo_seguinte, edge_color))  # topo
            arestas.append(ItemAresta(vertice_seguinte, vertice_topo_seguinte, edge_color))  # lateral

            posicao_aresta_base = 3 * vertice_atual
            faces.append(ItemFace([
                posicao_aresta_base,
                (posicao_aresta_base + 2) % (3 * segments),
                -1 * ((posicao_aresta_base + 1) % (3 * segments)),
                -1 * ((posicao_aresta_base - 1) % (3 * segments)),
            ], face_color))

        self._faces = faces
        self._arestas = arestas

    def get_vertices(self) -> list[IVertice]:
        return self._vertices

    def get_arestas(self) -> list[ItemAresta]:
        return self._arestas

    def get_faces(self) -> list[ItemFace]:
        return self._faces
