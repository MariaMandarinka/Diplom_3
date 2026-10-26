import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.epic("Дипломный проект: Stellar Burgers")
@allure.feature("Раздел Лента заказов")
class TestOrderFeed:

    @allure.title('При создании нового заказа счётчик "Выполнено за всё время" увеличивается')
    def test_new_order_increases_total_counter(self, login_user, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        main_page.click_order_feed()
        order_feed_page.is_order_feed_page_loaded()
        initial_total = order_feed_page.get_total_orders_count()
        
        main_page.click_constructor()
        main_page.create_order_ui()
        
        main_page.click_order_feed()
        order_feed_page.wait_for_counters_update(initial_total, 0)
        new_total = order_feed_page.get_total_orders_count()
        
        # СТРОГО ЕДИНСТВЕННЫЙ ФИНАЛЬНЫЙ АССЕРТ В ТЕСТЕ
        assert new_total > initial_total, f"Счетчик 'Выполнено за все время' не увеличился. Было: {initial_total}, стало: {new_total}"

    @allure.title('При создании нового заказа счётчик "Выполнено за сегодня" увеличивается')
    def test_new_order_increases_today_counter(self, login_user, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        main_page.click_order_feed()
        order_feed_page.is_order_feed_page_loaded()
        initial_today = order_feed_page.get_today_orders_count()
        
        main_page.click_constructor()
        main_page.create_order_ui()
        
        main_page.click_order_feed()
        order_feed_page.wait_for_counters_update(0, initial_today)
        new_today = order_feed_page.get_today_orders_count()
        
        # СТРОГО ЕДИНСТВЕННЫЙ ФИНАЛЬНЫЙ АССЕРТ В ТЕСТЕ
        assert new_today > initial_today, f"Счетчик 'Выполнено за сегодня' не увеличился. Было: {initial_today}, стало: {new_today}"

    @allure.title('После оформления заказа его номер появляется в разделе "В работе"')
    def test_order_number_appears_in_progress(self, login_user, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        main_page.click_order_feed()
        order_feed_page.is_order_feed_page_loaded()
        
        main_page.click_constructor()
        order_number = main_page.create_order_ui()
        
        main_page.click_order_feed()
        normalized_order_number = order_feed_page.normalize_order_number(order_number)
        order_feed_page.wait_for_order_in_progress(normalized_order_number)
        orders_in_progress_normalized = order_feed_page.get_orders_in_progress_normalized()
        
        # СТРОГО ЕДИНСТВЕННЫЙ ФИНАЛЬНЫЙ АССЕРТ В ТЕСТЕ
        assert normalized_order_number in orders_in_progress_normalized, (
            f"Заказ {order_number} не найден в разделе 'В работе'."
        )