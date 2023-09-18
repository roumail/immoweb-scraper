import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from immoweb_scraper.setup import browser_setup


def test_browser_setup_google_search():
    browser: WebDriver = browser_setup()
    try:
        # Navigate to Google
        browser.get("https://www.google.com")

        # Check if the Google search box can be located
        search_box = browser.find_element(By.NAME, "q")
        assert search_box is not None

        # Perform a search to further test
        search_term = "Hello, World!"
        search_box.send_keys(search_term)
        search_box.submit()

        # Wait for the results page to load and verify the title
        WebDriverWait(browser, 10).until(EC.title_contains(search_term))
        assert search_term in browser.title
    except NoSuchElementException as e:
        pytest.fail(f"Test failed due to element not found: {e}")
    except TimeoutException:
        pytest.fail("Test failed")
    finally:
        # Close the browser after the test
        browser.quit()
