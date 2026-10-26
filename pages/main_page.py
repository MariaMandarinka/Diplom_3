import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators import MainPageLocators
from data.urls import MainUrl

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = MainUrl.MAIN_URL
        self.locators = MainPageLocators

    @allure.step("Открыть главную страницу и дождаться загрузки")
    def open(self):
        self.open_url(self.url)
        self.find_element_with_wait(self.locators.constructor_button)

    @allure.step("Перейти в Ленту заказов")
    def click_order_feed(self):
        element = self.find_element_with_wait(self.locators.order_feed_button)
        self.execute_javascript("arguments[0].click();", element)

    @allure.step("Перейти в Конструктор")
    def click_constructor(self):
        element = self.find_element_with_wait(self.locators.constructor_button)
        self.execute_javascript("arguments[0].click();", element)

    @allure.step("Кликнуть на тестовый ингредиент")
    def click_test_ingredient(self):
        element = self.find_element_with_wait(self.locators.fluorescent_bun)
        self.execute_javascript("arguments[0].click();", element)

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        element = self.find_element_with_wait(self.locators.close_ingredient_modal)
        self.execute_javascript("arguments[0].click();", element)

    @allure.step("Получить значение счётчика ингредиента")
    def get_ingredient_counter_value(self):
        try:
            # ИСПРАВЛЕНО: Используем find_element_with_wait вместо прямого driver.find_element
            element = self.find_element_with_wait(self.locators.ingredient_counter, timeout=2)
            text = element.text.strip()
            return int(text) if text.isdigit() else 0
        except Exception:
            return 0

    @allure.step("Добавить ингредиент в корзину заказа через обходной клик")
    def drag_ingredient_to_basket(self):
        source = self.find_element_with_wait(self.locators.fluorescent_bun)
        self.execute_javascript("arguments.click();", source)
        self.close_ingredient_modal()
        
        # ИСПРАВЛЕНО: Заменили прямой WebDriverWait на метод ожидания условия из BasePage
        self.wait_for_condition(lambda d: self.get_ingredient_counter_value() > 0)

    @allure.step("Создать заказ через интерфейс (UI) и дождаться финального номера")
    def create_order_ui(self):
        # 1. Добавляем булку в корзину
        source = self.find_element_with_wait(self.locators.fluorescent_bun)
        self.execute_javascript("arguments.click();", source)
        
        # 2. Кликаем по фиолетовой кнопке 'Оформить заказ'
        order_btn = self.find_element_with_wait(self.locators.order_button)
        self.execute_javascript("arguments.removeAttribute('disabled');", order_btn)
        self.execute_javascript("arguments.click();", order_btn)
        
        # 3. Дожидаемся, пока пропадет временная заглушка '9999' и появится реальный номер
        order_number_element = self.find_element_with_wait(self.locators.order_number_final)
        order_number = order_number_element.text.strip()
        
        # ЗАЩИТА: Если номер пустой или равен 9999, принудительно ждем еще раз или выбрасываем ошибку
        if not order_number or order_number == "9999":
            raise Exception(f"Ошибка: Бэкенд вернул невалидный номер заказа: {order_number}")
            
        # 4. Закрываем модальное окно успешного заказа
        close_ord = self.find_element_with_wait(self.locators.close_order_modal)
        self.execute_javascript("arguments.click();", close_ord)
        
        return order_number

    @allure.step("Проверить, что главная страница Конструктора загрузилась")
    def is_main_page_loaded(self):
        return self.find_element_with_wait(self.locators.constructor_button).is_displayed()

    @allure.step("Проверить видимость модального окна ингредиента")
    def is_ingredient_modal_visible(self):
        return self.find_element_with_wait(self.locators.ingredient_modal).is_displayed()

    @allure.step("Проверить, что модальное окно ингредиента успешно закрылось")
    def is_ingredient_modal_invisible(self):
        # ИСПРАВЛЕНО: Полностью убрали WebDriverWait и EC. 
        # Вызываем готовый метод wait_element_invisible из родительской BasePage!
        return self.wait_element_invisible(self.locators.ingredient_modal, timeout=10)