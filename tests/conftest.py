import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Импорты данных и путей из папки data
from data.user_data import Person
from data.urls import MainUrl, Endpoints, URLS

# Импорты готовых классов страниц из папки pages
from pages.main_page import MainPage
from pages.login_page import LoginPage

def pytest_addoption(parser):
    """Опции для выбора браузера"""
    parser.addoption("--browser", default="chrome", help="Браузер: chrome или firefox")
    parser.addoption("--headless", action="store_true", help="Запуск в headless режиме")

@pytest.fixture
def driver(request):
    """Фикстура для создания и закрытия драйвера"""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Браузер {browser_name} не поддерживается")
    
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(5)
    
    yield driver
    driver.quit()

@pytest.fixture
def main_page(driver):
    """Фикстура для главной страницы"""
    page = StellarMainPage(driver)
    page.open()
    return page

@pytest.fixture
def user_data():
    """Фикстура для генерации данных пользователя"""
    return Person.create_data_correct_user()

@pytest.fixture
def create_new_user(user_data):
    """Фикстура для создания пользователя через API"""
    base_url = MainUrl.MAIN_URL.rstrip('/')
    response = requests.post(f"{base_url}/{Endpoints.CREATE_USER}", json=user_data)
    
    yield user_data, response
    
    if response.status_code == 200:
        token = response.json()["accessToken"]
        headers = {'Authorization': token}
        requests.delete(f"{base_url}/{Endpoints.DELETE_USER}", headers=headers)

@pytest.fixture
def login_user(driver, create_new_user):
    """Фикстура для логина пользователя через UI на базе Page Object методов"""
    user_data, response = create_new_user
    
    # ФИКС: Добавлены коды [200, 201] для корректной проверки условия if
    if response.status_code not in [200, 201]:
        user_data = {
            "email": "mirinda-yo@yandex.ru",
            "password": "password090770"
        }
    
    # ФИКС: Выровнены отступы (4 пробела) для всех строк внутри фикстуры
    login_page = LoginPage(driver)
    login_page.open()
    
    # Выполняем вход (внутри этого метода уже зашито ожидание invisibility_of_element_located!)
    login_page.login(user_data["email"], user_data["password"])
    
    return user_data