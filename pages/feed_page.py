from selenium.webdriver.common.by import By

from .base_page import BasePage


class FeedPageLocators:
    # Заголовок страницы
    FEED_HEADER = (By.XPATH, "//h1[contains(text(),'Лента заказов')]")

    # Счётчики
    ORDERS_DONE_ALL_TIME = (
        By.XPATH,
        "//p[contains(text(),'Выполнено за все время')]/following-sibling::p",
    )
    ORDERS_DONE_TODAY = (
        By.XPATH,
        "//p[contains(text(),'Выполнено за сегодня')]/following-sibling::p",
    )


    ORDERS_IN_PROGRESS = (
        By.XPATH,
        "//p[contains(text(),'В работе')]/following-sibling::ul//p[contains(@class,'text_type_digits-default')]",
    )


    ORDERS_IN_PROGRESS_FALLBACK = (
        By.XPATH,
        "//section[.//p[contains(text(),'В работе')]]//ul//p[contains(@class,'text_type_digits-default')]",
    )


class FeedPage(BasePage):
    def open_feed(self):
        self.open("/feed")
        self.wait_visible(FeedPageLocators.FEED_HEADER)

    def get_orders_done_all_time(self) -> int:
        return int(self.get_text(FeedPageLocators.ORDERS_DONE_ALL_TIME).strip())

    def get_orders_done_today(self) -> int:
        return int(self.get_text(FeedPageLocators.ORDERS_DONE_TODAY).strip())

    def wait_all_time_increases(self, old_value: int):
        self.wait_number_greater(FeedPageLocators.ORDERS_DONE_ALL_TIME, old_value)

    def wait_today_increases(self, old_value: int):
        self.wait_number_greater(FeedPageLocators.ORDERS_DONE_TODAY, old_value)

    def get_orders_in_progress(self) -> list[str]:
        elements = self.driver.find_elements(*FeedPageLocators.ORDERS_IN_PROGRESS)

        if not elements:
            elements = self.driver.find_elements(*FeedPageLocators.ORDERS_IN_PROGRESS_FALLBACK)

        return [el.text.strip() for el in elements if el.text and el.text.strip()]

    def wait_order_in_progress(self, order_number: int):
        self.wait.until(lambda d: str(order_number) in self.get_orders_in_progress())