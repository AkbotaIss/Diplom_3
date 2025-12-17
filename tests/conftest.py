import pytest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from urls import INGREDIENTS_API_URL, ORDERS_API_URL


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )

    elif browser == "firefox":
        options = FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
        driver.maximize_window()

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver
    driver.quit()


@pytest.fixture
def create_order():
    """
    Создаёт заказ через API и возвращает номер заказа.
    """

    def _create_order() -> int:
        # получаем ингредиенты
        ingredients_response = requests.get(INGREDIENTS_API_URL)
        ingredients_response.raise_for_status()

        ingredients = ingredients_response.json()["data"]
        ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]

        # создаём заказ
        order_response = requests.post(
            ORDERS_API_URL,
            json={"ingredients": ingredient_ids},
        )
        order_response.raise_for_status()

        return order_response.json()["order"]["number"]

    return _create_order
