from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
import locators.homepage as locs
from pages.streamer_page import StreamerPage


class HomePage(BasePage):

    def __init__(self, driver: WebDriver, mobile=True):
        super().__init__(driver)
        if mobile:
            self.url = "https://m.twitch.tv/"
        else:
            self.url = "https://twitch.tv/"
        self.title = "Twitch"

    def click_search_btn(self):
        """
        Click the search magnifying glass icon
        """
        self.click_element(locs.SEARCH_ICON)

    def input_search(self, text: str):
        """
        Write search input

        :param text: Text to search
        """
        self.set_text_field(locs.SEARCH_INPUT, text)

    def get_search_suggestions(self):
        """
        Get all search suggestion results

        :return: List of WebElement containing all suggestion results
        """

        return self.wait_and_get_elements(locs.SEARCH_SUGGESTIONS)

    def select_search_suggestion(self, index: int):
        """
        Search for specific suggestion at `index`

        :param index: Index of the suggestion to click
        """
        suggestions = self.get_search_suggestions()
        self.click_element(suggestions[index])

    def get_search_results(self):
        """
        Get stream results

        :return: List of WebElement containing each stream
        """
        return self.wait_and_get_elements(locs.SEARCH_RESULTS_ARTICLES)

    def select_search_result(self, result_element: WebElement) -> StreamerPage:
        """
        Select which stream to watch

        :param result_element: WebElememt to be clicked
        :return: StreamerPage object
        """
        self.click_element(result_element)
        return StreamerPage(self.driver)
