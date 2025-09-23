"""
End-to-end tests using Playwright for better browser automation.
"""

import pytest
import asyncio
from playwright.async_api import async_playwright


class TestPlaywrightE2E:
    """E2E tests using Playwright for more reliable browser automation."""

    @pytest.fixture(scope="class")
    def app_url(self):
        """Application URL for testing."""
        return "http://localhost:8080"

    @pytest.mark.asyncio
    async def test_app_loads_with_playwright(self, app_url):
        """Test that the application loads successfully using Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
            page = await context.new_page()

            try:
                # Navigate to the app
                await page.goto(app_url, wait_until="networkidle")

                # Wait for the page to be loaded
                await page.wait_for_load_state("domcontentloaded")

                # Check that the page title is not empty
                title = await page.title()
                assert title is not None
                assert len(title) > 0

                # Take a screenshot for debugging if needed
                await page.screenshot(path="tests/e2e/screenshots/app-loaded.png")

            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_counter_interaction_playwright(self, app_url):
        """Test counter functionality using Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(app_url, wait_until="networkidle")

                # Wait for the Flet app to initialize
                await page.wait_for_timeout(2000)

                # Look for text containing "0" (initial counter value)
                counter_locator = page.locator("text=0").first
                await counter_locator.wait_for(state="visible", timeout=10000)

                # Look for a button that might be the FAB
                # Flet creates buttons with specific attributes
                fab_locator = page.locator("button").first
                await fab_locator.wait_for(state="visible", timeout=10000)

                # Click the button
                await fab_locator.click()

                # Wait for the update
                await page.wait_for_timeout(1000)

                # Look for text containing "1" (incremented counter)
                incremented_counter = page.locator("text=1").first
                await incremented_counter.wait_for(state="visible", timeout=5000)

                # Take screenshot of the result
                await page.screenshot(
                    path="tests/e2e/screenshots/counter-incremented.png"
                )

            except Exception as e:
                # Take screenshot on failure for debugging
                await page.screenshot(path="tests/e2e/screenshots/test-failure.png")
                print(f"Test failed with error: {e}")
                print(f"Page content: {await page.content()}")
                raise

            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_mobile_responsive_playwright(self, app_url):
        """Test mobile responsiveness using Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Test different device configurations
            devices = [
                {"width": 375, "height": 667, "name": "mobile"},  # iPhone SE
                {"width": 768, "height": 1024, "name": "tablet"},  # iPad
                {"width": 1920, "height": 1080, "name": "desktop"},  # Desktop
            ]

            for device in devices:
                context = await browser.new_context(
                    viewport={"width": device["width"], "height": device["height"]}
                )
                page = await context.new_page()

                try:
                    await page.goto(app_url, wait_until="networkidle")
                    await page.wait_for_load_state("domcontentloaded")

                    # Take screenshot for each device size
                    await page.screenshot(
                        path=f"tests/e2e/screenshots/responsive-{device['name']}.png"
                    )

                    # Basic check that content exists
                    body_content = await page.locator("body").text_content()
                    assert len(body_content) > 0

                finally:
                    await context.close()

            await browser.close()

    @pytest.mark.asyncio
    async def test_performance_metrics_playwright(self, app_url):
        """Test performance metrics using Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Start measuring
                start_time = asyncio.get_event_loop().time()

                await page.goto(app_url, wait_until="networkidle")
                await page.wait_for_load_state("domcontentloaded")

                end_time = asyncio.get_event_loop().time()
                load_time = end_time - start_time

                # Assert reasonable load time
                assert (
                    load_time < 10
                ), f"Page took too long to load: {load_time} seconds"

                # Check for console errors
                console_messages = []

                def handle_console(msg):
                    console_messages.append(msg)

                page.on("console", handle_console)

                # Refresh to capture console messages
                await page.reload(wait_until="networkidle")
                await page.wait_for_timeout(2000)

                # Check for severe errors
                errors = [msg for msg in console_messages if msg.type == "error"]
                assert (
                    len(errors) == 0
                ), f"Console errors found: {[msg.text for msg in errors]}"

            finally:
                await browser.close()


# Utility to ensure screenshot directory exists
@pytest.fixture(autouse=True)
def ensure_screenshot_dir():
    """Ensure screenshot directory exists."""
    import os

    screenshot_dir = "tests/e2e/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
