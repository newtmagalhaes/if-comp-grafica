from src.objetos.segmento_de_reta import SegmentoDeReta
from src.objetos.solidos.triangulo import Triangulo
from src.objetos.vertice import Vertice2D
from src.temp.pipeline import plot2D

r = SegmentoDeReta(Vertice2D(2, 2), str_cor="blue")
t = Triangulo(Vertice2D(0, 2),
              Vertice2D(1, 0),
              Vertice2D(2, 3))

plot2D([t, r])
