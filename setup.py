import setuptools

setuptools.setup(
    name="Multiprocessor",
    version="2.0.0",
    author="Tschen Boffee",
    include_package_data=True,
    packages=setuptools.find_packages(where="../Multiprocessor"),
    description="A small tool for classifying books based on its file name and meta values",
    python_requires=">=3.6",
)
