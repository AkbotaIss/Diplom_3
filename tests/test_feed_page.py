import allure

from urls import BASE_URL
from pages.main_page import MainPage
from pages.feed_page import FeedPage


@allure.title("При создании заказа счётчик 'Выполнено за всё время' увеличивается")
def test_orders_done_all_time_increases(driver, create_order):
    main_page = MainPage(driver, BASE_URL)
    main_page.open_main()
    main_page.go_to_feed()

    feed_page = FeedPage(driver, BASE_URL)

    # начальное значение
    initial = feed_page.get_orders_done_all_time()

    # создаём заказ через API
    create_order()

    # обновляем страницу ленты
    driver.refresh()

    # ждём, пока счётчик станет больше
    feed_page.wait.until(
        lambda d: feed_page.get_orders_done_all_time() > initial
    )

    updated = feed_page.get_orders_done_all_time()
    assert updated > initial


@allure.title("При создании заказа счётчик 'Выполнено за сегодня' увеличивается")
def test_orders_done_today_increases(driver, create_order):
    main_page = MainPage(driver, BASE_URL)
    main_page.open_main()
    main_page.go_to_feed()

    feed_page = FeedPage(driver, BASE_URL)

    initial = feed_page.get_orders_done_today()

    create_order()

    driver.refresh()

    feed_page.wait.until(
        lambda d: feed_page.get_orders_done_today() > initial
    )

    updated = feed_page.get_orders_done_today()
    assert updated > initial


@allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
def test_new_order_appears_in_progress(driver, create_order):
    # создаём заказ и запоминаем номер
    order_number = create_order()

    main_page = MainPage(driver, BASE_URL)
    main_page.open_main()
    main_page.go_to_feed()

    feed_page = FeedPage(driver, BASE_URL)

    driver.refresh()

    # ждём, пока номер появится в списке "В работе"
    feed_page.wait.until(
        lambda d: str(order_number) in feed_page.get_orders_in_progress()
    )

    in_progress_numbers = feed_page.get_orders_in_progress()
    assert str(order_number) in in_progress_numbers
