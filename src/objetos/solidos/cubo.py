from numbers import Number

from src.objetos.vertice import IVertice

from ..colorset import ColorName
from ..vertice import Vertice3D
from .isolido import ISolido
from .item_aresta import ItemAresta
from .item_face import ItemFace


class Cubo(ISolido):
    @classmethod
    def criar_em(
            cls,
            vertice: Vertice3D,
            largura: Number,
            altura: Number | None = None,
            profundidade: Number | None = None,
            cor_arestas: ColorName | None = None,
            cor_faces: ColorName | None = None,
            ):
        altura = altura or largura
        profundidade = profundidade or largura

        x, y, z = vertice.get_coordenadas()
        vertices = [
            vertice,
            Vertice3D(x + largura, y, z),
            Vertice3D(x + largura, y, z + profundidade),
            Vertice3D(x, y, z + profundidade),
            Vertice3D(x, y + altura, z),
            Vertice3D(x + largura, y + altura, z),
            Vertice3D(x + largura, y + altura, z + profundidade),
            Vertice3D(x, y + altura, z + profundidade),
        ]
        return Cubo(*vertices, cor_arestas=cor_arestas, cor_faces=cor_faces)

    def __init__(
            self,
            *vertices: Vertice3D,
            cor_arestas: ColorName | None = None,
            cor_faces: ColorName | None = None
            ):
        cor_arestas = cor_arestas or 'black'
        cor_faces = cor_faces or 'blue'

        assert self._check_vertices(vertices)

        self._vertices = [*vertices]
        self._arestas = [
            ItemAresta(0, 1, cor_arestas), ItemAresta(1, 2, cor_arestas), ItemAresta(2, 3, cor_arestas), ItemAresta(3, 0, cor_arestas),
            ItemAresta(4, 5, cor_arestas), ItemAresta(5, 6, cor_arestas), ItemAresta(6, 7, cor_arestas), ItemAresta(7, 4, cor_arestas),
            ItemAresta(0, 4, cor_arestas), ItemAresta(1, 5, cor_arestas), ItemAresta(2, 6, cor_arestas), ItemAresta(3, 7, cor_arestas),
        ]
        self._faces = [
            ItemFace([0, 1, 2, 3], cor_faces),
            ItemFace([4, 5, 6, 7], cor_faces),
            ItemFace([0, 9, -4, -8], cor_faces),
            ItemFace([1, 10, -5, -9], cor_faces),
            ItemFace([2, 11, -6, -10], cor_faces),
            ItemFace([3, 8, -7, -11], cor_faces),
        ]

    def _check_vertices(self, vertices) -> bool:
        """Checa se são 8 vertices válidos para um cubo"""
        return len(vertices) == 8

    def get_vertices(self) -> list[IVertice]:
        return self._vertices  # type: ignore

    def get_arestas(self) -> list[ItemAresta]:
        return self._arestas

    def get_faces(self) -> list[ItemFace]:
        return self._faces
