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
