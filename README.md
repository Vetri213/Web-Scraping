# Project Title: Academic Journal Editor Scraper

## Description:

This project involves a custom software program designed to automate the collection of email addresses of editors-in-chief across various academic journals in the field of Medicine & Public Health. The script navigates web pages to extract journal information, identifies editors, and retrieves their contact details from publicly available sources, emphasizing PubMed entries.

## Features:

1. Automated navigation of journal listing pages

2. Extraction of editors-in-chief information from academic journals

3. Email address discovery from PubMed

4. Email verification and accuracy assessment

5. Data compilation into a structured Excel spreadsheet

## Installation
Ensure you have Python 3.9 installed on your system. You can download it from python.org.

### Dependencies
BeautifulSoup4 for parsing HTML content
Requests for making HTTP requests
Pandas for data manipulation and export
tqdm for progress bars
Selenium WebDriver for automated browser navigation

Install the required Python packages using the following command:
```
pip install beautifulsoup4 requests pandas tqdm selenium
```

## Setup
Clone this repository or download the source code.

Navigate to the project directory.

(Optional) Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Usage
To run the scraper, execute the main script from the terminal or command prompt:
```
python main.py
```
Modify main.py to adjust the page_start, page_end, and other parameters according to your specific needs.

## Data Structure
The output data is structured as follows:

1. Editor's Name

2. Journal URL

3. Email Address

4. Accuracy Score (of the email address)

This data is exported to an Excel file named Email-[Field]-pg[StartPage]-[EndPage].xlsx.

## Acknowledgements
This project utilizes data from PubMed for email address discovery.
