import pytest
from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from praktikum.database import Database
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING
from unittest.mock import Mock, patch
from data import (
    SPICY_SAUCE, 
    TEST_FILLING, 
    TEST_SAUCE, 
    STONE_BUN, 
    BLACK_BUN,
    TEST_BUN_1,
    TEST_BUN_2,
    TEST_BUN_3,
    TEST_INGREDIENT_1,
    TEST_INGREDIENT_2
)

class TestBun:
    
    # Получение названия булки
    @pytest.mark.parametrize("name, price", [
        (TEST_BUN_1['name'], TEST_BUN_1['price']),
        (TEST_BUN_2['name'], TEST_BUN_2['price']),
        (TEST_BUN_3['name'], TEST_BUN_3['price'])
    ])
    def test_bun_get_name(self, name, price):
        bun = Bun(name, price)
        assert bun.get_name() == name

    # Получение цены булки
    @pytest.mark.parametrize("name, price", [
        (TEST_BUN_1['name'], TEST_BUN_1['price']),
        (TEST_BUN_2['name'], TEST_BUN_2['price']),
        (TEST_BUN_3['name'], TEST_BUN_3['price'])
    ])
    def test_bun_get_price(self, name, price):
        bun = Bun(name, price)
        assert bun.get_price() == price



class TestDatabase:
    
    # Проверка получения списка булок
    def test_available_buns_returns_list_of_buns(self, database):
        buns = database.available_buns()    
        assert isinstance(buns, list)

    # Проверка получения списка ингредиентов
    def test_available_buns_returns_list_of_ingredients(self, database):
        ingredients = database.available_ingredients()    
        assert isinstance(ingredients, list)

    # Проверка того, что метод возвращает ожидаемые булки
    def test_available_buns_returns_expected_buns(self, database):
        buns = database.available_buns()
        bun_names = [bun.get_name() for bun in buns]
        assert "black bun" in bun_names
        assert "white bun" in bun_names
        assert "red bun" in bun_names

    # Проверка того, что метод возвращает ожидаемые ингредиенты
    def test_available_ingredients_returns_expected_ingredients(self, database):
        ingredients = database.available_ingredients()
        ingredient_names = [ingredient.get_name() for ingredient in ingredients]
        expected_names = [
            "hot sauce", "sour cream", "chili sauce", "cutlet", "dinosaur", "sausage"
            ]
        for expected_name in expected_names:
            assert expected_name in ingredient_names












    # Проверка наличия в полученном списке тех булок, которые сейчас есть в БД
    @pytest.mark.parametrize("index, expected_name, expected_price", [
        (0, "black bun", 100),
        (1, "white bun", 200),
        (2, "red bun", 300)
    ])
    def test_available_buns_returns_correct_bun_by_index(self, database, index, expected_name, expected_price):
        buns = database.available_buns()
        assert buns[index].get_name() == expected_name
        assert buns[index].get_price() == expected_price



class TestBurger:
    
    # Выбор булок
    def test_set_buns(self, burger, bun_mock):
        burger.set_buns(bun_mock)
        assert burger.bun == bun_mock
    
    # Добавление ингредиента
    def test_add_ingredient(self, burger, ingredient_mock):

        burger.add_ingredient(ingredient_mock)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient_mock

    # Удаление ингредиента
    def test_remove_ingredient(self, burger, ingredient_mock):

        burger.add_ingredient(ingredient_mock)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0
    
    # Перемещение ингредиента
    def test_move_ingredient(self, burger):

        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.move_ingredient(0, 1)
        assert burger.ingredients[0] == ingredient2
        assert burger.ingredients[1] == ingredient1
    
    # Получение цены бургера
    def test_get_burger_price(self, burger, bun_mock, ingredient_mock, ingredient_mock_filling):

        burger.set_buns(bun_mock)
        burger.add_ingredient(ingredient_mock)
        burger.add_ingredient(ingredient_mock_filling)
        # (1000 * 2) + 50 + 750 = 2800
        assert burger.get_price() == 2800
    
    # Получение чека
    @patch('praktikum.burger.Burger.get_price')
    def test_get_receipt(self, mock_get_price, burger, bun_mock, ingredient_mock):

        mock_get_price.return_value = 2050  # (1000 * 2) + 50 = 2050
        # Сборка бургера
        burger.set_buns(bun_mock)
        burger.add_ingredient(ingredient_mock)
        receipt = burger.get_receipt()
        # Проверка содержимого чека
        assert f'(==== {STONE_BUN['name']} ====)' in receipt
        assert f'= sauce {TEST_SAUCE['name']} =' in receipt
        assert 'Price: 2050' in receipt
    


class TestIngredient:
    
    # Получение типа ингредиента
    @pytest.mark.parametrize("ingredient_type, name, price", [
        (TEST_INGREDIENT_1['type'], TEST_INGREDIENT_1['name'], TEST_INGREDIENT_1['price']),
        (TEST_INGREDIENT_2['type'], TEST_INGREDIENT_2['name'], TEST_INGREDIENT_2['price']),
    ])
    def test_ingredient_get_type(self, ingredient_type, name, price):

        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_type() == ingredient_type
    
    # Получение цены ингредиента
    @pytest.mark.parametrize("ingredient_type, name, price", [
        (TEST_INGREDIENT_1['type'], TEST_INGREDIENT_1['name'], TEST_INGREDIENT_1['price']),
        (TEST_INGREDIENT_2['type'], TEST_INGREDIENT_2['name'], TEST_INGREDIENT_2['price']),
    ])
    def test_ingredient_get_price(self, ingredient_type, name, price):

        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_price() == price
    
    # Получение названия ингредиента
    @pytest.mark.parametrize("ingredient_type, name, price", [
        (TEST_INGREDIENT_1['type'], TEST_INGREDIENT_1['name'], TEST_INGREDIENT_1['price']),
        (TEST_INGREDIENT_2['type'], TEST_INGREDIENT_2['name'], TEST_INGREDIENT_2['price']),
    ])
    def test_ingredient_get_name(self, ingredient_type, name, price):

        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_name() == name
    



