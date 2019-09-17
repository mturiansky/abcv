import fresnel
import itertools
import numpy as np
from pymatgen.core.bonds import CovalentBond


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


def make_bonds(scene, structure, line_width=0.08, tol=0.2, color=[.1, .1, .1]):
    bonds = []
    for site0, site1 in itertools.combinations(structure, 2):
        if CovalentBond.is_bonded(site0, site1, default_bl=0.5):
            dist = site0.distance(site1)
            if np.isclose(np.linalg.norm(site0.coords - site1.coords),
                          dist, rtol=5e-3):
                bonds.append([site0.coords.tolist(), site1.coords.tolist()])
            # elif draw_pbc:
            #     for p in itertools.product([1, 0, -1], repeat=3):
            #         vec = site1.coords + np.dot(p, structure.lattice.matrix)
            #         if np.isclose(np.linalg.norm(site0.coords - vec),
            #                       dist, rtol=5e-3):
            #             bonds.append([site0.coords.tolist(), vec.tolist()])
            #             break
            #     for p in itertools.product([1, 0, -1], repeat=3):
            #         vec = site0.coords + np.dot(p, structure.lattice.matrix)
            #         if np.isclose(np.linalg.norm(vec - site1.coords),
            #                       dist, rtol=5e-3):
            #             bonds.append([vec.tolist(), site1.coords.tolist()])
            #             break

    bonds_geom = fresnel.geometry.Cylinder(scene, N=len(bonds))
    bonds_geom.points[:] = bonds
    bonds_geom.radius[:] = line_width * np.ones(len(bonds))
    bonds_geom.material = fresnel.material.Material(
        color=fresnel.color.linear(color)
    )
