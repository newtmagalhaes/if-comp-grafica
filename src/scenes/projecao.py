from dataclasses import dataclass


@dataclass
class Projecao:
    # W
    largura: int = 300
    # H
    altura: int = 300

    @property
    def proporcao(self) -> float:
        return self.altura / self.largura
