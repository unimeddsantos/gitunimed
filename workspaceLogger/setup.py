from setuptools import setup, find_packages

setup(
    name="loggerUnimed",
    version="0.1.2",
    packages=find_packages(),  # Isso encontra automaticamente seu pacote
    package_dir={'': '.'},     # Indica que os pacotes estão no diretório atual
    py_modules=["reportUnimed"],  # Para módulos únicos
)