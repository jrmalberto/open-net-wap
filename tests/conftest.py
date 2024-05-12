import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def init_driver():

    mobile_emulation = {"deviceName": "iPhone 14 Pro Max"}
    chrome_options = webdriver.ChromeOptions()
    cs = Service(ChromeDriverManager().install())
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(service=cs, options=chrome_options)  # sometimes you have to insert your execution path
    # driver.get('https://m.twitch.tv')
    yield driver
    driver.quit()