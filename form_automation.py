#asyncronic process for more optimized performance when dealing with multiple forms
from playwright.async_api import async_playwright
from playwright.async_api import Page
import asyncio
import pandas as pd
from typing import List, Dict
import time
import argparse

#parse command line arguments
parser = argparse.ArgumentParser(description="Run RPA automation challenge")
parser.add_argument("--headless", action="store_true", help="Run in headless mode")
parser.add_argument("--fast", action="store_true")
args = parser.parse_args()

def excel_to_dict_list(filename: str) -> List[Dict]:
    dataframe = pd.read_excel(filename)
    #orient="records" to use column names as keys
    return dataframe.to_dict(orient="records")


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

        #typecast everything to string, because of phone number
        if label_text in person:
            await input.fill(str(person[label_text]))
        else:
            print(f"Label doesn't match: '{label_text}'")


async def main() -> None:
    async with async_playwright() as playwright:
        #args.headless stores boolean value, true/false
        browser = await playwright.chromium.launch(headless=args.headless or args.fast)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.rpachallenge.com/")
        await page.get_by_role("button", name="Start").click()

        data = excel_to_dict_list("challenge.xlsx")

        start = time.time()

        for person in data:
            #Remove any extra spaces in Excelf headers
            person_cleaned = {key.strip(): value for key, value in person.items()}
            
            await fill_page(page, person_cleaned)
            await page.get_by_role("button", name="Submit").click()
            #await page.wait_for_timeout(1000)
            #wait for next form to load for 500 milliseconds

        end = time.time()
        #print own timer in perfomance mode
        if args.fast:
            print(f"\nPython timer: {int((end - start)*1000)} ms")
        
        #save and print the result to user
        result_text = await page.locator("div.message2").text_content()
        print(result_text)

        #close tab
        await context.close()
        #clear cookies etc.
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

