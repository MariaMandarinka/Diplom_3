import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators import AuthPageLocators
from data.urls import MainUrl, URLS

class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{MainUrl.MAIN_URL.rstrip('/')}/{URLS.url_login}"
        self.locators = AuthPageLocators

    @allure.step('Открыть страницу авторизации')
    def open(self):
        self.open_url(self.url)

    @allure.step('Ввести email')
    def set_email(self, email):
        # ИСПРАВЛЕНО: Используем ваш родной метод из BasePage вместо чужого
        email_field = self.find_element_with_wait(self.locators.email_input)
        email_field.clear()
        email_field.send_keys(email)

    @allure.step('Ввести пароль')
    def set_password(self, password):
        # ИСПРАВЛЕНО: Заменили find_element на find_element_with_wait из BasePage
        password_field = self.find_element_with_wait(self.locators.password_input)
        password_field.clear()
        password_field.send_keys(password)

    @allure.step('Кликнуть на кнопку "Войти"')
    def click_login_button(self):
        element = self.find_element_with_wait(self.locators.login_account_btn)
        # ИСПРАВЛЕНО: Заменили прямой вызов self.driver на метод execute_javascript из BasePage
        self.execute_javascript("arguments[0].click();", element)

    @allure.step('Выполнить авторизацию пользователя')
    def login(self, email, password):
        self.set_email(email)
        self.set_password(password)
        self.click_login_button()
        
        # ИСПРАВЛЕНО: Убрали прямой WebDriverWait. Теперь вызываем метод из BasePage!
        self.wait_element_invisible(self.locators.login_account_btn)
        
    @allure.step('Проверить видимость формы авторизации')
    def is_auth_form_visible(self):
        # Дожидаемся видимости формы авторизации через ваш базовый метод
        return self.find_element_with_wait(self.locators.auth_form).is_displayed()