import pytest
from praktikum.bun import Bun
from praktikum.database import Database
from praktikum.ingredient import Ingredient
from praktikum.burger import Burger
from unittest.mock import Mock, patch
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING

# Фикстуры для моков

@pytest.fixture
def bun_mock():
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = 'Каменная булка'
    mock_bun.get_price.return_value = 1000
    return mock_bun

@pytest.fixture
def ingredient_mock():
    mock_ingredient = Mock(spec=Ingredient)
    mock_ingredient.get_name.return_value = 'Тестовый соус'
    mock_ingredient.get_price.return_value = 50
    mock_ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
    return mock_ingredient

@pytest.fixture
def ingredient_mock_filling():
    mock_ingredient = Mock(spec=Ingredient)
    mock_ingredient.get_name.return_value = 'Тестовая начинка'
    mock_ingredient.get_price.return_value = 750
    mock_ingredient.get_type.return_value = INGREDIENT_TYPE_FILLING
    return mock_ingredient


# Фикстуры для объектов

@pytest.fixture
def bun():
    return Bun("Черная булка", 900)

@pytest.fixture
def database():
    return Database()

@pytest.fixture
def ingredient():
    return Ingredient(INGREDIENT_TYPE_SAUCE, "Острый соус", 99)

@pytest.fixture
def burger():
    return Burger()


