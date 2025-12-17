import allure

from urls import BASE_URL
from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.suite("Лента заказов")
class TestFeedPage:

    @allure.title("При создании заказа счётчик 'Выполнено за всё время' увеличивается")
    def test_orders_done_all_time_increases(self, driver, create_order):
        feed_page = FeedPage(driver, BASE_URL)
        main_page = MainPage(driver, BASE_URL)

        main_page.open_main()
        feed_page.open_feed()

        initial = feed_page.get_orders_done_all_time()

        create_order()  # создаём заказ через API

        feed_page.refresh()
        feed_page.wait_all_time_increases(initial)
        updated = feed_page.get_orders_done_all_time()

        assert updated > initial

    @allure.title("При создании заказа счётчик 'Выполнено за сегодня' увеличивается")
    def test_orders_done_today_increases(self, driver, create_order):
        feed_page = FeedPage(driver, BASE_URL)
        main_page = MainPage(driver, BASE_URL)

        main_page.open_main()
        feed_page.open_feed()

        initial = feed_page.get_orders_done_today()

        create_order()  # создаём заказ через API

        feed_page.refresh()
        feed_page.wait_today_increases(initial)
        updated = feed_page.get_orders_done_today()

        assert updated > initial

    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    def test_new_order_appears_in_progress(self, driver, create_order):
        feed_page = FeedPage(driver, BASE_URL)
        main_page = MainPage(driver, BASE_URL)

        order_number = create_order()  # номер заказа из API

        main_page.open_main()
        feed_page.open_feed()

        feed_page.wait_order_in_progress(order_number)
        in_progress_numbers = feed_page.get_orders_in_progress()

        assert str(order_number) in in_progress_numbers