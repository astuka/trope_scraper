import requests
from bs4 import BeautifulSoup
import csv

# Function to get links from a single page
def get_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # This will grab all 'a' tags with 'href' attributes (i.e., links)
    links = []
    for a_tag in soup.find_all('a', href=True):
        # Extract only URLs for trope pages if necessary (depends on your criteria)
        href = a_tag['href']
        if 'tvtropes.org/pmwiki/pmwiki.php/Main/' in href:  # Optional: filter to ensure it’s an external link
            links.append(href)
    return links

# Function to write links to a CSV file
def write_links_to_csv(links, filename='tropes_links.csv'):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

# Main function to handle pagination and link extraction
def scrape_tvtropes_links(base_url, num_pages):
    for page_num in range(1, num_pages + 1):
        print(f"Scraping page {page_num}...")
        page_url = f"{base_url}&page={page_num}"
        links = get_links_from_page(page_url)
        write_links_to_csv(links)
        print(f"Page {page_num} done.")

if __name__ == "__main__":
    base_url = 'https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope'  # Adjust if needed
    num_pages = 61 # Adjust this to match the number of pages
    scrape_tvtropes_links(base_url, num_pages)
    print("Scraping completed.")