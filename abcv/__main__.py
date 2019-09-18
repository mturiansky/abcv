import click
from abcv import Viewer
from pymatgen.io.vasp.outputs import Chgcar
from pymatgen import Structure


@click.command()
@click.argument('input_file', type=click.Path(dir_okay=False, exists=True))
@click.option('--save', '-s', type=click.Path(dir_okay=False, exists=False),
              help='save image to the given path')
def cli(input_file, save):
    if 'chgcar' in input_file.lower():
        chgcar = Chgcar.from_file(input_file)
        viewer = Viewer(chgcar.structure, chgcar.data['total'])
    else:
        try:
            struct = Structure.from_file(input_file)
        except ValueError as e:
            print(f'[!] Fatal Error: {e}\n'
                  f'[!] Please make sure your input file is valid.')
            return
        viewer = Viewer(struct)

    viewer.generate_scene(background_color=(1., 1., 1.))
    viewer.interact()
    if save is not None:
        viewer.save_image(save)


if __name__ == '__main__':
    import sys
    cli(sys.argv[1:])
