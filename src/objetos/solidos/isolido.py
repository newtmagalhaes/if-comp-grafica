from abc import ABC, abstractmethod

from ..vertice import IVertice
from .item_aresta import ItemAresta
from .item_face import ItemFace


class ISolido(ABC):
    @abstractmethod
    def get_vertices(self) -> list[IVertice]: ...

    @abstractmethod
    def get_arestas(self) -> list[ItemAresta]: ...

    @abstractmethod
    def get_faces(self) -> list[ItemFace]: ...

    def centro(self) -> IVertice:
        numero_vertices = len(self.get_vertices())
        return sum(self.get_vertices(), start=self.get_vertices()[0].ORIGEM()) / numero_vertices
