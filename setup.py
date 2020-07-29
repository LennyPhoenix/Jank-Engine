import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jank",
    version="0.1.0dev",
    author="DoAltPlusF4",
    author_email="doaltplusf4@gmail.com",
    description="A game engine using Pyglet and Pymunk.",
    license="LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DoAltPlusF4/Jank-Engine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
        "pyglet", "pymunk"
    ]
)
