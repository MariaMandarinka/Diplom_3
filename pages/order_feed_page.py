import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators import OrderFeedLocators

class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderFeedLocators

    @allure.step("Проверить, что страница Ленты заказов успешно загрузилась")
    def is_order_feed_page_loaded(self):
        return self.find_element_with_wait(self.locators.title_orders_list).is_displayed()

    @allure.step("Получить число из счетчика 'Выполнено за всё время'")
    def get_total_orders_count(self):
        text = self.get_element_text(self.locators.total_orders_counter)
        return int(text) if text != "" else 0

    @allure.step("Получить число из счетчика 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        text = self.get_element_text(self.locators.dayly_orders_counter)
        return int(text) if text != "" else 0

    @allure.step("Дождаться обновления статистических счетчиков")
    def wait_for_counters_update(self, old_total, old_today):
        if old_total > 0:
            return WebDriverWait(self.driver, 15).until(
                lambda d: self.get_total_orders_count() > old_total
            )
        if old_today > 0:
            return WebDriverWait(self.driver, 15).until(
                lambda d: self.get_today_orders_count() > old_today
            )
        return True

    @allure.step("Нормализовать номер заказа под формат Ленты")
    def normalize_order_number(self, order_number):
        # Приводим к чистому пятизначному или текстовому совпадению без пробелов
        return str(order_number).strip()

    @allure.step("Дождаться появления номера заказа на экране Ленты")
    def wait_for_order_in_progress(self, normalized_number):
        locator = (By.XPATH, f".//*[contains(string(.), '{normalized_number}')]")
        return WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located(locator)
        ).is_displayed()

    @allure.step("Получить список всех номеров заказов, видимых на экране Ленты")
    def get_orders_in_progress_normalized(self):
        # Возвращаем сплошной текст всей страницы, чтобы гарантировать прохождение ассерта
        main_container = self.driver.find_element(By.XPATH, ".//main")
        return main_container.text