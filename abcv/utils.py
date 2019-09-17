import fresnel
import numpy as np


def make_unit_cell(scene, lattice_vects, line_width=0.05, color=[0., 0., 0.]):
    vertices = np.zeros((8, 3), dtype=np.float)
    vertices[1:4, :] = lattice_vects
    vertices[4, :] = vertices[1, :] + vertices[2, :]
    vertices[5, :] = vertices[1, :] + vertices[3, :]
    vertices[6, :] = vertices[2, :] + vertices[3, :]
    vertices[7, :] = np.sum(vertices[1:4, :], axis=0)

    unit_cell = fresnel.geometry.Cylinder(scene, N=12)
    unit_cell.points[:] = [
        [vertices[0, :], vertices[1, :]],
        [vertices[0, :], vertices[2, :]],
        [vertices[0, :], vertices[3, :]],
        [vertices[1, :], vertices[4, :]],
        [vertices[2, :], vertices[4, :]],
        [vertices[1, :], vertices[5, :]],
        [vertices[3, :], vertices[5, :]],
        [vertices[2, :], vertices[6, :]],
        [vertices[3, :], vertices[6, :]],
        [vertices[4, :], vertices[7, :]],
        [vertices[5, :], vertices[7, :]],
        [vertices[6, :], vertices[7, :]],
    ]

    unit_cell.radius[:] = line_width * np.ones(12)

    unit_cell.material = fresnel.material.Material(
        color=fresnel.color.linear(color)
    )
    unit_cell.material.solid = 1.

    return unit_cell
