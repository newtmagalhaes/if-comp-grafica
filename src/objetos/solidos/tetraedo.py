from ..vertice import IVertice
from .isolido import ISolido
from .item_aresta import ItemAresta
from .item_face import ItemFace


class Tetraedro(ISolido):
    def __init__(self, p1: IVertice, p2: IVertice, p3: IVertice, p4: IVertice) -> None:
        # self._validar_vertices(p1, p2, p3, p4)
        self._vertices = [p1, p2, p3, p4]
        self._arestas = [
            ItemAresta(0, 1),
            ItemAresta(1, 2),
            ItemAresta(2, 0),
            ItemAresta(0, 3),
            ItemAresta(1, 3),
            ItemAresta(2, 3),
        ]
        self._faces = [
            ItemFace([0, 1, 2]),
            ItemFace([0, 4, 3]),
            ItemFace([1, 5, 4]),
            ItemFace([2, 3, 5]),
        ]

    def get_vertices(self) -> list[IVertice]:
        return self._vertices

    def get_arestas(self) -> list[ItemAresta]:
        return self._arestas

    def get_faces(self) -> list[ItemFace]:
        return self._faces
