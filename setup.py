from setuptools import setup, find_packages


VERSION = '0.0.1'

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='abcv',
    version=VERSION,
    author='Mark E. Turiansky',
    author_email='mturiansky@physics.ucsb.edu',
    description=('A python-based crystal viewer built upon the fresnel and '
                 'pymatgen libraries.'),
    license='MIT',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/mturiansky/abcv',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.17.1', 'pymatgen>=2019.9.16'
    ],
    extras_require={
        'dev': ['nose2>=0.9.1', 'coverage>=4.5.3', 'pillow>=6.1.0'],
    },
    keywords=['physics', 'materials', 'science', 'visualization'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
)
