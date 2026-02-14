import pytest
from pathlib import Path

@pytest.fixture
def assets_test_dir():
    # Retorna la ruta al directorio assets_test
    # Path(__file__) es el path a conftest.py
    # .parent es el directorio tests/
    # .parent es la raíz del proyecto
    # / "assets_test" es el directorio deseado
    return Path(__file__).parent.parent / "assets_test"
