from .isolido import ISolido
from .item_aresta import ItemAresta
from .item_face import ItemFace
from ..vertice import IVertice


class Triangulo(ISolido):
    def __init__(self, p1: IVertice, p2: IVertice, p3: IVertice) -> None:
        self._vertices = [p1, p2, p3]
        self._arestas = [
            ItemAresta(0, 1, "red"),
            ItemAresta(1, 2),
            ItemAresta(2, 0)
        ]
        self._faces = [ItemFace([0, 1, 2], "green")]

    def get_vertices(self) -> list[IVertice]:
        return self._vertices

    def get_arestas(self) -> list[ItemAresta]:
        return self._arestas

    def get_faces(self) -> list[ItemFace]:
        return self._faces
