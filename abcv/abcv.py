import PIL
import fresnel
import itertools
import numpy as np
from abcv.utils import make_unit_cell


COLORSCHEME = [
    (0.12156, 0.46666, 0.70588),
    (1.00000, 0.49803, 0.05490),
    (0.17254, 0.62745, 0.17254),
    (0.83921, 0.15294, 0.15686),
    (0.58039, 0.40392, 0.74117),
    (0.54901, 0.33725, 0.29411),
    (0.89019, 0.46666, 0.76078),
    (0.49803, 0.49803, 0.49803),
    (0.73725, 0.74117, 0.13333),
    (0.09019, 0.74509, 0.81176)
]


class Viewer:
    def __init__(self, structure, grid_data=None):
        self.structure = structure
        self.grid_data = grid_data

        # properties
        self._colors = None

        # fresnel related
        self.scene = None
        self.atoms = None
        self.unit_cell = None
        self._image = None

    def generate_scene(self, background_color=None, radius_scale=0.666):
        self.scene = fresnel.Scene()

        if background_color is not None:
            self.scene.background_color = background_color[:3]
            self.scene.background_alpha = background_color[-1]

        # set up atoms
        self.atoms = fresnel.geometry.Sphere(
            self.scene,
            position=self.structure.cart_coords,
            radius=1.0,
            outline_width=0.
        )

        self.atoms.radius[:] = \
            [radius_scale * x.specie.data['Atomic radius']
             for x in self.structure]

        self.atoms.material = fresnel.material.Material()
        self.atoms.material.primitive_color_mix = 1.0
        self.atoms.color[:] = fresnel.color.linear(
            [self.colors[x.specie.name] for x in self.structure]
        )

        # set up unit cell
        self.unit_cell = make_unit_cell(
            self.scene,
            self.structure.lattice.matrix
        )

        self.scene.camera = \
            fresnel.camera.fit(self.scene, view='isometric', margin=0.1)

        return self.scene

    @property
    def colors(self):
        if self._colors is None:
            self._colors = {}
            species = \
                np.unique([x.name for x in self.structure.species]).tolist()
            for ele, c in zip(species, itertools.cycle(COLORSCHEME)):
                self._colors[ele] = c

        return self._colors

    @colors.setter
    def colors(self, value_dict):
        for ele in self.structure.species:
            if ele.name not in value_dict:
                raise ValueError(f'species {ele.name} not found in value dict')

        for ele in value_dict:
            if len(value_dict[ele]) != 3:
                raise ValueError(f'invalid color {value_dict[ele]}')

        self._colors = value_dict

    def save_image(self, filename):
        if self.scene is None:
            self.generate_scene()

        self._image = fresnel.pathtrace(
            self.scene, samples=64, light_samples=32, w=640, h=640
        )

        PIL.Image.fromarray(self._image[:], mode='RGBA').save(filename)
        return self._image
