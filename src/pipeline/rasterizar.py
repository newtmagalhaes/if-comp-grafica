from copy import deepcopy

import numpy as np
from PIL import Image, ImageDraw

from src.objetos.solidos import ISolido, ItemAresta, ItemFace
from src.objetos.vertice import IVertice, Vertice3D

Faces = list[ItemFace]
Arestas = list[ItemAresta]
Vertices = np.typing.NDArray[np.float64]
Elementos = tuple[Vertices, Arestas, Faces]


def _normalizar_vertices(solidos: list[ISolido], resolucao: tuple[int, int] = (300, 300)) -> list[ISolido]:
    ALTURA, LARGURA = resolucao
    copia_solidos = deepcopy(solidos)
    vertices = sum((s.get_vertices() for s in copia_solidos), start=[])
    xy_vertices = np.vstack([v.get_coordenadas()[:2] for v in vertices])
    menor_xy, maior_xy = xy_vertices.min(axis=0), xy_vertices.max(axis=0)
    span = maior_xy - menor_xy
    span[span == 0] = 1e-6

    # converter em SCD (coordenadas de pixel)
    for s in copia_solidos:
        verts = s.get_vertices()
        for i, v in enumerate(verts):
            coords = v.get_coordenadas()
            norm = (coords[:2] - menor_xy) / span
            x_norm = norm[0] * (LARGURA - 1)
            y_norm = (1 - norm[1]) * (ALTURA - 1)
            verts[i] = Vertice3D(x_norm, y_norm, coords[2])
    copia_solidos.sort(key=_z_medio_do_solido, reverse=True)
    return copia_solidos


def _z_medio_do_solido(solido: ISolido) -> float:
    return float(np.mean([vertice[2] for vertice in solido.get_vertices()]))


def _filtrar_faces_ocultas(solido: ISolido, vetor_camera) -> tuple[list[IVertice], list[ItemAresta], list[ItemFace]]:
    faces = solido.get_faces()
    arestas = solido.get_arestas()
    vertices = solido.get_vertices()
    faces_filtradas = []
    for f in faces:
        a = [arestas[indice] for indice in f.arestas]
        a1, a2 = a[0], a[-1]
        v1 = vertices[a1.vertice_final] - vertices[a1.vertice_inicial]
        v2 = vertices[a2.vertice_final] - vertices[a2.vertice_inicial]
        vetor_face = np.cross(v1.get_coordenadas(), v2.get_coordenadas())
        result = np.dot(vetor_face, vetor_camera.get_coordenadas())
        if result <= 0:
            faces_filtradas.append(f)

    return vertices, arestas, faces_filtradas


def rasterizar(solidos: list[ISolido], vetor_camera, resolucao: tuple[int, int] = (300, 300)) -> Image.Image:
    BACKGROUND_COLOR = 'white'
    img = Image.new("RGB", resolucao, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    solidos_normalizados = _normalizar_vertices(solidos, resolucao)
    for solido in solidos_normalizados:
        # vertices, arestas, faces = _filtrar_faces_ocultas(solido, vetor_camera)
        vertices, arestas, faces = solido.get_vertices(), solido.get_arestas(), solido.get_faces()
        for f in faces:
            # a = [arestas[i] for i in f.arestas]
            a = f.get_arestas(arestas)
            poly = [tuple(vertices[i.vertice_inicial].get_coordenadas()[:2]) for i in a]
            draw.polygon(poly, fill=f.cor)

        for a in arestas:
            draw.line(
                xy=[
                    tuple(vertices[a.vertice_inicial].get_coordenadas()[:2]),
                    tuple(vertices[a.vertice_final].get_coordenadas()[:2])
                ],
                fill=a.cor,
                width=2)

    return img


def rasterizar_objetos(objetos_2d: list[Elementos], resolucao=(300, 300)) -> Image.Image:
    """
    Rasteriza com ocultação de arestas atrás de faces:
      • Ordena objetos por profundidade média (farthest first).
      • Para cada objeto: desenha faces, depois arestas.
    objetos_2d: lista de (verts_proj, arestas, faces[, _])
      - verts_proj: np.ndarray Nx4 → [x', y', z_cam, w']
      - arestas   : [(i,j,cor),...]
      - faces     : [(i0,i1,...,cor),...] ou None
    """
    W, H = resolucao

    # 1) Bounding‐box global para x',y'
    all_xy = np.vstack([v[:, :2] for v, *_ in objetos_2d])
    mn, mx = all_xy.min(axis=0), all_xy.max(axis=0)
    span = mx - mn
    span[span == 0] = 1e-6

    # 2) Converte cada objeto em coords de pixel e calcula profundidade média
    lista: list[tuple[float, np.ndarray, Arestas, Faces]] = []
    for v_proj, arestas, faces, *_ in objetos_2d:
        # normaliza → [0,1]
        norm = (v_proj[:, :2] - mn) / span
        xs = norm[:, 0] * (W-1)
        ys = (1 - norm[:, 1]) * (H-1)
        pix = np.stack([xs, ys], axis=1)
        z_cam = v_proj[:, 2]
        depth_obj = float(np.mean(z_cam))  # profundidade média do objeto
        lista.append((depth_obj, pix, arestas, faces))

    # 3) ordena do mais longe (maior z) para o mais perto
    lista.sort(key=lambda x: x[0], reverse=True)

    # 4) desenha em sequência
    img = Image.new("RGB", (W, H), 1)
    draw = ImageDraw.Draw(img)

    for _, pix, arestas, faces in lista:
        # 4a) faces (preenchimento)
        if faces:
            for f in faces:
                a = [arestas[i] for i in f.arestas]
                poly = [tuple(pix[i.vertice_inicial]) for i in a]
                draw.polygon(poly, fill=f.cor)
        # 4b) arestas (wireframe)
        for a in arestas:
            draw.line([tuple(pix[a.vertice_inicial]), tuple(pix[a.vertice_final])], fill=a.cor, width=2)

    return img
