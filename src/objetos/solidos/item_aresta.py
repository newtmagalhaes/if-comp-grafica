from dataclasses import dataclass

from ..colorset import ColorName


@dataclass
class ItemAresta:
    vertice_incial: int
    vertice_final: int
    cor: ColorName = 'black'

    def __getitem__(self, key: int) -> int:
        if key == 0:
            return self.vertice_incial

        if key == 1:
            return self.vertice_final

        raise ValueError(f'Valor deve ser 0 ou 1, foi passado "{key}"')
