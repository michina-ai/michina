from setuptools import setup, find_packages

setup(
    name="michina",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "python-dotenv",
        "pydantic",
    ],
    entry_points={
        "console_scripts": [
            "michina=michina.michina:main",
        ],
    },
)
