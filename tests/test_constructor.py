import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.epic("Дипломный проект: Stellar Burgers")
@allure.feature("Раздел Конструктор")
class TestStellarConstructor:

    @allure.title("Проверка перехода по клику на раздел 'Лента заказов'")
    @allure.description("Проверяем, что при клике на 'Лента заказов' открывается соответствующая страница с заголовком")
    def test_constructor_navigation_to_feed(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        main_page.open()
        main_page.click_order_feed()
        
        # Проверка вынесена в метод страницы
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"

    @allure.title("Проверка перехода по клику на раздел 'Конструктор'")
    @allure.description("Проверяем возврат на главную страницу при клике на вкладку 'Конструктор'")
    def test_constructor_navigation_to_constructor(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        main_page.open()
        main_page.click_order_feed()
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"
        
        main_page.click_constructor()
        
        # Проверка вынесена в метод страницы
        assert main_page.is_main_page_loaded(), "Главная страница Конструктора не загрузилась"

    @allure.title("Проверка появления всплывающего окна деталей при клике на ингредиент")
    @allure.description("Клик по ингредиенту открывает модальное окно с деталями")
    def test_ingredient_modal_appears(self, driver):
        main_page = MainPage(driver)
        
        main_page.open()
        main_page.click_test_ingredient()
        
        # Проверка вынесена в метод страницы
        assert main_page.is_ingredient_modal_visible(), "Модальное окно деталей ингредиента не появилось"

    @allure.title("Проверка закрытия всплывающего окна кликом по крестику")
    @allure.description("Клик по крестику модального окна ингредиента успешно закрывает его")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        
        main_page.open()
        main_page.click_test_ingredient()
        assert main_page.is_ingredient_modal_visible(), "Модальное окно деталей ингредиента не появилось"
        
        main_page.close_ingredient_modal()
        
        # Проверка вынесена в метод страницы
        assert main_page.is_ingredient_modal_invisible(), "Модальное окно ингредиента не закрылось"

    @allure.title("Проверка увеличения счётчика ингредиента при добавлении в заказ")
    @allure.description("Счётчик ингредиента увеличивается, когда мы перетаскиваем/добавляем его в корзину")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        
        main_page.open()
        initial_counter = main_page.get_ingredient_counter_value()
        
        # Метод выполняет добавление внутри себя
        main_page.drag_ingredient_to_basket()
        
        new_counter = main_page.get_ingredient_counter_value()
        assert new_counter > initial_counter, f"Счётчик ингредиента не увеличился. Было: {initial_counter}, стало: {new_counter}"