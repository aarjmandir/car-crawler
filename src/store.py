from urllib.parse import urlparse
from pymongo import MongoClient
from datetime import datetime
from .parser import get_adv_list, get_data
from . import config


def generate_file_name(url):
    parse = urlparse(url)
    name = (parse.query.split("&")[7] + \
            "-" + parse.query.split("&")[2] + \
            "-" + parse.query.split("&")[1] + "-" + \
            parse.query.split("&")[0]).replace("=", "_").replace("list_", "") + ".html"
    return name


def save_to_mongo(data):
    try:
        client = MongoClient(config.db_url, config.db_port) 
    except:
        client = MongoClient("localhost", 27017)
    try:
        db_name = config.db_name 
        collec_name = config.db_collection 
    except AttributeError:
        db_name = "crawl"
        collec_name = "crawl_collec"
    db = client[db_name]
    collection = db[collec_name]
    collection.insert_many(data)


def store_data(response, adv_id, file, db):
    adv_list = get_adv_list(response.text)
    if adv_list is not None:
        data = list()
        for adv in adv_list:
            adv_data = get_data(adv)
            adv_data.update({"adv_id": adv_id, "adv_receive_date": datetime.now()})
            data.append(adv_data)
            adv_id += 1
        print(data)
        if db:
            save_to_mongo(data)
        if file:
            with open('cars.txt', 'a') as f:
                for doc in data:
                    f.write(str(doc) + "\n")
        return True
    return False
