import allure

from urls import BASE_URL
from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.suite("Лента заказов")
class TestFeedPage:

    @allure.title("При создании заказа счётчик 'Выполнено за всё время' увеличивается")
    def test_orders_done_all_time_increases(self, driver):
        feed_page = FeedPage(driver, BASE_URL)
        main_page = MainPage(driver, BASE_URL)

        feed_page.open_feed()
        initial = feed_page.get_orders_done_all_time()

        main_page.open_main()
        main_page.create_order_via_ui()

        feed_page.open_feed()
        feed_page.wait_all_time_increases(initial)

        updated = feed_page.get_orders_done_all_time()
        assert updated > initial

    @allure.title("При создании заказа счётчик 'Выполнено за сегодня' увеличивается")
    def test_orders_done_today_increases(self, driver):
        feed_page = FeedPage(driver, BASE_URL)
        main_page = MainPage(driver, BASE_URL)

        feed_page.open_feed()
        initial = feed_page.get_orders_done_today()

        main_page.open_main()
        main_page.create_order_via_ui()

        feed_page.open_feed()
        feed_page.wait_today_increases(initial)

        updated = feed_page.get_orders_done_today()
        assert updated > initial

    @allure.title("Созданный заказ появляется в разделе 'В работе'")
    def test_new_order_appears_in_progress(self, driver):
        feed_page = FeedPage(driver, BASE_URL)
        main_page = MainPage(driver, BASE_URL)

        main_page.open_main()
        order_number = int(main_page.create_order_via_ui())

        feed_page.open_feed()
        feed_page.wait_order_in_progress(order_number)

        assert str(order_number) in feed_page.get_orders_in_progress()