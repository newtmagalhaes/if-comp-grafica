from dataclasses import dataclass

from ..colorset import ColorName


@dataclass
class ItemAresta:
    vertice_inicial: int
    vertice_final: int
    cor: ColorName = 'black'

    def __getitem__(self, key: int) -> int:
        if key == 0:
            return self.vertice_inicial

        if key == 1:
            return self.vertice_final

        raise ValueError(f'Valor deve ser 0 ou 1, foi passado "{key}"')

    def __mul__(self, other: int):
        if other == 1:
            return self
        elif other == -1:
            return ItemAresta(self.vertice_final, self.vertice_inicial, self.cor)
        raise Exception(f'número invalido "{other}"')
