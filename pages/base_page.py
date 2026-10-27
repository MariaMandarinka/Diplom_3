import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть страницу по URL")
    def open_url(self, url):
        self.driver.get(url)

    @allure.step("Найти элемент с ожиданием видимости")
    def find_element_with_wait(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Найти несколько элементов")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Кликнуть по элементу через JavaScript")
    def click_via_js(self, locator):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Получить текст элемента")
    def get_element_text(self, locator):
        element = self.find_element_with_wait(locator)
        return element.text.strip()
    
    @allure.step("Выполнить JavaScript-скрипт в контексте браузера")
    def execute_javascript(self, script, element):
        # Если мы передаем "arguments[0].click();", заменяем это на полноценный клик через событие мыши MouseEvent.
        # Это защитит тесты от ошибок "is not a function" на реактовых элементах Практикума!
        if script == "arguments[0].click();":
            click_script = (
                "var evt = document.createEvent('MouseEvents');"
                "evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);"
                "arguments[0].dispatchEvent(evt);"
            )
            return self.driver.execute_script(click_script, element)
            
        # Для остальных скриптов (например, удаления атрибутов) оставляем стандартное выполнение
        return self.driver.execute_script(script, element)
    
    @allure.step("Дождаться, пока элемент станет невидимым/исчезнет с экрана")
    def wait_element_invisible(self, locator, timeout=15):
        # Переносим WebDriverWait со страниц строго сюда
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Дождаться выполнения кастомного условия (лямбды)")
    def wait_for_condition(self, condition_lambda, timeout=15):
        # Универсальный метод для кастомных ожиданий (например, счетчиков)
        return WebDriverWait(self.driver, timeout).until(condition_lambda)