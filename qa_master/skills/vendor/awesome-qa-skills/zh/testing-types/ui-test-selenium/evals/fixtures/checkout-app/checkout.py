import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

for user in ("A", "B"):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(f"http://127.0.0.1:4173/?user={user}&order={user}-1&mode={os.environ.get('MODE', 'good')}")
        # Re-find on each poll so rerenders do not retain a stale element.
        driver.find_element(By.CSS_SELECTOR, '[data-testid="pay"]').click()
        WebDriverWait(driver, 3).until(lambda d: d.find_element(By.CSS_SELECTOR, '[data-testid="state"]').text == "paid")
        record = driver.execute_script("return window.fixtureRecord()")
        assert record == dict(principal=user, orderId=f"{user}-1", amount=20, state="paid")
    except Exception:
        driver.save_screenshot(f"failure-{user}.png")
        raise
    finally:
        driver.quit()
