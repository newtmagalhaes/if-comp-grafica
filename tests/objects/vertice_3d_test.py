from src.objetos.vertice import Vertice3D


def test_origem_3d():
    assert Vertice3D(0, 0, 0) == Vertice3D.ORIGEM()


def test_subtracao_2d():
    ponto = Vertice3D(1, 2, 3)
    assert Vertice3D.ORIGEM() - ponto == Vertice3D(-1, -2, -3)


def test_divisao_escalar():
    ponto = Vertice3D(2, 4, 6)
    assert ponto / 2 == Vertice3D(1, 2, 3)


def test_produto_vetorial():
    v1 = Vertice3D(1, 0, 0)
    v2 = Vertice3D(0, 1, 0)
    assert v1.produto_vetorial(v2) == Vertice3D(0, 0, 1)
