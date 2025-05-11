from playwright.async_api import async_playwright, Page
from typing import List, Dict
from argparse import Namespace
import time

async def fill_page(page: Page, person: Dict) -> None:
    #divs[] = save all divs which contain label
    divs = await page.locator("form div:has(label)").all()
    for div in divs:
        #.first for selecting first labels/inputs if div has multiple
        label = div.locator("label").first
        input = div.locator("input").first

        #skip divs with no label nor input
        if await label.count() == 0 or await input.count() == 0:
            continue

        #.text_content() returns what user sees, e.g. "First Name"
        label_text = (await label.text_content())

        if label_text in person:
            await input.fill(str(person[label_text]))


async def run_automation(data: List[Dict[str, str]], args: Namespace) -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=args.headless or args.fast)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.rpachallenge.com/")
        await page.get_by_role("button", name="Start").click()

        start = time.time()

        for person in data:
            #Remove any extra spaces in Excel headers
            person_cleaned = {key.strip(): value for key, value in person.items()}
            await fill_page(page, person_cleaned)
            await page.get_by_role("button", name="Submit").click()

        end = time.time()

        if args.fast:
            print(f"\nPython timer: {int((end - start)*1000)} ms\n")
        
        result_text = await page.locator("div.message2").text_content()
        print(result_text)

        await context.close()
        await browser.close()
