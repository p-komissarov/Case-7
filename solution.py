import requests
from bs4 import BeautifulSoup
import time
import ru_local as ru

BASE_URL = "https://obuv-tut2000.ru"

def parse_product(url):

    """
    Gets the values of all required parameters for a specific product.

    Args:
    url(str): A link to an arbitrary product from the search page.

    Returns:
    str: Shoe characteristics.
    """

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    article_elem = soup.find(class_="shop2-product-article")
    if article_elem:
        article = article_elem.get_text(strip=True)
    else:
        article = None

    name_elem = soup.find(class_="gr-product-name")
    if name_elem:
        name = name_elem.get_text(strip=True)
    else:
        name = None

    shoe_type = name.split()[0] if name else None

    season_elem = soup.find(class_="option-item sezon odd")
    if season_elem == None:
        season_elem = soup.find(class_="option-item sezon even")
    if season_elem:
        season = season_elem.get_text(strip=True)
    else:
        season = None

    price_elem = soup.find(class_="price-current")
    if price_elem:
        price = price_elem.get_text(strip=True)
    else:
        price = None

    sizes_elem = soup.find(class_="option-item razmery_v_korobke odd")
    if sizes_elem == None:
        sizes_elem = soup.find(class_="option-item razmery_v_korobke even")
    if sizes_elem:
        sizes = sizes_elem.get_text(strip=True)
    else:
        sizes = None

    material_elem = soup.find(class_="option-item material_verha_960 odd")
    if material_elem == None:
        material_elem = soup.find(class_="option-item material_verha_960 even")
    if material_elem:
        material = material_elem.get_text(strip=True)
    else:
        material = None

    color_elem = soup.find(class_="option-item cvet odd")
    if color_elem == None:
        color_elem = soup.find(class_="option-item cvet even")
    if color_elem:
        color = color_elem.get_text(strip=True)
    else:
        color = None

    country_elem = soup.find(class_="gr-vendor-block")
    if country_elem:
        country = country_elem.get_text(strip=True)
    else:
        country = None

    return (
    ru.ARTICLE + (article[8:] if article else ru.NO_ARTICLE) +
    ru.NAME + (name[:-9] if name else ru.NO_NAME) +
    ru.SHUE_TYPE + (shoe_type if shoe_type else ru.NO_SHUE_TYPE) +
    ru.SEASON + (season[5:] if season else ru.NO_SEASON) +
    ru.PRICE + (price if price else ru.NO_PRICE) +
    ru.SIZE + (sizes[7:] if sizes else ru.NO_SIZE) +
    ru.MATERIAL + (material[14:] if material else ru.NO_MATERIAL) +
    ru.COLOR + (color[4:] if color else ru.NO_COLOR) +
    ru.COUNTRY + (country if country else ru.APATRIDE)
    )

def main(raw_request):
    
    """
    Processes the user's search query and displays the products with their characteristics.
    Args:
    raw_request(str): The user's search query.

    Returns:
    results.txt: A file with all the shoes obtained from the user's query and their characteristics.
    """

    request = raw_request.replace(" ", "+")

    url = f"https://obuv-tut2000.ru/magazin/search?gr_smart_search=1&search_text={request}&s[sort_by]=price%20asc"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    max_pages_1 = soup.find(class_="page-num page_last")
    max_pages_2 = soup.find_all(class_="page-num")
    if max_pages_1:
        max_pages = max_pages_1.find("a")
        max_pages = int(max_pages.get_text(strip=True))
    elif max_pages_2:
        max_pages_2 = max_pages_2[-1]
        max_pages = max_pages_2.find("a")
        max_pages = int(max_pages.get_text(strip=True))
    else:
        max_pages = 1

    links = []

    for page in range(1, max_pages + 1):
        url = f"https://obuv-tut2000.ru/magazin/search?gr_smart_search={page}&search_text={request}&s[sort_by]=price%20asc"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        page_links = [BASE_URL + div.find("a")["href"] for div in soup.find_all(class_="gr-product-name")] # ПОДШАРИТЬ
        links.extend(page_links)
        time.sleep(0.5)

    with open("results.txt", "w") as f:
        for link in links:
            f.write("\n" + parse_product(link) + "\n")
            time.sleep(0.5)

if __name__ == "__main__":
    request = input(ru.ENTER).strip()
    main(request)
