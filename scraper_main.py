import argparse
import os
import pandas as pd
from selenium import webdriver

from scraper_utils import go_to_page, scrape_book_info, select_stars, \
    list_reviews, scrape_review
from scraper_settings import chrome_path, book_urls, output_dir


# Set script arguments
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--allstars', action='store_true', help='Scrape 300 reviews from each star rating; otherwise, scrape just the top 300 reviews')
args = parser.parse_args()

# Set whether to scrape just the top 300 reviews or 300 reviews from each rating
all_stars = args.allstars


# Check that output directory exists; if not, create it
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)


# Initialize browser
browser = webdriver.Chrome(chrome_path)


# Loop through each book in list
for book_url in book_urls:

    print(f'Starting scraping of {book_url}')

    # Initialize dataframe to store review data
    reviews_df = pd.DataFrame()

    # Go to book's URL
    go_to_page(browser, book_url)

    # Scrape the book's essential info
    book_id, book_title, book_author = scrape_book_info(browser, book_url)

    # Set whether to loop through review star filters
    num_loops = (5 if all_stars else 1)

    # Loop through 5-star to 1-star review filters, if selected
    for i in range(num_loops):

        # Select the review filter
        if all_stars:
            select_stars(browser, i+1)

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
            browser.execute_script('window.scrollTo(0, 0);')
            try:
                browser.find_element_by_class_name('next_page')
            except:
                print(f'Successfully scraped {j+1} pages of reviews')
                break
            next_page = browser.find_element_by_class_name('next_page')
            if next_page.get_attribute('class') != 'next_page disabled':
                next_page.click()
            else:
                print(f'Successfully scraped {j+1} pages of reviews')
                break

    # Rename columns of reviews dataframe
    reviews_df.columns = ['book_id', 'book_title', 'book_author',
                          'reviewer_id', 'rating', 'review', 'date']

    # Create unique file name from book ID and title
    book_name = book_title.lower().replace(':', '').replace('//', '-').replace(' ', '_')
    file_name = f"{book_id}_{book_name}"

    # Write reviews dataframe to csv
    reviews_df.to_csv(f'{output_dir}{file_name}.csv', index=False)

    print(f'Finished scraping of {book_title}!')