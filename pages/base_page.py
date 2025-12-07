import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 30)

    @allure.step("Открыть страницу {path}")
    def open(self, path: str = ""):
        """
        Открывает страницу по относительному пути.
        Если path пустой — открывается просто BASE_URL.
        """
        url = self.base_url + path
        self.driver.get(url)

    def click(self, locator):
        """
        Клик по элементу, когда он кликабелен.
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def find_element(self, locator):
        """
        Найти один элемент и дождаться его видимости.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        """
        Найти список элементов (без явного ожидания каждого).
        """
        return self.driver.find_elements(*locator)

    def get_text(self, locator) -> str:
        """
        Получить текст элемента по локатору.
        """
        return self.find_element(locator).text
