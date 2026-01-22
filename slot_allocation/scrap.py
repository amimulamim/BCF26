import pandas as pd
from playwright.sync_api import sync_playwright

URL = "https://bapsoj.org/contests/icpc-dhaka-onsite-2025/standings"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Run with browser visible for debugging
    page = browser.new_page()
    
    # Set a user agent to avoid being blocked
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(5000)  # Wait 5 seconds for content to load
        html = page.content()
        print("Page loaded successfully!")
    except Exception as e:
        print(f"Error loading page: {e}")
        html = page.content()
        print(f"Captured HTML length: {len(html)}")
    finally:
        browser.close()

tables = pd.read_html(html)
# pick the table that looks like standings
tables[0].to_csv("standings.csv", index=False)
