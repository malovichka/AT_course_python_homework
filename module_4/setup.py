from setuptools import setup, find_packages


setup(
    name="package_path",
    version="1.0.0",
    description="package_path is a Python project that returns path to package if it is installed.",
    author="Iuliia Malovichko",
    author_email="iuliia_malovichko@epam.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    python_requires=">=3.10, <4",
)
