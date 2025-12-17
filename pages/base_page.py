import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, driver, base_url, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    # ---------- navigation ----------
    @allure.step("Открыть страницу: {path}")
    def open(self, path: str = ""):
        self.driver.get(self.base_url + path)

    @allure.step("Обновить страницу")
    def refresh(self):
        self.driver.refresh()

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    # ---------- wait / find ----------
    @allure.step("Подождать присутствие элемента")
    def wait_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Подождать видимость элемента")
    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Подождать исчезновение элемента")
    def wait_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Найти элементы")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Подождать кастомное условие")
    def wait_until(self, condition, timeout: int | None = None):
        if timeout is not None:
            WebDriverWait(self.driver, timeout).until(condition)
        else:
            self.wait.until(condition)

    # ---------- actions ----------
    @allure.step("Клик по элементу")
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step("JS-клик по элементу")
    def js_click(self, locator):
        element = self.wait_presence(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Drag&Drop элемента")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.wait_visible(source_locator)
        target = self.wait_visible(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    # ---------- getters ----------
    @allure.step("Получить текст элемента")
    def get_text(self, locator) -> str:
        return self.wait_visible(locator).text

    @allure.step("Получить число из элемента")
    def get_number(self, locator) -> int:
        return int(self.get_text(locator).strip())

    # ---------- custom waits ----------
    @allure.step("Дождаться изменения текста")
    def wait_text_changes(self, locator, old_text: str):
        self.wait_until(lambda d: self.get_text(locator) != old_text)

    @allure.step("Дождаться увеличения числа")
    def wait_number_greater(self, locator, old_value: int):
        self.wait_until(lambda d: self.get_number(locator) > old_value)

    @allure.step("Дождаться равенства числа")
    def wait_number_equals(self, locator, expected: int):
        self.wait_until(lambda d: self.get_number(locator) == expected)