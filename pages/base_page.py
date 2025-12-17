from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, base_url, timeout=10):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path=""):
        self.driver.get(self.base_url + path)

    # ---- waits ----
    def wait_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    # ---- actions ----
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def js_click(self, locator):
        element = self.wait_presence(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def refresh(self):
        self.driver.refresh()

    # ---- getters ----
    def get_text(self, locator) -> str:
        return self.wait_visible(locator).text.strip()

    def get_number(self, locator) -> int:
        return int(self.get_text(locator))

    # ---- custom waits ----
    def wait_text_changes(self, locator, old_text: str):
        self.wait.until(lambda d: self.get_text(locator) != old_text)

    def wait_number_greater(self, locator, old_value: int):
        self.wait.until(lambda d: self.get_number(locator) > old_value)

    def wait_number_equals(self, locator, expected: int):
        self.wait.until(lambda d: self.get_number(locator) == expected)