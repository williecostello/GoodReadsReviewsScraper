from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import re
import time

from scraper_settings import zzz


# Function to scrape a book's essential info (ID, title, author)
def scrape_book_info(browser, book_url):

    # Download & Soupify webpage
    r = browser.page_source
    soup = BeautifulSoup(r, features = 'html.parser')
    
    # Find book ID, title, and author
    book_id = book_url.split('/')[-1].split('-')[0]
    book_title = soup.find(id = 'bookTitle').text.replace('\n', '').strip()
    book_author = soup.find('a', class_='authorName').text
    
    return book_id, book_title, book_author


# Function to scrape a review's essential info (reviewer ID, text, rating, date)
def scrape_review(review):

    # Find reviewer's URL
    reviewer_url = review.find('a', class_='user').get('href')
    # Isolate reviewer ID, between the final '/' and following '-' in the URL
    reviewer_id = reviewer_url.split('/')[-1]
    reviewer_id = reviewer_id.split('-')[0]

    # Create dictionary to translate rating description to number
    rating_dict = {'did not like it': 1, 'it was ok': 2, 'liked it': 3,
                   'really liked it': 4, 'it was amazing': 5}
    # Find review rating & convert rating description to number
    try:
        rating_text = review.find('span', class_='staticStars notranslate').text
        rating = rating_dict[rating_text]
    # If no rating given, encode as 'NaN'
    except:
        rating = np.nan
    
    # Find review text
    text_block = review.find('div', class_='reviewText stacked')
    try:
        text = text_block.find('span', style='display:none').get_text(' ', strip=True)
    except:
        text = text_block.get_text(' ', strip=True)

    # Remove spoiler tags from review text
    text = re.sub(r'\(view spoiler\) \[', '', text)
    text = re.sub(r'\(hide spoiler\) \] ', '', text)

    # Find review date
    date_text = review.find('a', class_='reviewDate createdAt right').text
    # Convert date to datetime
    date = datetime.strptime(date_text, '%b %d, %Y')

    return reviewer_id, rating, text, date


# Function to load a book's URL
def go_to_page(browser, book_url):
    browser.get(book_url)
    time.sleep(zzz)
    close_pop_up(browser)


# Function to close pesky pop-up message, if present
def close_pop_up(browser):
    pop_up_xpath = '/html/body/div[3]/div/div/div[1]/button/img'
    try:
        browser.find_element_by_xpath(pop_up_xpath).click()
        time.sleep(zzz)
    except:
        pass


# Function to list all reviews on a given page
def list_reviews(browser):

    # Wait to allow page of reviews to load
    time.sleep(zzz)

    # Download & Soupify webpage
    r = browser.page_source
    soup = BeautifulSoup(r, features = 'html.parser')

    # Create list of all reviews on webpage (there should be 30)
    reviews = soup.find_all('div', class_='friendReviews elementListBrown')
    
    return reviews


# Function to select n-stars review filter
def select_stars(browser, n):
    
    # Go to top of page
    browser.execute_script('window.scrollTo(0, 0);')

    # Scroll down a while, so that "More filters" is visible
    # (This is necessary sometimes for the code to work)
    browser.execute_script('window.scrollBy(0, 1200);')

    # Refresh browser (also necessary for code to work)
    browser.refresh()
    time.sleep(zzz)

    # Close pesky pop-up message, if present
    close_pop_up(browser)
    
    # Click on "More filters"
    # (Try multiple XPaths, as different pages have different XPaths)
    filters_xpaths = ['/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[3]/div[4]/div[2]/div/div[1]/div[2]/div[6]/a/span',
                      '/html/body/div[2]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[2]/div/div[1]/div[2]/div[6]/a/span',
                      '/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[3]/div[5]/div[2]/div/div[1]/div[2]/div[6]/a/span',
                      '/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/div[3]/div[5]/div[2]/div/div[1]/div[2]/div[6]/a/span',]
    for filters_xpath in filters_xpaths:
        try:
            browser.find_element_by_xpath(filters_xpath).click()
        except:
            pass
    time.sleep(zzz)

    # Click on "n-stars"
    stars_class = 'actionLinkLite.loadingLink'
    try:
        browser.find_elements_by_class_name(stars_class)[n].click()
    except:
        pass
    time.sleep(zzz)