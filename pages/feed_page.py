import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class FeedPageLocators:
    FEED_HEADER = (By.XPATH, "//h1[contains(text(),'Лента заказов')]")

    ORDERS_DONE_ALL_TIME = (
        By.XPATH,
        "//p[contains(text(),'Выполнено за все время')]/following-sibling::p"
    )
    ORDERS_DONE_TODAY = (
        By.XPATH,
        "//p[contains(text(),'Выполнено за сегодня')]/following-sibling::p"
    )

    ORDERS_IN_PROGRESS = (
        By.XPATH,
        "//p[contains(text(),'В работе')]/following-sibling::ul//p[contains(@class,'text_type_digits-default')]"
    )
    ORDERS_IN_PROGRESS_FALLBACK = (
        By.XPATH,
        "//section[.//p[contains(text(),'В работе')]]//ul//p[contains(@class,'text_type_digits-default')]"
    )


class FeedPage(BasePage):

    @allure.step("Открыть страницу ленты заказов")
    def open_feed(self):
        self.open("/feed")
        self.wait_visible(FeedPageLocators.FEED_HEADER)

    @allure.step("Получить значение счётчика 'Выполнено за всё время'")
    def get_orders_done_all_time(self) -> int:
        return self.get_number(FeedPageLocators.ORDERS_DONE_ALL_TIME)

    @allure.step("Получить значение счётчика 'Выполнено за сегодня'")
    def get_orders_done_today(self) -> int:
        return self.get_number(FeedPageLocators.ORDERS_DONE_TODAY)

    @allure.step("Дождаться увеличения 'Выполнено за всё время' (было: {old_value})")
    def wait_all_time_increases(self, old_value: int):
        self.wait_until(lambda d: self.get_orders_done_all_time() > old_value)

    @allure.step("Дождаться увеличения 'Выполнено за сегодня' (было: {old_value})")
    def wait_today_increases(self, old_value: int):
        self.wait_until(lambda d: self.get_orders_done_today() > old_value)

    @allure.step("Получить список номеров заказов в блоке 'В работе'")
    def get_orders_in_progress(self) -> list[str]:
        elements = self.find_elements(FeedPageLocators.ORDERS_IN_PROGRESS)
        if not elements:
            elements = self.find_elements(FeedPageLocators.ORDERS_IN_PROGRESS_FALLBACK)

        return [el.text.strip() for el in elements if el.text and el.text.strip()]

    @allure.step("Дождаться появления заказа {order_number} в блоке 'В работе'")
    def wait_order_in_progress(self, order_number: int):
        self.wait_until(lambda d: str(order_number) in self.get_orders_in_progress())