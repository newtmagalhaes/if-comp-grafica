from copy import deepcopy

import numpy as np

from src.objetos import Vertice3D
from src.objetos.solidos.isolido import ISolido


class ConversorSCCparaSCPcomProfundidade:
    """Converte para o Sistema de Coordenadas de Projeção com profundidade"""

    def __init__(
            self,
            altura=2,
            largura=4,
            d_projecao=1,
            d_near=1,
            d_far=5,
            ) -> None:
        assert d_projecao <= d_near <= d_far

        self.H = altura
        self.W = largura
        self.ASPECT_RATIO = largura / altura
        self.D = d_projecao
        self.d_near = d_near
        self.d_far = d_far
        self.alfa_radianos = 2 * np.arctan(altura / (2 * d_projecao))
        self.beta_radianos = 2 * np.arctan(largura / (2 * d_projecao))

    def _converter_vertice_para_projecao_com_profundidade(self, vertice: Vertice3D):
        tan_alfa_sobre_dois_radiano = self.H / (2 * self.D)

        A = self.d_far / (self.d_far - self.d_near)
        B = -A * self.d_near
        T_COM_PROFUNDIDADE = np.array([
            [1 / tan_alfa_sobre_dois_radiano, 0, 0, 0],
            [0, 1 / tan_alfa_sobre_dois_radiano, 0, 0],
            [0, 0, A, B],
            [0, 0, 1, 0],
        ])
        coord = vertice.get_coordenadas_homogeneas()
        new_var = T_COM_PROFUNDIDADE.dot(coord.transpose())
        # divide valores por Z
        new_var /= coord[2]
        return Vertice3D(*new_var[:-1])

    def converter(self, solidos: list[ISolido]) -> list[ISolido]:
        result = []
        for s in solidos:
            copia = deepcopy(s)
            vertices = copia.get_vertices()
            for i, vert in enumerate(vertices):
                vertices[i] = self._converter_vertice_para_projecao_com_profundidade(vert)

            result.append(copia)

        return result
