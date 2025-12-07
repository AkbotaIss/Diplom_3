import allure

from pages.base_page import BasePage
from pages.locators.feed_page_locators import FeedPageLocators


class FeedPage(BasePage):

    @allure.step("Получить количество заказов за всё время")
    def get_orders_done_all_time(self) -> int:
        raw_text = self.get_text(FeedPageLocators.ORDERS_DONE_ALL_TIME)
        # На всякий случай вытащим только цифры, если там есть слова/пробелы
        digits = "".join(ch for ch in raw_text if ch.isdigit())
        return int(digits)

    @allure.step("Получить количество заказов за сегодня")
    def get_orders_done_today(self) -> int:
        raw_text = self.get_text(FeedPageLocators.ORDERS_DONE_TODAY)
        digits = "".join(ch for ch in raw_text if ch.isdigit())
        return int(digits)

    @allure.step("Получить список заказов в работе")
    def get_orders_in_progress(self) -> list[str]:
        elements = self.find_elements(FeedPageLocators.ORDERS_IN_PROGRESS)
        return [el.text for el in elements]
