# News Scraping Project

## Table of Contents
1. [Version History](#version-history)
2. [License](#license)

## Version History

### v1.0.1
- Initial release: Scraping from Hindustan Times and saving data to `scraped_data.xlsx`.

### v1.0.1.1
- Update: Added scraping from Hindustan Times Bangla and saved data to `scraped_data.xlsx`.

### v1.0.1.2
- Update: Added scraping from Zee News and saved data to `scraped_data.xlsx`.

### v1.0.1.3
- Update: Added scraping from TV9 Bangla and saved data to `scraped_data.xlsx`.

### v1.0.1.4
- Update: Added scraping from Ananda Bazar and saved data to `scraped_data.xlsx`.

### v2.0.1
- Release: Scraping from four news sites based on request value and saving data to `scraped_data.xlsx`.

### v2.0.1.1
- Update: Appended new scrape data to an existing DataFrame and saved it to `scraped_data.xlsx`.

### v3.0.1
- Release: Introduced threading to run all news scrapers simultaneously with a 2-minute interval before the next iteration.

### v3.0.1.1
- Update: Created a new folder with the current date if it doesn't exist and saved `scraped_data.xlsx` with the current time and date.

### v4.0.1
- Release: Created `scrapdata_db` database in MySQL with three tables for different newspapers. Updated `models.py` and `settings.py`.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.
