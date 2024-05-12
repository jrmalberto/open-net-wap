from selenium.webdriver.common.by import By

SEARCH_ICON = (By.XPATH, "//a[@aria-label='Search']")
SEARCH_INPUT = (By.XPATH, "//input[@type='search']")
SEARCH_SUGGESTIONS = (By.XPATH, "//a[contains(@class,'tw-link')]")
SEARCH_RESULTS_ARTICLES = (By.XPATH, "//article")
SEARCH_RESULTS_IMGS = (By.XPATH, "//img[@class='tw-image'][ancestor::article]")
USERNAME_AND_GAME = (By.XPATH, "//p[contains(title)][ancestor::div[@class='Layout-sc-1xcs6mc-0 kFwQBd']]")