from setuptools import setup, find_packages

setup(
    name="universal-converter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add dependencies here
    ],
    entry_points={
        "console_scripts": [
            "universal-converter=converter.cli:main",
        ],
    },
)
