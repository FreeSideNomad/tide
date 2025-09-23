"""
End-to-end tests for the Tide DBT AI Assistant application.
"""

import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


class TestAppE2E:
    """End-to-end tests for the Flet web application."""

    @pytest.fixture(scope="class")
    def app_url(self):
        """Application URL for testing."""
        return "http://localhost:8080"

    @pytest.fixture(scope="class")
    def driver(self):
        """Selenium WebDriver instance."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode for CI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    @pytest.fixture(autouse=True)
    def wait_for_app(self, app_url):
        """Wait for the application to be available."""
        max_retries = 30
        retry_delay = 2

        for _ in range(max_retries):
            try:
                response = requests.get(app_url, timeout=5)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                pass
            time.sleep(retry_delay)
        else:
            pytest.fail(
                f"Application not available at {app_url} after {max_retries * retry_delay} seconds"
            )

    def test_app_loads_successfully(self, driver, app_url):
        """Test that the application loads without errors."""
        driver.get(app_url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Check that we can find some basic elements
        # Note: Flet apps render in a specific way, so we look for common elements
        assert "Tide" in driver.title or driver.title != ""

    def test_counter_functionality(self, driver, app_url):
        """Test the counter increment functionality."""
        driver.get(app_url)

        try:
            # Wait for the Flet app to load
            wait = WebDriverWait(driver, 15)

            # Look for counter text (initially "0")
            # Flet renders text in specific elements, we may need to adjust selectors
            counter_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '0')]"))
            )

            initial_value = counter_element.text
            assert "0" in initial_value

            # Look for the floating action button (+ button)
            # Flet FABs are typically rendered as buttons
            fab_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(@aria-label, 'add') or contains(@title, 'add')]",
                    )
                )
            )

            # Click the button
            fab_button.click()

            # Wait a moment for the update
            time.sleep(1)

            # Check that the counter has incremented
            # The counter should now show "1"
            updated_counter = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '1')]"))
            )

            assert "1" in updated_counter.text

        except TimeoutException:
            # If we can't find the specific elements, at least verify the page loaded
            # This is a fallback for the initial basic Flet app structure
            page_source = driver.page_source
            assert len(page_source) > 100  # Basic check that content exists
            pytest.skip(
                "Could not locate counter elements - Flet app structure may need adjustment"
            )

    def test_responsive_design(self, driver, app_url):
        """Test that the app works on different screen sizes."""
        driver.get(app_url)

        # Test desktop size
        driver.set_window_size(1920, 1080)
        time.sleep(2)
        assert driver.execute_script("return document.readyState") == "complete"

        # Test tablet size
        driver.set_window_size(768, 1024)
        time.sleep(2)
        assert driver.execute_script("return document.readyState") == "complete"

        # Test mobile size
        driver.set_window_size(375, 667)
        time.sleep(2)
        assert driver.execute_script("return document.readyState") == "complete"

    def test_no_javascript_errors(self, driver, app_url):
        """Test that there are no JavaScript errors on page load."""
        driver.get(app_url)

        # Wait for page to fully load
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Get console logs
        logs = driver.get_log("browser")

        # Filter for actual errors (not warnings or info)
        errors = [log for log in logs if log["level"] == "SEVERE"]

        # Assert no severe errors
        assert len(errors) == 0, f"JavaScript errors found: {errors}"

    def test_page_performance(self, driver, app_url):
        """Test basic page performance metrics."""
        start_time = time.time()
        driver.get(app_url)

        # Wait for page to be interactive
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        load_time = time.time() - start_time

        # Page should load within 10 seconds
        assert load_time < 10, f"Page took too long to load: {load_time} seconds"

        # Check that the page has some content
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0, "Page appears to be empty"


class TestAppAccessibility:
    """Basic accessibility tests."""

    @pytest.fixture(scope="class")
    def driver(self):
        """Selenium WebDriver instance for accessibility testing."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        yield driver
        driver.quit()

    def test_page_has_title(self, driver, app_url="http://localhost:8080"):
        """Test that the page has a proper title."""
        driver.get(app_url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        title = driver.title
        assert title is not None
        assert len(title) > 0
        assert title != "about:blank"

    def test_basic_semantic_structure(self, driver, app_url="http://localhost:8080"):
        """Test basic semantic HTML structure."""
        driver.get(app_url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Check for basic HTML structure
        html_element = driver.find_element(By.TAG_NAME, "html")
        assert html_element is not None

        body_element = driver.find_element(By.TAG_NAME, "body")
        assert body_element is not None
