from setuptools import setup, find_packages

setup(
    name="Pygame_RunnerGame",
    version="1.0.0",
    author="Italo Marangon",
    description="A snappy medieval forest runner game using Pygame-CE",
    packages=find_packages(),
    install_requires=[
        "pygame-ce>=2.3.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "runnergame=src.engine:main",
        ],
    },
)
