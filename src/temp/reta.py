from src.objetos.segmento_de_reta import SegmentoDeReta
from src.objetos.vertice import Vertice2D, Vertice3D
from src.temp.pipeline import plot2D, plot3D

seg_2d = SegmentoDeReta(Vertice2D(2, 3), Vertice2D(-1, -1))
plot2D([seg_2d])

seg_3d = SegmentoDeReta(Vertice3D(1, 2, -1), Vertice3D(3, 3, 3))
# requer ajustes
plot3D([(seg_3d.get_vertices(), seg_3d.get_arestas(), seg_3d.get_faces())])
