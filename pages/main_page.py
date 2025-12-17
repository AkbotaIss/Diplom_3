import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class MainPageLocators:
    FEED_TAB = (By.XPATH, "//a[contains(@href,'/feed')]")
    CONSTRUCTOR_TAB = (By.XPATH, "//a[@href='/' or contains(@href,'/#')]")

    CONSTRUCTOR_HEADER = (By.XPATH, "//h1[contains(text(),'Соберите бургер')]")

    SPICY_SAUCE_CARD = (By.XPATH, "//p[text()='Соус Spicy-X']/ancestor::a")

    SPICY_SAUCE_COUNTER = (
        By.XPATH,
        "//p[text()='Соус Spicy-X']/ancestor::a//p[contains(@class,'counter_counter__num')]"
    )

    CONSTRUCTOR_DROP_AREA = (By.XPATH, "//section[contains(@class,'BurgerConstructor_basket__')]")

    INGREDIENT_MODAL = (By.XPATH, "//section[contains(@class,'Modal_modal__container')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[contains(@class,'Modal_modal__close')]")

    ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Оформить заказ')]")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class,'Modal_modal__title')]")


class MainPage(BasePage):

    @allure.step("Открыть главную страницу")
    def open_main(self):
        self.open("")
        self.wait_visible(MainPageLocators.CONSTRUCTOR_HEADER)

    # ---- Навигация ----
    @allure.step("Перейти в ленту заказов")
    def go_to_feed(self):
        self.click(MainPageLocators.FEED_TAB)

    @allure.step("Перейти в конструктор")
    def go_to_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_TAB)

    @allure.step("Проверить, что открыта лента заказов")
    def is_feed_open(self) -> bool:
        return "/feed" in self.get_current_url()

    @allure.step("Проверить, что открыт конструктор")
    def is_constructor_open(self) -> bool:
        return "/feed" not in self.get_current_url()

    # ---- Модалка ингредиента ----
    @allure.step("Открыть детали ингредиента")
    def open_ingredient_details(self):
        self.click(MainPageLocators.SPICY_SAUCE_CARD)
        self.wait_visible(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Проверить, что модалка ингредиента открыта")
    def is_ingredient_modal_open(self) -> bool:
        try:
            self.wait_visible(MainPageLocators.INGREDIENT_MODAL)
            return True
        except Exception:
            return False

    @allure.step("Закрыть модалку ингредиента")
    def close_ingredient_modal(self):
        self.click(MainPageLocators.CLOSE_MODAL_BUTTON)
        self.wait_invisible(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Проверить, что модалка ингредиента закрыта")
    def is_ingredient_modal_closed(self) -> bool:
        try:
            return bool(self.wait_invisible(MainPageLocators.INGREDIENT_MODAL))
        except Exception:
            return True

    # ---- Счётчик ингредиента ----
    @allure.step("Получить значение счётчика соуса Spicy-X")
    def get_spicy_sauce_counter(self) -> int:
        try:
            return int(self.get_text(MainPageLocators.SPICY_SAUCE_COUNTER).strip())
        except Exception:
            return 0

    @allure.step("Перетащить соус Spicy-X в конструктор")
    def add_spicy_sauce_to_burger(self):
        self.drag_and_drop(MainPageLocators.SPICY_SAUCE_CARD, MainPageLocators.CONSTRUCTOR_DROP_AREA)

    @allure.step("Дождаться увеличения счётчика соуса (было: {old_value})")
    def wait_spicy_sauce_counter_to_increase(self, old_value: int):
        self.wait_until(lambda d: self.get_spicy_sauce_counter() > old_value)

    # ---- Создание заказа через UI ----
    @allure.step("Создать заказ через UI и вернуть номер")
    def create_order_via_ui(self) -> str:
        self.add_spicy_sauce_to_burger()
        self.click(MainPageLocators.ORDER_BUTTON)

        order_number = self.get_text(MainPageLocators.ORDER_NUMBER).strip()


        try:
            self.click(MainPageLocators.CLOSE_MODAL_BUTTON)
        except Exception:
            pass

        return order_number