import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
from requests.exceptions import RequestException
from tqdm import tqdm  # Import tqdm

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

def find_journal_urls(start_page=1, end_page=10):
    print("FINDING URLS")
    journal_urls = []
    for i in tqdm(range(start_page, end_page + 1), desc="Fetching Journal URLs"):
        # Change link based on the intended website
        page_url = f"https://link.springer.com/search/page/{i}?facet-content-type=%22Journal%22&facet-discipline=%22Medicine+%26+Public+Health%22"
        soup = get_soup(page_url)
        if soup:
            journals = soup.find_all('li', class_='has-cover')
            for journal in journals:
                relative_url = journal.find('a', class_='title')['href']
                journal_urls.append(f"https://link.springer.com{relative_url}")
        time.sleep(1)
    return journal_urls

def extract_editors_in_chief(journal_urls):
    print("FINDING EDITORS")
    editors_info = []
    for url in tqdm(journal_urls, desc="Extracting Editors"):
        soup = get_soup(url)
        if soup:
            editor_elements = soup.find_all('li', class_='u-display-inline')
            for editor in editor_elements:
                editor_name = editor.get_text(strip=True).strip(",")
                editors_info.append({'name': editor_name, 'journal_url': url, 'email': None, 'accuracy': None})
        time.sleep(1)
    return editors_info

def find_emails_for_editors(editors_info, max_publications=10, min_accuracy=0.1):
    print("FINDING EMAILS")
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    for editor_info in tqdm(editors_info, desc="Finding Emails"):
        search_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={editor_info['name']}"
        soup = get_soup(search_url)
        if soup:
            publications = soup.find_all('a', class_='docsum-title', limit=max_publications)
            for pub in publications:
                article_id = pub.get('data-article-id')
                if article_id:
                    article_url = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
                    article_soup = get_soup(article_url)
                    if article_soup:
                        affiliation = article_soup.find('li', {'data-affiliation-id': True})
                        if affiliation:
                            emails = email_pattern.findall(affiliation.get_text())
                            if emails:
                                top, accuracy = predict_email_accuracy(editor_info['name'], emails)
                                if accuracy >= min_accuracy:
                                    editor_info['email'] = top
                                    editor_info['accuracy'] = accuracy
                                    break  # Stop searching once a suitable email is found
        time.sleep(1)
        for editor in editors_info:
            # Check if the editor has an email and the accuracy is above the threshold

            if editor['email'] is None and editor['accuracy'] is None:
                editor['email'] = "None"
                editor["accuracy"] = "None"
    return editors_info

def predict_email_accuracy(editor_name, emails):
    print(emails)
    best_email = emails[0]
    max_score = 0
    editor_name_parts = editor_name.lower().split()  # Split the editor's name into parts and convert to lowercase for comparison

    for email in emails:
        email_local_part = email.split('@')[0].lower()  # Consider only the local part of the email for name comparison
        email_local_part = "".join(c for c in email_local_part if c.isalpha()) # Turn it into a string without any symbols
        points = 0
        # Check for the presence of each part of the editor's name in the email address
        for part in editor_name_parts:
            # print(part)
            if part in email_local_part:
                points += len(part)  # Increase points based on the length of the matching part of the name
            else:
                if part[0] in email_local_part:
                    points += 1
            # print(points)
        score = points / (
                    len(email_local_part) + 1)  # Normalize the score by the length of the email local part + 1 to avoid division by zero
        if (score > max_score):
            max_score = score
            best_email = email

    return best_email, max_score

def write_data(editors_info, filename):
    df = pd.DataFrame(editors_info)
    df.to_excel(filename, index=False)

def main():
    type = "MedicineAndPublicHealth" #Change according to the topic
    page_start, page_end = 23, 44 #Change according to which pages you want to access
    # Find the journal URLs
    journal_urls = find_journal_urls(page_start, page_end)
    # Find the names of the Editors in Chief
    editors_info = extract_editors_in_chief(journal_urls)
    # Find the emails of the Editors in Chief
    editors_info_with_emails = find_emails_for_editors(editors_info)
    # Create name of file based on topic and pages covered
    filename = f"Email-{type}-pg{page_start}-{page_end}.xlsx"
    # Write all the information into an excel file
    write_data(editors_info_with_emails, filename)

if __name__ == '__main__':
    main()
