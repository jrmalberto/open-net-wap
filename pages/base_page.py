import sys
import time

from selenium.common import TimeoutException, NoSuchElementException, ElementNotVisibleException, \
    ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    """
    BasePage class to contain commonly used page interactions to avoid code repeatability
    and follow DRY principle
    """

    def __init__(self, driver: WebDriver, url=None, title=None):
        """
        Main constructor for all page objects, with attributes common to any page

        :param driver: WebDriver instance used by the page instance
        :param url: URL of the page
        :param title: Page Title
        """
        self.driver = driver
        self.url = url
        self.title = title
        self.action = ActionChains(self.driver)

    def go_to_link(self, url: str) -> None:
        """
        Method to go to a specific `url`.

        :param url: URL as `str` to be passed
        """
        self.driver.get(url)

    def click_element(self, element: tuple | WebElement, timeout: float = 10) -> None:
        """
        Method to click() a WebElement

        :param element: WebElement's locator as a `tuple` or `WebElement` objects
        :param timeout: Amount of time to pass to `wait_and_get_element`
        """
        try:
            if isinstance(element, tuple):
                self.wait_and_get_element(element, timeout).click()
            else:
                element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            if isinstance(element, tuple):
                element = self.wait_and_get_element(element, timeout)
            self.action.click(element).perform()

    def clear_text_field(self, element: tuple, timeout: float = 10) -> None:
        """
        Method to clear() a WebElement's text

        :param element: WebElement's locator as a `tuple`
        :param timeout: Amount of time to pass to `wait_and_get_element`
        """
        self.wait_and_get_element(element, timeout).clear()

    def set_text_field(self, element: tuple, text, timeout: float = 10) -> None:
        """
        Method to send_keys() to a WebElement

        :param element: WebElement's locator as a `tuple`
        :param timeout: Amount of time to pass to `wait_and_get_element`
        :param text: Input text
        """
        self.clear_text_field(element, timeout)
        self.driver.find_element(*element).send_keys(text)

    def get_element_text(self, element: tuple | WebElement, timeout: float = 10) -> str:
        """
        Method to get text from a WebElement

        :param element: WebElement's locator as a `tuple`
        :param timeout: Amount of time to pass to `wait_and_get_element`
        :return: Text of WebElement
        """
        return self.wait_and_get_element(element, timeout).text

    def get_attribute_content(self, element: tuple, attribute_name: str,
                              timeout: float = 10) -> str:
        """
        Method to get content of WebElement's attribute

        :param element: WebElement `tuple` to interact with
        :param attribute_name: ex: 'value', 'id',..., etc
        :param timeout: Amount of time to wait in seconds
        """
        return self.wait_and_get_element(element, timeout).get_attribute(attribute_name)

    def js_scroll_into_view(self, element: tuple | WebElement,
                            timeout: float = 10) -> None:
        """
        Method to scroll to an element until it's in view using javascript.

        :param element: Locator tuple or WebElement
        :param timeout: Amount of time to pass to `wait_and_get_element`
        """
        if isinstance(element, tuple):
            element = self.wait_and_get_element(element, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_for_page_load(self, timeout: float = 5):
        self.driver.implicitly_wait(timeout)

    def wait_and_get_element(self, element: tuple, timeout: float = 15) -> WebElement:
        """
        Method to deal with waiting for an element and finding it in the DOM.

        :param element: WebElement's locator as a `tuple`
        :param timeout: Time in seconds we want to wait when locating elements
        :return: WebElement to be interacted with
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.all_of(
                    EC.visibility_of_element_located(element),
                    EC.presence_of_element_located(element),
                )
            )
            return self.driver.find_element(*element)
        except (TimeoutException, NoSuchElementException,
                ElementNotVisibleException):
            error = self.get_exception()
            self.meta_raise(error)

    def wait_and_get_elements(self, element: tuple, timeout: float = 15) -> list[WebElement]:
        """
        Method to deal with waiting for all elements and finding them in the DOM.

        :param element: WebElements' locator as a `tuple`
        :param timeout: Time in seconds we want to wait when locating elements
        :return: a list of WebElements to be interacted with
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.all_of(
                    EC.visibility_of_all_elements_located(element),
                    EC.presence_of_all_elements_located(element),
                )
            )
            return self.driver.find_elements(*element)
        except (TimeoutException, NoSuchElementException,
                ElementNotVisibleException):
            error = self.get_exception()
            self.meta_raise(error)

    @staticmethod
    def get_exception():
        """
            Method to return sys.exc_info() exceptions
        """
        return sys.exc_info()

    @staticmethod
    def meta_raise(exc_info):
        """
            Method to raise caught exceptions with traceback
        """
        raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
