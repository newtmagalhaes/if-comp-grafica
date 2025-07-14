from src.objetos.solidos import ISolido


def calcular_at_medio(objetos: list[ISolido]):
    vertices_medios = [
        sum(s.get_vertices()) / len(s.get_vertices())
        for s in objetos
    ]
    return sum(vertices_medios) / len(vertices_medios)
