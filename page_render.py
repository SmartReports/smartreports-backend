import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import os, time

url = 'https://smartreports.it'
path = '../archive/example'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url=url, wait_until='networkidle')
        await page.evaluate('document.cookie = "cookies_accepted=true"')
        # await page.set_viewport_size({"width": 4320 , "height": 7680 }) 
        await page.set_viewport_size({"width": 1080 , "height": 2280 })
        # wait 1 sec
        time.sleep(1.5)
        await page.screenshot(path=path+'.png', full_page=True)
        await browser.close()

        image = Image.open(fp=path+'.png')
        image = image.convert('RGB')
        image.save(fp=path+'.pdf')
        # os.remove(path=path+'.png')
        

asyncio.run(main())