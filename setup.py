# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author='Daniel Espiritu',
    description=(
        f'Python package for systematic coloring of PyMol structures according',
        f'to customizable color gradients.'
        ),
    name='pyml_rgb_encoding',
    version='0.1.0',
    packages=find_packages(
        include=['pypml_rgb_encoding', 'pypml_rgb_encoding.*']
        ),
    install_requires=['pandas>=2.0.3', 'numpy>=1.24.3','matplotlib>=3.8.3']
    )
