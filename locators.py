from selenium.webdriver.common.by import By

class MainPageLocators:
    # Хедер и навигация (ИСПРАВЛЕНО: сделано содержит 'Лента' для защиты от регистра букв)
    constructor_button = (By.XPATH, "//p[contains(text(), 'Конструктор')]")
    order_feed_button = (By.XPATH, "//p[contains(text(), 'Лента')]")
    personal_account_button = (By.XPATH, "//p[contains(text(), 'Личный')]")
        
    # Модальное окно деталей ингредиента
    ingredient_modal = (By.XPATH, "//h2[text()= 'Детали ингредиента']")
    close_ingredient_modal = (By.XPATH, "//button[contains(@class,'close')]")

    modal_overlay = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]")
    fluorescent_bun = (By.XPATH, "//img[@alt = 'Флюоресцентная булка R2-D3']")
    constructor_drop_area = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_top')]")
    
    # Исправленный локатор для счетчика ингредиента
    ingredient_counter = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']/../..//p[contains(@class, 'counter_counter__num__3nue1')]")
    
    # Локаторы для создания заказа (ИСПРАВЛЕНО: ищет просто слово 'Оформить' без привязки к букве 'з')
    order_button = (By.XPATH, "//button[contains(text(), 'Оформить')]")
    login_to_order_button = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")
    
    order_modal = (By.XPATH, ".//h2[contains(@class, 'Modal_modal__title_shadow__3ikwq')]")
    order_number_loading = (By.XPATH, "//h2[text()='9999']")
    order_number_final = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title_shadow__3ikwq') and not(text()='9999')]")
    close_order_modal = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]//button[contains(@class, 'close')]")


class AuthPageLocators:
    """Форма авторизации"""
    auth_form = (By.XPATH, ".//div[@class = 'Auth_login__3hAey']")
    email_input = (By.XPATH, ".//input[@name = 'name']")
    password_input = (By.XPATH, ".//input[@name = 'Пароль']")
    login_account_btn = (By.XPATH, "//button[text() = 'Войти']")
    registration_btn = (By.XPATH, "//a[text() = 'Зарегистрироваться']")
    recover_btn = (By.XPATH, "//a[text() = 'Восстановить пароль']")


class OrderFeedLocators:
    """Форма Лента заказов"""
    title_orders_list = (By.XPATH, '//h1[contains(text(), "Лента")]')
    orders_info = (By.XPATH, '//p[text()="Cостав"]')
    total_orders_counter = (By.XPATH, "//*[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    dayly_orders_counter = (By.XPATH, "//*[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    number_order_in_job = (By.XPATH, ".//li[contains(@class, 'text_type_digits-default')]")
    order_info_window = (By.XPATH, ".//li[contains(@class, 'OrderHistory_listItem__2x95r')][1]")
    order_history = (By.XPATH, './/p[contains(@class, "text_type_digits-default")]')