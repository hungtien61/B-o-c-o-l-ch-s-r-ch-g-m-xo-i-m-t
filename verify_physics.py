from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 3000})

        print("Navigating to app...")
        page.goto("http://localhost:8000")

        print("Waiting for intro...")
        page.wait_for_selector("main.opacity-100", timeout=10000)

        print("Scrolling...")
        page.get_by_text("Vật Lý Chiến Trường").scroll_into_view_if_needed()
        time.sleep(1)

        print("Forcing low tide...")
        slider = page.locator("input[type=range]")
        # React requires 'input' event, and sometimes the prototype setter
        slider.evaluate("""el => {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            nativeInputValueSetter.call(el, 10);
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }""")
        time.sleep(2)

        print("Checking Ship Transform:")
        ship = page.locator(".ship-container")
        style = ship.get_attribute("style")
        print(f"Ship Style: {style}")

        # Check if style contains STRANDED rotation (approx -15deg)
        if "-15deg" in str(style):
             print("SUCCESS: Ship is tilted correctly (-15deg).")
        else:
             print("ERROR: Ship is NOT tilted correctly.")

        print("Checking for label...")
        ship_html = ship.inner_html()
        if "STRANDED" in ship_html:
             print("SUCCESS: Label found in ship container.")
        else:
             print("ERROR: Label NOT found in ship container.")
             print(f"Container HTML: {ship_html}")

        print("Taking screenshot...")
        page.screenshot(path="physics_low_tide.png")

        browser.close()

if __name__ == "__main__":
    run()
