import sys
from abcv import Viewer
from pymatgen import Structure


struct = Structure.from_file(sys.argv[1])
viewer = Viewer(struct * [3, 3, 3])
viewer.generate_scene(background_color=(1., 1., 1., 1.))
viewer.save_image(sys.argv[2])
