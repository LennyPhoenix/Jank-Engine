import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jank",
    version="0.1.0",
    author="LennyPhoenix",
    author_email="LennyPhoenixC@gmail.com",
    description="A game engine using Pyglet and Pymunk.",
    license="LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LennyPhoenix/Jank-Engine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyglet", "pymunk==5.6.0"
    ]
)
