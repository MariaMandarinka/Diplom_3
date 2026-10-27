class MainUrl:
    # Главный базовый домен тестового стенда Stellar Burgers
    MAIN_URL = 'https://qa-stellarburgers.education-services.ru/'


class URLS:
    """URL-адреса страниц сервиса для открытия в браузере (UI-тесты)"""
    url_feed = 'feed'                      # Лента заказов
    url_login = 'login'                    # Авторизация
    url_recovery = 'forgot-password'        # Восстановление пароля
    url_register = 'register'              # Регистрация пользователя
    url_profile_area = 'account/profile'    # Личный кабинет
    url_history_order = 'account/order-history' # История заказов
    url_reset_password = 'reset-password'  # Сброс пароля


class Endpoints:
    """Ручки бэкенда для выполнения быстрых сетевых запросов (API)"""
    CREATE_USER = 'api/auth/register'       # Создание пользователя
    LOGIN = 'api/auth/login'                # Вход в систему (генерация токена)
    DELETE_USER = 'api/auth/user'           # Удаление пользователя из базы
    CREATE_ORDER = 'api/orders'             # Создание заказа
    GET_ORDERS = 'api/orders'               # Получение списка заказов юзера
    GET_USER_ORDERS = 'api/orders'          # Заказы конкретного пользователя
    GET_ALL_ORDERS = 'api/orders/all'       # Общая Лента всех заказов в системе