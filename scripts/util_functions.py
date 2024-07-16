import requests
from unidecode import unidecode
from bs4 import BeautifulSoup

def session_init():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    return session

def listado_provincias(url, session):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        return [unidecode(prov['nombre'].lower().replace('ciudad autónoma de buenos aires', 'capital federal')) for prov in json_data['provincias'][:-1]]
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching provinces: {e}")
        return []

def armar_links(provincias):
    URL = "https://www.argenprop.com/departamentos/alquiler"
    links = set()
    for prov in provincias:
        link = f"{URL}/{prov.replace(' ', '-')}"
        links.add(link)
    return list(links)

def last_page_extractor(soup):
    paginator = soup.find('ul', class_='pagination pagination--links')
    if paginator:
        pages = paginator.find_all('li', class_='pagination__page')
        pages = [page for page in pages if 'pagination__page-prev' not in page['class'] and 'pagination__page--disable' not in page['class'] and 'pagination__page-next' not in page['class']]
        last_page = int(pages[-1].get_text())
        return last_page
    else:
        return None

def id_info(property):
    try:
        id_property = int(property.get('id'))
        link_property = property.find('a', class_='card').get('href')
        return id_property, link_property
    except (AttributeError, ValueError) as e:
        print(f"Error extracting property info: {e}")
        return None, None
