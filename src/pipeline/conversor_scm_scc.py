from copy import deepcopy

import numpy as np

from src.objetos import Vertice3D
from src.objetos.solidos.isolido import ISolido


class ConversorSCMparaSCC:
    def __init__(
            self,
            posicao_camera: Vertice3D,
            posicao_at: Vertice3D,
            ) -> None:
        # vetores
        up_auxiliar = Vertice3D(0, 1, 0)
        n = (posicao_at - posicao_camera).normalizado()
        u = n.produto_vetorial(up_auxiliar).normalizado()
        v = u.produto_vetorial(n)
        self.n = n
        self.u = u
        self.v = v

        # Matrizes de transformação do SCM para SCC
        self.R = np.identity(4)
        self.R[0:3, 0:3] = np.array([
            u.get_coordenadas(),
            v.get_coordenadas(),
            n.get_coordenadas(),
        ])

        self.T = np.identity(4)
        self.T[:3, 3] = -1 * posicao_camera.get_coordenadas()

        self.RT = self.R.dot(self.T)

    def converter(self, solidos: list[ISolido]) -> list[ISolido]:
        convertidos = []
        for elemento in solidos:
            vertices = np.array([
                v.get_coordenadas_homogeneas()
                for v in elemento.get_vertices()
            ], dtype=np.float64).transpose()
            resultado = self.RT.dot(vertices).transpose()

            copia = deepcopy(elemento)
            # TODO: criar melhor forma de fazer ISolidos a partir da lista de vertices
            for i, linha in enumerate(resultado):
                copia.get_vertices()[i]._coordenadas = linha

            convertidos.append(copia)
        return convertidos
