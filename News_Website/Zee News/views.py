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
from selenium.common.exceptions import NoSuchElementException  # Import the exception

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
        website = "https://zeenews.india.com/bengali/"

        # Open the website
        driver.get(website)

        # Wait for the website to load
        time.sleep(5)
        
        class_names = ["lead-head", "nation-lead-txt", "mini-con", "field-content", "oneblock"]
        
        scraped_data = []
        
        for class_name in class_names:
            # Find all elements with the current class
            elements = driver.find_elements(By.CLASS_NAME, class_name)
            
            # Scrape data from each element
            for element in elements:
                try:
                    # Get the element link
                    element_link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                except NoSuchElementException:
                    continue  # Skip to the next iteration if the hyperlink is not found
                
                # Open a new tab with the element link
                driver.execute_script(f"window.open('{element_link}', '_blank');")
                
                # Switch to the newly opened tab
                driver.switch_to.window(driver.window_handles[-1])

                # Wait for the page to load
                time.sleep(5)

                # Get the HTML of the page
                html = driver.page_source

                # Create a BeautifulSoup object
                soup = BeautifulSoup(html, "html.parser")

                # Find the headline element
                headline_element = soup.find(class_="article-heading margin-bt10px")
                headline = headline_element.text if headline_element else "Headline not found"

                # Find the elements with class "margin-bt10px"
                sort_dec_elements = soup.find_all(class_="margin-bt10px")

                # Find the <p> tags
                p_tags = soup.find_all("p")

                # Find the image element with class "media"
                image_element = soup.find(class_="field-item even")

                # Get the image source and the image caption
                image_src = image_element.find("img")["src"]if image_element else ""

                # Store the scraped data
                scraped_data.append({
                    "Class": class_name,
                    "Headline": headline,
                    "SortDec": "\n".join([element.text for element in sort_dec_elements]),
                    "News": "\n".join([p_tag.text for p_tag in p_tags]),
                    "Image Source": image_src,
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
