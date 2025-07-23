from dataclasses import dataclass

from ..colorset import ColorName
from .item_aresta import ItemAresta


@dataclass
class ItemFace:
    arestas: list[int]
    cor: ColorName = 'black'

    def __getitem__(self, key: int) -> int:
        return self.arestas[key]

    def get_arestas(self, arestas: list[ItemAresta]) -> list[ItemAresta]:
        result = []
        for i_aresta in self.arestas:
            if tem_reverso := (i_aresta < 0):
                i_aresta *= -1
            result.append(arestas[i_aresta] * pow(-1, tem_reverso))

        return result
