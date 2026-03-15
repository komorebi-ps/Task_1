import pytest
from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from praktikum.database import Database
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING
from unittest.mock import Mock, patch

class TestBun:
    
    # Создание булки с параметризацией
    @pytest.mark.parametrize("name, price", [
        ("Булка с кунжутом", 850),
        ("Бриошь", 930),
        ("Цельнозерновая", 750)
    ])
    def test_bun_create(self, name, price):
        bun = Bun(name, price)
        assert bun.get_name() == name
        assert bun.get_price() == price
    
    # Получение названия булки
    def test_bun_get_name(self, bun):
        assert bun.get_name() == "Черная булка"
    
    # Получение цены булки
    def test_bun_get_price(self, bun):
        assert bun.get_price() == 900


class TestDatabase:
    
    def test_database_init(self, database):
        assert len(database.available_buns()) == 3
        assert len(database.available_ingredients()) == 6
    
    # Получение списка доступных булок
    def test_available_buns(self, database):
        buns = database.available_buns()
        assert len(buns) == 3
        assert buns[0].get_name() == "black bun"
        assert buns[1].get_name() == "white bun"
        assert buns[2].get_name() == "red bun"
    
    # Получение списка доступных ингредиентов
    def test_available_ingredients(self, database):
        ingredients = database.available_ingredients()
        assert len(ingredients) == 6
        assert ingredients[0].get_type() == INGREDIENT_TYPE_SAUCE
        assert ingredients[3].get_type() == INGREDIENT_TYPE_FILLING



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
        assert '(==== Каменная булка ====)' in receipt
        assert '= sauce Тестовый соус =' in receipt
        assert 'Price: 2050' in receipt
    


class TestIngredient:
    
    # Создание ингредиента с параметризацией
    @pytest.mark.parametrize("ingredient_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "Кетчунез", 70),
        (INGREDIENT_TYPE_SAUCE, "Сладкий чили", 80),
        (INGREDIENT_TYPE_FILLING, "Котлета", 950),
        (INGREDIENT_TYPE_FILLING, "Огурчики", 40)
    ])
    def test_ingredient_create(self, ingredient_type, name, price):

        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_type() == ingredient_type
        assert ingredient.get_name() == name
        assert ingredient.get_price() == price
    
    # Получение цены ингредиента
    def test_ingredient_get_price(self, ingredient):
        assert ingredient.get_price() == 99

    # Получение названия ингредиента
    def test_ingredient_get_name(self, ingredient):
        assert ingredient.get_name() == "Острый соус"

    # Получение типа ингредиента
    def test_ingredient_get_type(self, ingredient):
        assert ingredient.get_type() == INGREDIENT_TYPE_SAUCE


