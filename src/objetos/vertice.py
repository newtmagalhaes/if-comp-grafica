from abc import ABC, abstractmethod
from numbers import Number
from typing import Self

import numpy as np
from numpy.typing import NDArray


class IVertice(ABC):
    """Interface de vértice

    Contém as definições de operações básicas entre vértices
    """
    _DEFAULT_VALUE_ERROR = 'Tipo "%s" não é feito para esta operação'

    @classmethod
    def ORIGEM(cls):
        if cls._ORIGEM is None:
            cls._ORIGEM = cls(*np.zeros(cls.get_numero_dimensoes()))
        return cls._ORIGEM

    @classmethod
    @abstractmethod
    def get_numero_dimensoes(cls) -> int: ...

    @abstractmethod
    def get_coordenadas(self) -> NDArray[np.float64]: ...

    @abstractmethod
    def get_coordenadas_homogeneas(self) -> NDArray[np.float64]: ...

    def distance(self, other) -> Number:
        assert isinstance(other, self.__class__), self._DEFAULT_VALUE_ERROR % type(other)
        diferencas = self.get_coordenadas() - other.get_coordenadas()
        quadrados_dos_catetos = np.square(diferencas)
        return np.sqrt(quadrados_dos_catetos.sum())

    def modulo(self) -> Number:
        return self.distance(self.ORIGEM())

    def normalizado(self):
        return self / self.modulo()

    def __str__(self) -> str:
        return f'Vertice{self.get_numero_dimensoes()}D{self.get_coordenadas()}'

    def __add__(self, other):
        assert isinstance(other, self.__class__), self._DEFAULT_VALUE_ERROR % type(other)
        soma = self.get_coordenadas() + other.get_coordenadas()
        return self.__class__(*soma)

    def __sub__(self, other):
        assert isinstance(other, self.__class__), self._DEFAULT_VALUE_ERROR % type(other)
        diferenca = self.get_coordenadas() - other.get_coordenadas()
        return self.__class__(*diferenca)

    def __truediv__(self, other: Number | int | float):
        assert isinstance(other, Number)
        quociente = self.get_coordenadas() / other  # type: ignore
        return self.__class__(*quociente)

    def __mul__(self, other: int | float):
        assert isinstance(other, Number)
        produto = self.get_coordenadas() * other
        return self.__class__(*produto)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return all(a == b for a, b in zip(self.get_coordenadas(), other.get_coordenadas()))
        return False

    def __getitem__(self, key: int):
        return self.get_coordenadas()[key]


class Vertice2D(IVertice):
    _ORIGEM = None

    def __init__(self, x: float, y: float) -> None:
        self._coordenadas = np.array([x, y, 1], dtype=np.float64)

    def get_coordenadas(self) -> NDArray[np.float64]:
        return self._coordenadas[:2]

    def get_coordenadas_homogeneas(self):
        return self._coordenadas

    @classmethod
    def get_numero_dimensoes(cls) -> int:
        return 2


class Vertice3D(IVertice):
    _ORIGEM = None

    def __init__(self, x: float, y: float, z: float) -> None:
        self._coordenadas = np.array([x, y, z, 1], dtype=np.float64)

    def get_coordenadas(self) -> NDArray[np.float64]:
        return self._coordenadas[:3]

    def get_coordenadas_homogeneas(self):
        return self._coordenadas

    @classmethod
    def get_numero_dimensoes(cls) -> int:
        return 3

    def produto_vetorial(self, other: Self):
        assert isinstance(other, Vertice3D)
        result = np.cross(self.get_coordenadas(), other.get_coordenadas())
        return self.__class__(*result)
