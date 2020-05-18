# GoodReadsReviewsScraper

A script that scrapes the top 1500 reviews of all books in a given list of GoodReads URLs, written in Python using Selenium and BeautifulSoup.

## Introduction

This is a Python/Selenium-based web crawler that (relatively quickly) scrapes up to 1500 full-text reviews for any given book (or list of books) on [GoodReads](https://www.goodreads.com/). These data provide a rich source for textual analysis.

## How To Run

After cloning the repo and creating a virtual environments with the packages listed in `requirements.txt`, edit the `scrape-settings.py` file with your desired settings:

- `chrome_path`: the local path of your ChromeDriver ([download here](https://sites.google.com/a/chromium.org/chromedriver/)) 
- `book_urls`: a list of GoodReads book URLs to be scraped
- `output_dir`: the local directory in which to write the output file
- `output_name`: the name to assign to the output file

After this, simply run the `scraper_main.py` script. The script will launch a Chrome browser that will automatically cycle through the books and their review pages.

## Data Schema

| Column | Description |
| --- | --- |
| book_id | The book's unique GoodReads ID |
| book_title | The book's title |
| book_author | The book's author |
| reviewer_id | The reviewer's unique GoodReads ID |
| rating | Star rating of review |
| review | Full text of review |
| date | Date of reivew (YYYY-MM-DD) |

## Limitations / Future Work

GoodReads does not make the full set of reviews for any given book available for public viewing. The site will show only up to 10 pages of reviews per book, which, at 30 reviews per page, comes to 300 reviews. This number can be increased by filtering by the reviews' star rating. You can then view 300 5-star reviews, 300 4-star reviews, and so on, for a total of 1500 reviews. Some more reviews could be found by filtering by "Oldest" and "Newest", but this would result in many duplicate reviews, so I have chosen to omit these filters here.

Note that **the script takes between 4 and 5 minutes to scrape 1500 reviews for a single book.** The script can be sped up by decreasing the `zzz` variable in `scraper_settings.py`; however, doing so increasing the likelihood that the script will scrape the same reviews over again, as the next page of reviews has not had. In my own testing, setting `zzz` equal to 4 avoids this happening. In any case, the output file should be checked for duplicate rows during data cleaning.

## Troubleshooting

A consistent hiccup in the script is getting the browser to successfully find and click on the "More filters" link, so as to filter the reviews by star rating. The script will not break if it does not find this link, but it will instead simply loop through the top reviews of the book five times in a row. Further improvements to this step can be made by adding additional valid XPaths to the `filters_xpaths` list variable in `scraper_utils.py`.

## Contributing

This is the first automated script I've written, so fixes and improvements are more than welcome!