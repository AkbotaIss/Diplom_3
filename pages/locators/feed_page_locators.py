from selenium.webdriver.common.by import By


class FeedPageLocators:
    FEED_TAB = (By.XPATH, "//p[text()='Лента заказов']")

    ORDERS_DONE_ALL_TIME = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p"
    )

    ORDERS_DONE_TODAY = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p"
    )

    ORDERS_IN_PROGRESS = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderListReady')]//li"
    )
