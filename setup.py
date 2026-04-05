# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author='Daniel Espiritu',
    description=(
        f'Python package for systematic coloring of PyMol structures according',
        f'to customizable color gradients.'
        ),
    name='pymol_rgb_encoding',
    version='0.1.0',
    packages=find_packages(
        include=['pymol_rgb_encoding', 'pymol_rgb_encoding.*']
        ),
    install_requires=['pandas==2.1.4', 'numpy==1.26.4','matplotlib==3.8.0'],
    python_requires="==3.11.*"
    )
