from setuptools import setup, find_packages

setup(
    name='customGcodeGenerator',  # Name of library
    version='0.1.0',              # Version of library
    packages=find_packages(),     # Automatically find all packages within customGcodeGenerator
    install_requires=[
        'numpy',         # List of dependencies necesary for the library to work
        'pygame',
        'typing',
        'pydantic'


    ],
    description='A library designing and visualizing and finally generating custom G-code paths for 3D printing.',
    author='Wiktor Suchy',
    author_email='such.wik@gmail.com',
    url='https://github.com/your_username/your_repo',  # Link to your repository (if applicable)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.13',  # Specify your Python version compatibility
)
