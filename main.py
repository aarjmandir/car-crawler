import requests
from src.store import store_data
from time import sleep


def crawl_site(url, db=False, file=True):
    crawl = True
    page = 0
    adv_id = 0
    price_min = input("Enter the minimum price in dollars [1000]: ")
    price_max = input("Enter the maximum price in dollars [2000]: ")
    while crawl:
        page += 1
        response = requests.get(url.format(page, price_max, price_min))
        if response.status_code == 200:
            crawl = store_data(response, adv_id, db=db, file=file)
            adv_id += 20
        if crawl:
            print(f'Page {page} crawled.')
            if db:
                print("Saved in mongo.")
            if file:
                print("Saved in file.")
        sleep(2)


if __name__ == "__main__":
    url = "https://www.cars.com/shopping/results/?page={}&list_price_max={}&list_price_min={}&maximum_distance=30&page_size=20&sort=best_match_desc&stock_type=all&year_min=2020&zip=33673"
    print("\nCrawl - www.cars.com - \n")
    db = input("Save to MongoDB (defaults: False)[Y/N]: ")
    file = input("Save to file (defaults: True)[Y/N]: ")
    db = True if db.lower() == 'y' else False
    file = False if file.lower() == 'n' else True
    crawl_site(url, db, file)
