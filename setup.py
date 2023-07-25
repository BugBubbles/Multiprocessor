import setuptools

setuptools.setup(
    name="classfy_book",
    version="1.0.0",
    author="Tschen Boffee",
    include_package_data=True,
    packages=setuptools.find_packages(where='../classfy_book'),
    description="A small tool for classifying books based on its file name and meta values",
)
