import time

from pages.homepage import HomePage


class TestSearch:

    def test_search(self, init_driver):
        homepage = HomePage(init_driver)
        homepage.go_to_link(homepage.url)
        homepage.click_search_btn()
        homepage.input_search("StarCraft II")
        time.sleep(1)  # Give a second for results to show
        suggestions = homepage.get_search_suggestions()

        # Make sure we are searching correctly
        assert suggestions[0].text == "StarCraft II"

        # Pick first suggestion result and click to search
        homepage.select_search_suggestion(0)
        results = homepage.get_search_results()

        homepage.js_scroll_into_view(results[1])
        homepage.js_scroll_into_view(results[-1])

        # Elements texts into a list for assertion against streamer page ['Title', 'Username', 'Game', 'LIVE', 'No of viewers']
        texts = results[-1].text.splitlines()

        sp = homepage.select_search_result(results[-1])
        time.sleep(2)  # Give a couple secs for dynamic content to load

        # Deal with popup for mature audiences only
        if sp.for_mature_audiences():
            sp.click_start_watching()

        # Verify we landed on correct page via username and game
        assert (sp.get_user_and_game()[0].text.casefold() in texts[1].casefold()
                and texts[2].casefold() in sp.get_user_and_game()[1].text.casefold())

        # Take screenshot
        time.sleep(4)  # Give a couple secs for dynamic content to load
        sp.driver.save_screenshot("end_result.png")
