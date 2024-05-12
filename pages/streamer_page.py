from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
import locators.streamer_page as locs


class StreamerPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://m.twitch.tv/velocitish"

    def get_user_and_game(self) -> [WebElement]:
        """
        Method to get the username and game being played texts

        :return: List containing username and game WebElements
        """
        return self.wait_and_get_elements(locs.USERNAME_AND_GAME)

    # def username_exists(self, username) -> str:
    #     return self.get_element_text(locs.)

    def for_mature_audiences(self, timeout: float = 1) -> bool:
        """
        When the stream is covered with mature audiences, check if `start watching` button is visible

        :param timeout: How long to wait
        :returns: True if button is displayed, false otherwise
        """
        try:
            return self.wait_and_get_element(locs.START_WATCHING_BTN, timeout).is_displayed()
        except TimeoutException:
            return False

    def click_start_watching(self):
        """
        Click `Start Watching` button
        """
        self.click_element(locs.START_WATCHING_BTN)

