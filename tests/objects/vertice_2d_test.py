from src.objetos.vertice import Vertice2D


def test_origem():
    assert Vertice2D(0, 0) == Vertice2D.ORIGEM()


def test_soma():
    ponto = Vertice2D(1, 2)
    assert ponto + Vertice2D.ORIGEM() == ponto


def test_distancia():
    p1 = Vertice2D(3, 0)
    p2 = Vertice2D(0, 4)
    assert p1.distance(p2) == 5.0
