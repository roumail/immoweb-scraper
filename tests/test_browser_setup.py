import pytest
from selenium.common.exceptions import NoSuchElementException

from immoweb_scraper.setup import browser_setup


def test_browser_setup_google_search():
    browser = browser_setup()
    try:
        # Navigate to Google
        browser.get("https://www.google.com")

        # Check if the Google search box can be located
        search_box = browser.find_element_by_name("q")
        assert search_box is not None

        # Perform a search to further test
        search_box.send_keys("Hello, World!")
        search_box.submit()

        # Check if search results are displayed
        results = browser.find_elements_by_css_selector("h3")
        assert len(results) > 0

    except NoSuchElementException as e:
        pytest.fail(f"Test failed due to element not found: {e}")
    finally:
        # Close the browser after the test
        browser.quit()
