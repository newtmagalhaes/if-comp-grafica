from .colorset import ColorName
from .solidos.isolido import ISolido
from .solidos.item_aresta import ItemAresta
from .solidos.item_face import ItemFace
from .vertice import IVertice


class SegmentoDeReta(ISolido):
    def __init__(
            self,
            ponto_inicial: IVertice,
            ponto_final: IVertice | None = None,
            str_cor: ColorName = "black"):

        if ponto_final is None:
            ponto_final = ponto_inicial
            ponto_inicial = ponto_inicial.ORIGEM()

        if ponto_inicial == ponto_final:
            raise ValueError('Segmento de reta não pode ter comprimento 0')

        self._vertices = [ponto_inicial, ponto_final]
        self._arestas = [ItemAresta(0, 1, str_cor)]
        self._cor = str_cor
        self.comprimento = ponto_inicial.distance(ponto_final)

    def get_vertices(self) -> list[IVertice]:
        return self._vertices

    def get_arestas(self) -> list[ItemAresta]:
        return self._arestas

    def get_faces(self) -> list[ItemFace]:
        return []
