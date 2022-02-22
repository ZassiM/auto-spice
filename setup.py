import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-spice", # Replace with your own username
    version="0.0.1",
    author="Wassim Zahr",
    author_email="zahr@ice.rwth-aachen.de",
    description="Automatic generation of netlist files for Spice simulations with Cadence Spectre",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.iss.rwth-aachen.de/neuro/hardware/auto-spice",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
