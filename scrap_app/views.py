import os
import time
import datetime
import threading
import openpyxl
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import FileResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from .models import HindustanTimesBangla, ZeeNews, TV9Bangla

# Other functions remain the same

excel_file_path = "scraped_data.xlsx"  # Global variable to store the Excel file path
iteration_count = 0  # Global variable to track the iteration count


def scrape_newspaper(request):
    global iteration_count
    
    if request.method == 'GET':
        return render(request, 'scrap_app/scrap_app.html')

    while True:  # Infinite loop
        data = []  # Data to store scraped information
        
        # Create a list to hold the threads
        threads = []

        # Create and start a thread for each scraping function
        thread1 = threading.Thread(target=scrape_thread, args=(hindustantimesbangla, data))
        thread2 = threading.Thread(target=scrape_thread, args=(zeenews, data))
        thread3 = threading.Thread(target=scrape_thread, args=(tv9bangla, data))
        # thread4 = threading.Thread(target=scrape_thread, args=(anandabazar, data))
        
        threads.extend([thread1, thread2, thread3])

        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        iteration_count += 1  # Increment the iteration count

        # Save the scraped data to an Excel file
        save_to_database(data)
        
        if iteration_count > 1:
            # Wait for 2 minutes before the next iteration
            time.sleep(120)

def save_to_database(data):
    for item in data:
        # Determine which model to use based on the news source
        if item["News Source"] == "hindustantimesbangla":
            news_model = HindustanTimesBangla
        elif item["News Source"] == "zeenews":
            news_model = ZeeNews
        elif item["News Source"] == "tv9bangla":
            news_model = TV9Bangla
        # Add more conditions for other news sources
        
        # Create a new instance of the news model and save it to the database
        news_instance = news_model(
            headline=item["Headline"],
            sort_description=item["SortDec"],
            news=item["News"],
            image_source=item["Image Source"],
            image_caption=item["Image Caption"]
        )
        news_instance.save()

def scrape_thread(scrape_function, data):
    scraped_data = scrape_function()
    data.extend(scraped_data)

def hindustantimesbangla():
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
        sort_dec_elements = soup.find_all(class_="highlights")

        # Find the <p> tags
        p_tags = soup.find_all("p")

        # Find the image element with class "media"
        image_element = soup.find(class_="storyExpend")

        # Get the image source and the image caption
        image_src = image_element.find("source")["srcset"] if image_element else ""
        image_caption = image_element.find("figcaption").text if (image_element and image_element.find("figcaption")) else ""

        # Adding "News Source" information correctly
        item = {
            "Headline": headline,
            "SortDec": "\n".join([element.text for element in sort_dec_elements]),
            "News": "\n".join([p_tag.text for p_tag in p_tags]),
            "Image Source": image_src,

            
            "Image Caption": image_caption
        }

        item["News Source"] = "hindustantimesbangla"
        scraped_data.append(item)

        # Close the current tab and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # Close the webdriver
    driver.quit()

    return scraped_data

def zeenews():
    # Set Chrome driver path
    driver_path = "D:\Drivers\chromedriver_win32\chromedriver.exe"

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

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
            # p_tags = soup.find_all("p")

            # Find the news content
            news_content = ""
            field_items = soup.find("div", class_="field field-name-body field-type-text-with-summary field-label-hidden")
            if field_items:
                div_field_items = field_items.find("div", class_="field-items")
                if div_field_items:
                    field_item_even = div_field_items.find("div", class_="field-item even")
                    if field_item_even:
                        p_tags = field_item_even.find_all("p")
                        news_content = " ".join([p_tag.text for p_tag in p_tags])

            # Find the image element with class "media"
            image_element = soup.find(class_="field-item even")

            # Initialize image_src and image_caption with default values
            image_src = ""
            image_caption = ""

            # Check if image_element is not None before accessing its attributes
            if image_element:
                img_tag = image_element.find("img")
                if img_tag and "src" in img_tag.attrs:
                    image_src = img_tag["src"]

                image_caption_element = image_element.find("figcaption")
                if image_caption_element:
                    image_caption = image_caption_element.text

            # Store the scraped data
            item = {
                "Class": class_name,
                "Headline": headline,
                "SortDec": "\n".join([element.text for element in sort_dec_elements]),
                "News": news_content,
                "Image Source": image_src,
                "Image Caption": image_caption,
            }
            item["News Source"] = "zeenews"
            scraped_data.append(item)

            # Close the current tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # Close the webdriver
    driver.quit()

    return scraped_data

def tv9bangla():
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
    website = "https://tv9bangla.com/"

    # Open the website
    driver.get(website)

    # Wait for the website to load
    time.sleep(5)
        
    class_names = ["imgThumb"]
        
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
                
            # Check if the link is the one to be skipped
            if "https://tv9bangla.com/videos" in element_link:
                continue  # Skip to the next iteration if the link is the one to be skipped
                
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
            headline_element = soup.find(class_="article-HD")
            headline = headline_element.text if headline_element else "Headline not found"

            # Find the elements with class "margin-bt10px"
            sort_dec_elements = soup.find_all(class_="summery")

            # Find the <p> tags
            p_tags = soup.find_all("p")

            # Find the image element with class "articleImg"
            image_element = soup.find(class_="articleImg")

            # Check if the image element contains a video
            video_element = image_element.find("video", class_="jw-video jw-reset")
            if video_element:
                # If a video element is found, skip scraping image and image caption
                image_src = "Video found, image skipped"
                image_caption = "Video caption"
            else:
                # If no video element is found, scrape image and image caption
                image_src_element = image_element.find("img")
                image_src = image_src_element["src"] if image_src_element else ""
                # Get the caption from class "smallSum"
                caption_element = soup.find(class_="smallSum")
                image_caption = caption_element.text if caption_element else ""

            # Store the scraped data
            item = {
                "Class": class_name,
                "Headline": headline,
                "SortDec": "\n".join([element.text for element in sort_dec_elements]),
                "News": "\n".join([p_tag.text for p_tag in p_tags]),
                "Image Source": image_src,
                "Image Caption": image_caption,
            }
            item["News Source"] = "tv9bangla"
            scraped_data.append(item)

            # Close the current tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # Close the webdriver
    driver.quit()

    return scraped_data

# def anandabazar():
#     # Set Chrome driver path
#     driver_path = "D:\Drivers\chromedriver_win32\chromedriver.exe"
    
#     # Set Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--window-size=1920x1080")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument(f"load-extension=path_to_ublock_extension_directory")
#     chrome_options.add_argument("--disable-notifications")
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
#     chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

#     # Create the WebDriver instance
#     driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

#     # Set the website and Chrome webdriver path
#     website = "https://www.anandabazar.com/"

#     # Open the website
#     driver.get(website)

#     # Wait for the website to load
#     time.sleep(5)

#     class_names = ["leadstorybox", "storylisting", "storylbox"]
#     scraped_data = []

#     for class_name in class_names:
#         # Find all elements with the current class
#         elements = driver.find_elements(By.CLASS_NAME, class_name)

#         # Scrape data from each element
#         for element in elements:
#             try:
#                 # Get the element link
#                 element_link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
#             except NoSuchElementException:
#                 continue  # Skip to the next iteration if the hyperlink is not found

#             # Open a new tab with the element link
#             driver.execute_script(f"window.open('{element_link}', '_blank');")

#             # Switch to the newly opened tab
#             driver.switch_to.window(driver.window_handles[-1])

#             # Wait for the page to load
#             time.sleep(5)

#             # Get the HTML of the page
#             html = driver.page_source

#             # Create a BeautifulSoup object
#             soup = BeautifulSoup(html, "html.parser")

#             # Find the headline element
#             headline_element = soup.find("h1", class_="mt-8")
#             headline = headline_element.text if headline_element else "Headline not found"

#             # Find the elements with class "margin-bt10px"
#             sort_dec_elements = soup.find_all("h2", class_="mt-8")

#             # Find the news content
#             p_tags = soup.find("div", class_="contentbox").find_all("p")
#             news_content = " ".join([p_tag.text for p_tag in p_tags])

#             # Find the image element with class "leadimgbox mt-24"
#             image_element = soup.find(class_="leadimgbox mt-24")

#             # Get the image source and the image caption
#             image_src = image_element.find("img")["src"] if image_element and image_element.find("img") else ""

#             # Find the image caption within the div with class "leadimgbox mt-24"
#             image_caption_element = soup.find("div", class_="leadimgbox mt-24")
#             image_caption = ""
#             if image_caption_element:
#                 p_tag = image_caption_element.find("p")
#                 if p_tag:
#                     spans = p_tag.find_all("span")
#                     image_caption = " ".join([span.text for span in spans if span.text])

#             # Store the scraped data
#             scraped_data.append({
#                 "Class": class_name,
#                 "Headline": headline,
#                 "SortDec": "\n".join([element.text for element in sort_dec_elements]),
#                 "News": news_content,
#                 "Image Source": image_src,
#                 "Image Caption": image_caption
#             })

#             # Close the current tab and switch back to the main tab
#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])

#     # Close the webdriver
#     driver.quit()

#     return scraped_data
