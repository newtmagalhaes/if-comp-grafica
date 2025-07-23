import numpy as np
from PIL import Image

from src.objetos.solidos.isolido import ISolido
from src.objetos.vertice import Vertice3D

from .conversor_scc_scp import ConversorSCCparaSCPcomProfundidade
from .conversor_scm_scc import ConversorSCMparaSCC
from .rasterizar import rasterizar


class Pipeline:
    def __init__(
            self,
            classe_conversor_scc=ConversorSCMparaSCC,
            classe_conversor_scp=ConversorSCCparaSCPcomProfundidade,
            ) -> None:
        self._classe_conversor_scc = classe_conversor_scc
        self._classe_conversor_scp = classe_conversor_scp

    def render(
            self,
            solidos: list[ISolido],
            eye: Vertice3D,
            at: Vertice3D | None = None,
            resolucao: tuple[int, int] = (300, 300),
            ) -> Image.Image:
        # setup
        if at is None:
            at = np.mean([s.centro() for s in solidos])

        self.conversor_scc = self._classe_conversor_scc(eye, at)
        self.conversor_scp = self._classe_conversor_scp()

        solidos_scc = self.conversor_scc.converter(solidos)
        solidos_scp = self.conversor_scp.converter(solidos_scc)
        return rasterizar(solidos_scp, self.conversor_scc.n, resolucao)
