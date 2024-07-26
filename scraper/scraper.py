import requests
from bs4 import BeautifulSoup

def perform_scraping(form_data):
    url = form_data.get('url')
    item_selector = form_data.get('item_selector')
    title_selector = form_data.get('title_selector')
    price_selector = form_data.get('price_selector')
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.select(item_selector)
        scraped_data = []
        for item in items:
            title = item.select_one(title_selector).get_text(strip=True) if item.select_one(title_selector) else 'No title'
            price = item.select_one(price_selector).get_text(strip=True) if item.select_one(price_selector) else 'No price'
            scraped_data.append({'title': title, 'price': price})
        
        return scraped_data
    
    except Exception as e:
        return {'error': str(e)}
