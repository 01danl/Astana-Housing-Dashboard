import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import uuid

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = 'https://krisha.kz/prodazha/kvartiry/astana/'
data = []


def scr_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        listings = soup.find_all('div', class_='a-card')
        for listing in listings:
            try:
                title = listing.find('a', class_='a-card__title')
                title_text = title.get_text(strip=True) if title else None

                rooms = None
                area = None
                floor = None
                if title_text:
                    parts = [part.strip() for part in title_text.split('·')]
                    if len(parts) > 0:
                        first_part = parts[0]
                        if 'комнатная' in first_part:
                            rooms = first_part.split('-')[0].strip() if '-' in first_part else 'Студия'
                        if len(parts) > 1:
                            second_part = parts[1]
                            if 'м²' in second_part:
                                area = second_part
                        if len(parts) > 2:
                            third_part = parts[2]
                            if '/' in third_part or 'этаж' in third_part:
                                floor = third_part
                    """
                    parts = title_text.split()
                    print(f"parts: {parts}")
                    rooms = parts[0].split('-')[0].strip() if len(parts) > 0 else None
                    area = parts[3].strip() if len(parts) > 2 else None
                    floor = parts[6].strip() if len(parts) > 3 else None
                """
                district = listing.find('div', class_='a-card__subtitle')
                district_text = district.get_text(strip=True) if district else None

                price = listing.find('div', class_='a-card__price')
                price_text = price.get_text(strip=True) if price else None

                if district_text:
                    parts = district_text.split(',', 1)
                    district = parts[0].strip() if len(parts) > 0 else None
                    address = parts[1].strip() if len(parts) > 1 else None

                description = listing.find('div', class_='a-card__text-preview')
                description_text = description.get_text(strip=True) if description else None

                data.append({
                    'Rooms': rooms,
                    'Area': area,
                    'Floor': floor,
                    'District': district,
                    'Price': price_text,
                    'Address': address,
                    'Details': description_text
                })
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue
        next_page = soup.find('a', class_='paginator__btn paginator__btn--next')
        return urljoin(url, next_page['href']) if next_page and next_page.get('href') else None

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    current_url = url
    page_count = 1
    max_pages = 80

    while current_url and page_count < max_pages:
        print(f"Scraping page {current_url}... page_count={page_count}")
        next_page = scr_page(current_url)
        current_url = next_page
        page_count += 1

        #time.sleep(random.uniform(0.5, 1.5))

    df = pd.DataFrame(data)
    df.to_csv('krisha_astana_rentals.csv', index=False, encoding='utf-8')
    print("Succesful")

if __name__ == '__main__':
        main()
