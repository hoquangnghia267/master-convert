from setuptools import setup, find_packages

setup(
    name="universal-converter",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ttkbootstrap>=1.10.1",
        "Pillow>=9.0.0",
        "cryptography>=41.0.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0"
    ],
    entry_points={
        "console_scripts": [
            "universal-converter=converter.cli:main",
            "universal-converter-gui=converter.gui.app:main",
        ],
    },
)
