import allure

from urls import BASE_URL
from pages.main_page import MainPage


@allure.suite("Главная страница")
class TestMainPage:

    @allure.title("Переход по клику на «Конструктор»")
    def test_go_to_constructor(self, driver):
        page = MainPage(driver, BASE_URL)
        page.open_main()

        page.go_to_feed()
        page.go_to_constructor()

        assert page.is_constructor_open()

    @allure.title("Переход по клику на раздел «Лента заказов»")
    def test_go_to_feed(self, driver):
        page = MainPage(driver, BASE_URL)
        page.open_main()

        page.go_to_feed()

        assert page.is_feed_open()

    @allure.title("Клик по ингредиенту открывает всплывающее окно с деталями")
    def test_ingredient_click_opens_modal(self, driver):
        page = MainPage(driver, BASE_URL)
        page.open_main()

        page.open_ingredient_details()

        assert page.is_ingredient_modal_open()

    @allure.title("Всплывающее окно закрывается по крестику")
    def test_close_ingredient_modal(self, driver):
        page = MainPage(driver, BASE_URL)
        page.open_main()

        page.open_ingredient_details()
        assert page.is_ingredient_modal_open()

        page.close_ingredient_modal()

        assert page.is_ingredient_modal_closed()

    @allure.title("При добавлении ингредиента счётчик увеличивается")
    def test_ingredient_counter_increases(self, driver):
        page = MainPage(driver, BASE_URL)
        page.open_main()

        initial = page.get_spicy_sauce_counter()

        page.open_ingredient_details()
        page.add_spicy_sauce_to_burger()

        page.wait_spicy_sauce_counter_to_increase(initial)

        updated = page.get_spicy_sauce_counter()
        assert updated == initial + 1