import pytest
from playwright.sync_api import sync_playwright
import random

@pytest.fixture(scope="session")
def test_env():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        ctx = browser.new_context()
        yield ctx
        ctx.close()
        browser.close()

def test_add_book(test_env):
    pg = test_env.new_page()
    pg.goto("http://localhost:5001/add_book")
    pg.fill('input[name="title"]', "Test Autobiography")
    pg.fill('input[name="author"]', "Author That Totally Exists")
    isbn = str(random.randint(10**12, 10**13 - 1))
    pg.fill('input[name=isbn]', isbn)
    pg.fill('input[name="total_copies"]', "5")
    pg.click('button[type="submit"]')
    txt = pg.text_content("body").lower()
    assert "successfully" in txt
    pg.wait_for_selector("table")
    assert pg.locator("td", has_text="Test Autobiography").count() > 0

def test_borrow_book(test_env):
    t = test_env.new_page()
    t.goto("http://localhost:5001")
    row = t.locator("tbody tr", has_text="Test Autobiography").nth(0)
    row.locator('input[name="patron_id"]').fill("555123")
    row.locator("text=Borrow").click()
    t.wait_for_selector("text=Successfully borrowed")
    msg = t.text_content("body").lower()
    assert "successfully borrowed" in msg

