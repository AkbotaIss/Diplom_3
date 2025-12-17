# pages/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from .base_page import BasePage


class MainPageLocators:
    # вкладки
    FEED_TAB = (By.XPATH, "//a[contains(@href,'/feed')]")
    CONSTRUCTOR_TAB = (By.XPATH, "//a[@href='/' or contains(@href,'/#')]")

    # заголовок конструктора
    CONSTRUCTOR_HEADER = (By.XPATH, "//h1[contains(text(),'Соберите бургер')]")

    # карточка ингредиента
    SPICY_SAUCE_CARD = (By.XPATH, "//p[text()='Соус Spicy-X']/ancestor::a")

    # счётчик на карточке (если счётчика нет — считаем 0)
    SPICY_SAUCE_COUNTER = (
        By.XPATH,
        "//p[text()='Соус Spicy-X']/ancestor::a//p[contains(@class,'counter_counter__num')]"
    )

    # зона конструктора (куда делаем drop)
    CONSTRUCTOR_DROP_AREA = (
        By.XPATH,
        "//section[contains(@class,'BurgerConstructor_basket__')]"
    )

    # модалка ингредиента + закрытие
    INGREDIENT_MODAL = (By.XPATH, "//section[contains(@class,'Modal_modal__container')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[contains(@class,'Modal_modal__close')]")

    # оформление заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Оформить заказ')]")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class,'Modal_modal__title')]")


class MainPage(BasePage):
    def open_main(self):
        self.open("")
        self.wait_visible(MainPageLocators.CONSTRUCTOR_HEADER)

    # ---- Навигация ----
    def go_to_feed(self):
        self.click(MainPageLocators.FEED_TAB)

    def go_to_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_TAB)

    def is_feed_open(self) -> bool:
        return "/feed" in self.driver.current_url

    def is_constructor_open(self) -> bool:
        return "/feed" not in self.driver.current_url

    # ---- Ингредиенты / модалка ----
    def open_ingredient_details(self):
        self.click(MainPageLocators.SPICY_SAUCE_CARD)
        self.wait_visible(MainPageLocators.INGREDIENT_MODAL)

    def is_ingredient_modal_open(self) -> bool:
        try:
            self.wait_visible(MainPageLocators.INGREDIENT_MODAL)
            return True
        except Exception:
            return False

    def close_ingredient_modal(self):
        self.click(MainPageLocators.CLOSE_MODAL_BUTTON)
        self.wait_invisible(MainPageLocators.INGREDIENT_MODAL)

    def is_ingredient_modal_closed(self) -> bool:
        try:
            return bool(self.wait_invisible(MainPageLocators.INGREDIENT_MODAL))
        except Exception:
            return True

    # ---- Счётчик ингредиента ----
    def get_spicy_sauce_counter(self) -> int:
        try:
            return int(self.get_text(MainPageLocators.SPICY_SAUCE_COUNTER).strip())
        except Exception:
            return 0

    def add_spicy_sauce_to_burger(self):
        """

        """
        source = self.wait_visible(MainPageLocators.SPICY_SAUCE_CARD)
        target = self.wait_visible(MainPageLocators.CONSTRUCTOR_DROP_AREA)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def wait_spicy_sauce_counter_to_increase(self, old_value: int):
        self.wait.until(lambda d: self.get_spicy_sauce_counter() > old_value)

    # ---- Создание заказа через UI (понадобится для ленты) ----
    def create_order_via_ui(self) -> str:
        """

        """
        self.add_spicy_sauce_to_burger()
        self.click(MainPageLocators.ORDER_BUTTON)
        order_number = self.get_text(MainPageLocators.ORDER_NUMBER).strip()


        try:
            self.click(MainPageLocators.CLOSE_MODAL_BUTTON)
        except Exception:
            pass

        return order_number