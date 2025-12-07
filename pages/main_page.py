from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from .base_page import BasePage


class MainPageLocators:
    # Верхнее меню
    CONSTRUCTOR_TAB = (By.XPATH, "//a[@href='/']")
    FEED_TAB = (By.XPATH, "//a[@href='/feed']")

    # Заголовки
    CONSTRUCTOR_HEADER = (By.XPATH, "//h1[text()='Соберите бургер']")
    FEED_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")

    # Ингредиент «Соус Spicy-X»
    SPICY_SAUCE_INGREDIENT = (
        By.XPATH,
        "//p[text()='Соус Spicy-X']/ancestor::a"
    )
    SPICY_SAUCE_COUNTER = (
        By.XPATH,
        "//p[text()='Соус Spicy-X']/../..//p[contains(@class,'counter')]"
    )

    # Область конструктора (на всякий случай, если пригодится drag-and-drop)
    CONSTRUCTOR_AREA = (
        By.XPATH,
        "//section[.//h1[text()='Соберите бургер']]"
    )

    # Модалка ингредиента
    INGREDIENT_MODAL_TITLE = (
        By.XPATH,
        "//h2[text()='Детали ингредиента']"
    )
    INGREDIENT_MODAL_CLOSE = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//button[contains(@class,'close')]"
    )

    # Кнопка «Добавить» внутри модалки
    ADD_INGREDIENT_BUTTON = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]//button[text()='Добавить']"
    )


class MainPage(BasePage):
    def open_main(self):
        self.open("/")

    # Навигация по вкладкам
    def go_to_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_TAB)

    def go_to_feed(self):
        self.click(MainPageLocators.FEED_TAB)

    def is_constructor_open(self) -> bool:
        return self.is_visible(MainPageLocators.CONSTRUCTOR_HEADER)

    def is_feed_open(self) -> bool:
        return self.is_visible(MainPageLocators.FEED_HEADER)

    # Работа с ингредиентом и модалкой
    def open_ingredient_details(self):
        """Открываем модалку ингредиента. В Firefox обычный click может перехватываться оверлеем,
        поэтому используем JavaScript-клик — он надёжнее.
        """
        element = self.driver.find_element(*MainPageLocators.SPICY_SAUCE_INGREDIENT)
        self.driver.execute_script("arguments[0].click();", element)

    def is_ingredient_modal_open(self) -> bool:
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def close_ingredient_modal(self):
        """Закрываем модалку по крестику и ждём, пока заголовок исчезнет."""
        self.click(MainPageLocators.INGREDIENT_MODAL_CLOSE)
        # ждём, пока модалка исчезнет
        return self.is_not_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def is_ingredient_modal_closed(self) -> bool:
        return self.is_not_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def get_spicy_sauce_counter(self) -> int:
        text = self.get_element_text(MainPageLocators.SPICY_SAUCE_COUNTER)
        return int(text) if text else 0

    def add_spicy_sauce_to_burger(self):
        """Добавляем ингредиент в заказ через кнопку 'Добавить' в модалке."""
        self.click(MainPageLocators.ADD_INGREDIENT_BUTTON)

    # Если вдруг захочешь вернуться к drag-and-drop — оставлю метод на будущее:
    def drag_spicy_sauce_to_constructor(self):
        ingredient = self.wait.until(
            lambda d: d.find_element(*MainPageLocators.SPICY_SAUCE_INGREDIENT)
        )
        target = self.wait.until(
            lambda d: d.find_element(*MainPageLocators.CONSTRUCTOR_AREA)
        )

        actions = ActionChains(self.driver)
        (
            actions
            .move_to_element(ingredient)
            .click_and_hold(ingredient)
            .move_to_element(target)
            .pause(0.5)
            .release()
            .perform()
        )
