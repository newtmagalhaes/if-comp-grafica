from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from numpy.typing import NDArray
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

from src.objetos.solidos.isolido import ISolido


def createAx():
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    return ax


def drawAxes(ax: Axes, origin: np.ndarray, axes: np.ndarray, labels=["x", "y", "z"], colorSet=0, scatterLabel="point"):
    color = np.array([
        ["red", "yellow", "blue"],
        ["green", "purple", "orange"]
    ])[colorSet]
    scatterColor = np.array([
        "blue",
        "red"
    ])[colorSet]

    ax.quiver(origin[0], origin[1], origin[2], axes[0][0], axes[0][1], axes[0][2], color=color[0], linewidth=2, label=labels[0])
    ax.quiver(origin[0], origin[1], origin[2], axes[1][0], axes[1][1], axes[1][2], color=color[1], linewidth=2, label=labels[1])
    ax.quiver(origin[0], origin[1], origin[2], axes[2][0], axes[2][1], axes[2][2], color=color[2], linewidth=2, label=labels[2])
    ax.scatter(origin[0], origin[1], origin[2], color=scatterColor, s=100, marker='x', label=scatterLabel)


def plot3D(objects, title: str = "Object", ax: Axes | None = None):
    if ax is None:
        ax = createAx()

    for index, (vertices, arestas, faces) in enumerate(objects):
        if arestas is not None and len(arestas) > 0:
            linhas = []
            line_colors = []

            for aresta in arestas:
                i, j, cor = aresta  # agora pegamos os 3 elementos

                # Monta a linha
                linha = [
                    (vertices[i][0], vertices[i][1], vertices[i][2]),
                    (vertices[j][0], vertices[j][1], vertices[j][2])
                ]

                linhas.append(linha)
                line_colors.append(cor)

            lc = Line3DCollection(linhas, colors=line_colors, linewidths=1.5)
            ax.add_collection3d(lc)

        if faces is not None and len(faces) > 0:
            polys = []
            face_colors = []
            for face in faces:
                # Separa todos os índices da cor:
                *indices, cor = face

                # Constrói a lista de vértices (x, y, z) da face:
                poly = [(vertices[i][0], vertices[i][1], vertices[i][2]) for i in indices]

                polys.append(poly)
                face_colors.append(cor)
            pc = Poly3DCollection(polys, facecolors=face_colors, alpha=0.3, edgecolor='black')
            ax.add_collection3d(pc)

    # Marcar a origem do mundo no sistema da câmera

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()


def plot2D(objects: list[ISolido], title: str = "Object 2D"):
    fig, ax = plt.subplots(figsize=(8, 8))

    for index, solido in enumerate(objects):
        vertices, arestas, faces = solido.get_vertices(), solido.get_arestas(), solido.get_faces()
        # Arestas (linhas)
        for aresta in arestas:
            i, j, cor = aresta.vertice_incial, aresta.vertice_final, aresta.cor

            x_coords = [vertices[i][0], vertices[j][0]]
            y_coords = [vertices[i][1], vertices[j][1]]

            ax.plot(x_coords, y_coords, color=cor, linewidth=1.5)

        # Faces (polígonos preenchidos)
        for face in faces:
            arestas_da_face, cor = face.arestas, face.cor
            x_coords = []
            y_coords = []
            for i_aresta in arestas_da_face:
                i_vertice = arestas[i_aresta].vertice_incial
                coordenada_x, coordenada_y = vertices[i_vertice].get_coordenadas()
                # print(f'coordenada x é: {coordenada_x}')
                x_coords.append(coordenada_x)
                y_coords.append(coordenada_y)
            # print(x_coords)
            # x_coords.append(x_coords[0])
            # y_coords.append(y_coords[0])

            ax.fill(x_coords, y_coords, color=cor, alpha=0.3, edgecolor='black')

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
