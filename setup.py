import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codra",
    version="0.0.3",
    author="Omar Elawady",
    author_email="omarelawady1998@gmail.com",
    description="A python template engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OmarElawady/codra",
    packages=['codra'],
    install_requires=['ply'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
