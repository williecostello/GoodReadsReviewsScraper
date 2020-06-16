import os
import pandas as pd
from selenium import webdriver

from scraper_utils import go_to_page, scrape_book_info, select_stars, \
    list_reviews, scrape_review
from scraper_settings import chrome_path, book_urls, output_dir


# Check that output directory exists; if not, create it
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)


# Initialize browser
browser = webdriver.Chrome(chrome_path)


# Loop through each book in list
for book_url in book_urls:

    # Initialize dataframe to store review data
    reviews_df = pd.DataFrame()

    # Go to book's URL
    go_to_page(browser, book_url)

    # Scrape the book's essential info
    book_id, book_title, book_author = scrape_book_info(browser, book_url)

    # Loop through 5-star to 1-star review filters
    for i in range(1, 6):

        # Select the review filter
        select_stars(browser, i)

        # Loop through the first 10 pages of reviews
        for j in range(10):

            # Create list of all reviews on current page
            reviews = list_reviews(browser)

            # Loop through each review
            for review in reviews:

                # Scrape the review's essential info
                reviewer_id, rating, text, date = scrape_review(review)

                # Create dataframe of review data
                review_df = pd.Series([book_id, book_title, book_author,
                                       reviewer_id, rating, text, date])

                # Append review data to master dataframe
                reviews_df = reviews_df.append(review_df, ignore_index = True)

            # Check to see if at the last page of reviews
            # If not, move on to the next page of reviews
            try:
                browser.find_element_by_class_name('next_page')
            except:
                break
            next_page = browser.find_element_by_class_name('next_page')
            if next_page.get_attribute('class') != 'next_page disabled':
                next_page.click()
            else:
                break

    # Rename columns of reviews dataframe
    reviews_df.columns = ['book_id', 'book_title', 'book_author',
                          'reviewer_id', 'rating', 'review', 'date']

    # Create unique file name from book ID and title
    book_name = book_title.lower().replace(':', '').replace('//', '-').replace(' ', '_')
    file_name = f"{book_id}_{book_name}"

    # Write reviews dataframe to csv
    reviews_df.to_csv(f'{output_dir}{file_name}.csv', index=False)