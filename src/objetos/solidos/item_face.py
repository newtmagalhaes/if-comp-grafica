from dataclasses import dataclass

from ..colorset import ColorName


@dataclass
class ItemFace:
    arestas: list[int]
    cor: ColorName = 'black'

    def __getitem__(self, key: int) -> int:
        return self.arestas[key]
