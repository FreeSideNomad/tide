"""
End-to-end tests for the Tide DBT AI Assistant application using Playwright.
Replaces Selenium-based tests with more reliable browser automation.
"""

import pytest
import asyncio
import requests
import time
from playwright.async_api import async_playwright, Page


class TestTideAppE2E:
    """End-to-end tests for the Tide DBT AI Assistant application."""

    @pytest.fixture(scope="class")
    def app_url(self):
        """Application URL for testing."""
        return "http://localhost:8080"

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

    @pytest.mark.asyncio
    async def test_app_loads_successfully(self, app_url):
        """Test that the application loads without errors."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
            page = await context.new_page()

            try:
                # Navigate to the app
                await page.goto(app_url, wait_until="networkidle")

                # Wait for page to be ready
                await page.wait_for_load_state("domcontentloaded")

                # Verify it's our Tide app
                title = await page.title()
                assert "Tide" in title or "Flet" in title

                # Verify Flet framework is loaded
                flet_loaded = await page.evaluate(
                    """
                    () => {
                        return typeof _flutter !== 'undefined' ||
                               document.querySelector('flutter-view') !== null;
                    }
                """
                )

                assert flet_loaded, "Flet/Flutter framework not loaded"

                # Take screenshot for debugging
                await page.screenshot(path="tests/e2e/screenshots/app-loaded.png")

            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_authentication_page_structure(self, app_url):
        """Test that the authentication page has the expected structure."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(app_url, wait_until="networkidle")
                await page.wait_for_load_state("domcontentloaded")

                # Wait for Flet to initialize
                await page.wait_for_timeout(3000)

                # Enable Flet accessibility features
                await self.enable_flet_accessibility(page)

                # Look for authentication page elements
                # This is more flexible than strict element matching

                # Check if we can find authentication-related elements
                # Flet apps may render differently, so we check for various indicators
                has_auth_content = await page.evaluate(
                    """
                    () => {
                        // Look for any text that suggests this is an auth page
                        const bodyText = document.body.innerText.toLowerCase();
                        const authKeywords = ['sign', 'auth', 'login', 'google', 'tide', 'dbt'];
                        return authKeywords.some(keyword => bodyText.includes(keyword));
                    }
                """
                )

                # Also check for interactive elements that might be buttons
                interactive_elements = await page.locator(
                    "[role='button'], button, [onclick], [onmousedown]"
                ).count()

                # Take screenshot for visual verification
                await page.screenshot(path="tests/e2e/screenshots/auth-page.png")

                # Verify we have some authentication content or interactive elements
                assert (
                    has_auth_content or interactive_elements > 0
                ), "Could not find authentication page content or interactive elements"

            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_flet_rendering_and_framework(self, app_url):
        """Test Flet framework detection and rendering mode."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(app_url, wait_until="networkidle")
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(3000)

                # Get comprehensive rendering information
                render_info = await page.evaluate(
                    """
                    () => {
                        return {
                            hasFlutterView: !!document.querySelector('flutter-view'),
                            hasGlassPane: !!document.querySelector('flt-glass-pane'),
                            renderer: document.body.getAttribute('flt-renderer'),
                            flutterAvailable: typeof _flutter !== 'undefined',
                            canvasCount: document.querySelectorAll('canvas').length,
                            semanticsPlaceholder: !!document.querySelector('flt-semantics-placeholder'),
                            title: document.title,
                            embedding: document.body.getAttribute('flt-embedding'),
                            buildMode: document.body.getAttribute('flt-build-mode')
                        };
                    }
                """
                )

                print(f"Render info: {render_info}")

                # Verify this is a proper Flet app
                assert render_info["hasFlutterView"], "No flutter-view found"
                assert render_info["hasGlassPane"], "No glass pane found"
                assert render_info["flutterAvailable"], "Flutter not available"
                assert render_info[
                    "semanticsPlaceholder"
                ], "No semantics placeholder for accessibility"

                # Take screenshot showing the rendered app
                await page.screenshot(path="tests/e2e/screenshots/flet-framework.png")

            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_accessibility_features(self, app_url):
        """Test that accessibility features work properly."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(app_url, wait_until="networkidle")
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(3000)

                # Check that accessibility placeholder exists
                placeholder_exists = await page.evaluate(
                    """
                    () => {
                        const placeholder = document.querySelector('flt-semantics-placeholder');
                        return placeholder !== null;
                    }
                """
                )

                assert placeholder_exists, "Flet accessibility placeholder not found"

                # Try to activate accessibility features
                accessibility_activated = await self.enable_flet_accessibility(page)

                # Check if semantic elements became available
                semantic_elements_count = await page.locator(
                    "flt-semantics *, flt-semantics-host *"
                ).count()

                # Take screenshot showing accessibility state
                await page.screenshot(path="tests/e2e/screenshots/accessibility.png")

                print(f"Accessibility activated: {accessibility_activated}")
                print(f"Semantic elements found: {semantic_elements_count}")

            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_no_javascript_errors(self, app_url):
        """Test that there are no JavaScript errors on page load."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # Collect console messages
            console_messages = []

            def handle_console(msg):
                console_messages.append(msg)

            page.on("console", handle_console)

            try:
                await page.goto(app_url, wait_until="networkidle")
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(5000)  # Wait for full initialization

                # Filter for actual errors (not warnings or info)
                errors = [msg for msg in console_messages if msg.type == "error"]

                # Print all console messages for debugging
                for msg in console_messages:
                    print(f"Console {msg.type}: {msg.text}")

                # Assert no severe errors
                assert (
                    len(errors) == 0
                ), f"JavaScript errors found: {[msg.text for msg in errors]}"

            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_responsive_design(self, app_url):
        """Test responsive design across different screen sizes."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Test different viewport sizes
            viewports = [
                {"width": 375, "height": 667, "name": "mobile"},  # iPhone SE
                {"width": 768, "height": 1024, "name": "tablet"},  # iPad
                {"width": 1920, "height": 1080, "name": "desktop"},  # Desktop
            ]

            for viewport in viewports:
                context = await browser.new_context(
                    viewport={"width": viewport["width"], "height": viewport["height"]}
                )
                page = await context.new_page()

                try:
                    await page.goto(app_url, wait_until="networkidle")
                    await page.wait_for_load_state("domcontentloaded")
                    await page.wait_for_timeout(3000)

                    # Take screenshot for each viewport
                    await page.screenshot(
                        path=f"tests/e2e/screenshots/responsive-{viewport['name']}.png"
                    )

                    # Verify content is present and accessible
                    body_content = await page.locator("body").text_content()
                    assert (
                        body_content is not None and len(body_content.strip()) > 0
                    ), f"No content found on {viewport['name']} viewport"

                finally:
                    await context.close()

            await browser.close()

    async def enable_flet_accessibility(self, page: Page) -> bool:
        """Enable Flet accessibility features to expose DOM elements."""
        print("🔧 Enabling Flet accessibility features...")

        # Try to activate accessibility through the semantics placeholder
        accessibility_result = await page.evaluate(
            """
            () => {
                const placeholder = document.querySelector('flt-semantics-placeholder');
                if (placeholder) {
                    // Click the placeholder to activate accessibility
                    placeholder.click();
                    placeholder.focus();

                    // Try pressing Enter key
                    const enterEvent = new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        bubbles: true
                    });
                    placeholder.dispatchEvent(enterEvent);

                    return 'Accessibility activation attempted';
                }
                return 'No accessibility placeholder found';
            }
        """
        )

        print(f"   Accessibility result: {accessibility_result}")

        # Wait for accessibility features to activate
        await page.wait_for_timeout(3000)

        # Check for semantic elements
        semantic_elements_count = await page.locator(
            "flt-semantics *, flt-semantics-host *"
        ).count()
        print(f"   Semantic elements available: {semantic_elements_count}")

        # Also check for aria elements
        aria_elements_count = await page.locator(
            "[aria-label], [role], [aria-describedby]"
        ).count()
        print(f"   Aria elements available: {aria_elements_count}")

        return semantic_elements_count > 0 or aria_elements_count > 0


class TestPerformanceAndMetrics:
    """Test performance and loading metrics."""

    @pytest.mark.asyncio
    async def test_page_load_performance(self, app_url="http://localhost:8080"):
        """Test page load performance metrics."""
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

                print(f"Page load time: {load_time:.2f} seconds")

                # Assert reasonable load time (10 seconds is generous for development)
                assert (
                    load_time < 10
                ), f"Page took too long to load: {load_time:.2f} seconds"

                # Get performance metrics
                metrics = await page.evaluate(
                    """
                    () => {
                        const perf = performance.getEntriesByType('navigation')[0];
                        return {
                            domContentLoaded: perf.domContentLoadedEventEnd - perf.domContentLoadedEventStart,
                            loadComplete: perf.loadEventEnd - perf.loadEventStart,
                            firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
                        };
                    }
                """
                )

                print(f"Performance metrics: {metrics}")

            finally:
                await browser.close()


# Utility fixture to ensure screenshot directory exists
@pytest.fixture(autouse=True)
def ensure_screenshot_dir():
    """Ensure screenshot directory exists."""
    import os

    screenshot_dir = "tests/e2e/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
