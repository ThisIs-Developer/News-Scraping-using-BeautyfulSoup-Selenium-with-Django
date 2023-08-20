import os
import time
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_newspaper(request):
    if request.method == 'POST':
        # Set Chrome driver path
        driver_path = "D:\Drivers\chromedriver_win32\chromedriver.exe"

        # Set Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-extensions")

        # Create the WebDriver instance
        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

        # Set the website and Chrome webdriver path
        website = "https://bangla.hindustantimes.com/"

        # Open the website
        driver.get(website)

        # Wait for the website to load
        time.sleep(5)

        # Find all hdg3 elements
        hdg3_elements = driver.find_elements(By.CLASS_NAME, "headline")

        # Scrape data from each hdg3 element
        scraped_data = []
        for i in range(len(hdg3_elements)):
            # Find all hdg3 elements again to avoid StaleElementReferenceException
            hdg3_elements = driver.find_elements(By.CLASS_NAME, "headline")

            # Check if the index is within range
            if i >= len(hdg3_elements):
                break

            # Get the current hdg3 element
            hdg3_element = hdg3_elements[i]

            # Get the hdg3 link
            hdg3_link = hdg3_element.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Open a new tab with the hdg3 link
            driver.execute_script(f"window.open('{hdg3_link}', '_blank');")

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])

            # Wait for the hdg3 link page to load
            time.sleep(5)

            # Get the HTML of the hdg3 link page
            html = driver.page_source

            # Create a BeautifulSoup object
            soup = BeautifulSoup(html, "html.parser")

            # Find the headline element with class "hdg1"
            headline_element = soup.find(class_="headline")

            # Get the headline text
            headline = headline_element.text if headline_element else "Headline not found"

            # Find the elements with class "sortDec"
            # sort_dec_elements = soup.find_all(class_="contentSec")

            # Find the <p> tags
            p_tags = soup.find_all("p")

            # Find the image element with class "media"
            image_element = soup.find(class_="storyExpend")

            # Get the image source and the image caption
            image_src = image_element.find("source")["srcset"]if image_element else ""
            image_caption = image_element.find("figcaption").text if (image_element and image_element.find("figcaption")) else ""

            # Store the scraped data
            scraped_data.append({
                "Headline": headline,
                # "SortDec": "\n".join([element.text for element in sort_dec_elements]),
                "News": "\n".join([p_tag.text for p_tag in p_tags]),
                "Image Source": image_src,
                "Image Caption": image_caption
            })

            # Close the current tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Close the webdriver
        driver.quit()

        # Create a pandas DataFrame from the scraped data
        df = pd.DataFrame(scraped_data)

        # Save the DataFrame to an Excel file
        excel_file_path = "scraped_data.xlsx"
        df.to_excel(excel_file_path, index=False)

        # Return a response to download the Excel file
        with open(excel_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="scraped_data.xlsx"'

        # Remove the temporary Excel file
        # os.remove(excel_file_path)

        return response

    return render(request, 'scrap_app/scrap_app.html')
