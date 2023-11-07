from playwright.sync_api import sync_playwright, Playwright

url = 'https://smartreports.it'
path = '../archive/example'


def run(playwright: Playwright):
    webkit = playwright.chromium
    browser = webkit.launch()
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 640, "height": 480})
    page.goto(url, wait_until="load")
    page.emulate_media(media='screen')

    page.pdf(path=path+'.pdf')
    page.screenshot(path=path+'.png', animations='disabled', full_page=True)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)