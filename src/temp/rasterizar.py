from PIL import Image, ImageDraw
import numpy as np


def rasterizar_objetos(objetos_2d, resolucao=(300, 300)):
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
    lista = []
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
            for *idxs, cor in faces:
                poly = [tuple(pix[i]) for i in idxs]
                draw.polygon(poly, fill=cor)
        # 4b) arestas (wireframe)
        for i, j, cor in arestas:
            draw.line([tuple(pix[i]), tuple(pix[j])], fill=cor, width=2)

    return img
