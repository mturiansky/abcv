<div align="center">
  <img src="assets/logo.png" alt="ABCV" width=330>
  <h2>A Better Crystal Viewer</h2>
</div>

`ABCV` is a python-based crystal viewer built upon the popular [pymatgen](https://github.com/materialsproject/pymatgen) and [fresnel](https://github.com/glotzerlab/fresnel) libraries.
By leveraging pymatgen, `ABCV` supports a range of popular input/output files associated with common quantum chemistry codes.
Furthermore, various transformations and analysis tools are provided by pymatgen that makes preparing images with `ABCV` a snap.
`ABCV` attempts to be fully customizable by utilizing the fresnel library, which provides a range features for creating publication-quality images.

## Gallery

Below are a selection of images generated with `ABCV`.

<p><img src="assets/example0.png" alt="example0" width=250>
<img src="assets/example1.png" alt="example1" width=250></p>

## Example

A simple example utilizing `ABCV` is shown below.
```python
from abcv import Viewer
from pymatgen import Structure

# load the logo structure with pymatgen
struct = Structure.from_file('test_files/POSCAR.logo')

# instantiate the ABCV Viewer
viewer = Viewer(struct)

# generate scene and set background color to white (in RGBA)
viewer.generate_scene(background_color=(1., 1., 1., 1.))

# save the image
viewer.save_image('test.png')
```

`ABCV` also comes with a command-line interface.
The above code is essentially equivalent to running the following.
```shell
$ abcv --save test.png test_files/POSCAR.logo
```

## Documentation

For now, documentation can be accessed from the docstring of each object.
Extensive online documentation will be provided in the future.

## Installation

Presently, there are two methods for installing `ABCV`.
In the future, we plan to provide a package on conda-forge for installation.

### Docker (Recommended)

To install via docker, first clone the repository.
```shell
$ git clone https://github.com/mturiansky/abcv && cd abcv/
```
Next, build the docker image.
```shell
$ docker build -t abcv:v0.0.1 .
```
You are now ready to run the container.
```shell
$ docker run --rm -it abcv:v0.0.1 bash
```
Within the container, one can access `ABCV` with the `$ abcv` command or as a library (`from abcv import Viewer`).
To use the interactive GUI, you need to run the docker container with the following command.
```shell
$ docker run --rm --volume="$HOME/.Xauthority:/home/user/.Xauthority:rw" --env="DISPLAY" --net=host -it abcv:v0.0.1 bash
```

### Pip

To install via pip, you first need to install [fresnel](https://github.com/glotzerlab/fresnel#installing-fresnel) (*tip*: you may need to manually install qhull if you don't use the conda-forge package).
Next, you simply need to run the following command (preferably within a virtual environment).
```shell
$ pip install git+https://github.com/mturiansky/abcv
```

## Contributing

We would be happy to accept contributions from other developers.
There is still much work to do to implement various convenience features.
All contributed code should conform to `pep8` standards.
