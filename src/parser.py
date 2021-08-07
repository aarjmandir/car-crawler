from bs4 import BeautifulSoup as bs


def clear_text(text):
    chars = ["-", "\n", "\r", "،", ",", "\xa0"]
    for char in text:
        if char in chars:
            if char == "،":
                text = text.replace(char, "-")
                continue
            text = text.replace(char, "")
    return text


def get_adv_pic(adv):
    container = adv.find("div", "gallery-wrap")
    if container:
        adv_images = container.find_all('img')
        if adv_images:
            image_list = []
            for img in adv_images:
                if img.attrs.get('data-src'):
                    image_list.append(img['data-src'])
                else:
                    image_list.append(img['src'])
            return image_list


def get_adv_title(adv):
    title = adv.find("h2", "title")
    if title:
        return title.text[5:]


def is_used(adv):
    type = adv.find("p", "stock-type")
    if type:
        return type.text


def get_adv_year(adv):
    title = adv.find("h2", "title")
    if title:
        return title.text[:4]


def get_adv_mileage(adv):
    mileage = adv.find("div", "mileage")
    if mileage:  
        return mileage.text


def get_adv_price(adv):
    price = adv.find("span", "primary-price")
    if price:
        return price.text


def get_adv_rating(adv):
    container = adv.find("sds-rating")
    if container:
        return container.find("span", "sds-rating__count").text


def get_adv_reviews(adv):
    container = adv.find("sds-rating")
    if container:
        reviews = container.find("span", "sds-sds-rating__link").text
        return reviews.split(" ")[0]


def get_adv_list(data):
    soup = bs(data)
    adv_wrapper = soup.find( class_="vehicle-cards" )
    if adv_wrapper:
        adv_list = adv_wrapper.find_all("div", "vehicle-card")
        if adv_list:
            return adv_list


def get_data(adv):
    adv_title = get_adv_title(adv)
    adv_pic = get_adv_pic(adv)
    adv_year = get_adv_year(adv)
    adv_used = is_used(adv)
    adv_mileage = get_adv_mileage(adv)
    adv_price = get_adv_price(adv)
    adv_rating = get_adv_rating(adv)
    adv_reviews = get_adv_reviews(adv)
    data = {
        "adv_title": adv_title,
        "adv_pic": adv_pic,
        "adv_year": adv_year,
        "adv_used": adv_used,
        "adv_mileage": adv_mileage,
        "adv_price": adv_price,
        "adv_rating": adv_rating,
        "adv_reviews": adv_reviews
    }
    return data