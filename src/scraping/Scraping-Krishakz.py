import requests
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
                    parts = title.text_split(',')
                    rooms = parts[0].split('-')[0].strip() if len(parts) > 0 else None
                    area = parts[1].strip() if len(parts) > 1 else None
                    floor = parts[2].strip() if len(parts) > 2 else None

                district = listing.find('div', class_='a-card__subtitle')
                district_text = district.get_text(strip=True) if district else None

                price = listing.find('div', class_='a-card__price')
                price_text = price.get_text(strip=True) if price else None

                if district_text:
                    parts = district.text_split(',', 1)
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
        next_page = soup.find('a', class_='paginator__btn-text')
        return next_page['href'] if next_page else None

    except Exception as e:
        print(f"Error scraping {url}: {e}"))
        return None
