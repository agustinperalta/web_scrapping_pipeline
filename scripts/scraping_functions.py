import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from scripts.util_functions import session_init, listado_provincias, armar_links, last_page_extractor, id_info

def task_scrape_ids_and_hrefs():
    session = session_init()
    provincias = listado_provincias('https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.2/download/provincias.json', session)
    link_prov_list = armar_links(provincias)

    data = {
        'id_property': [],
        'link_property': []
    }
    
    for link in link_prov_list:
        try:
            response_prov = session.get(link, timeout=10)
            soup_prov = BeautifulSoup(response_prov.content, 'html.parser')
            last_page = last_page_extractor(soup_prov)
            
            if last_page:
                for i in range(1, last_page + 1):
                    new_url = f"{link}?pagina={i}"
                    print(new_url)
                    response_page = session.get(new_url, timeout=10)
                    
                    if response_page.status_code == 200:
                        soup_page = BeautifulSoup(response_page.content, 'html.parser')
                        listing_container = soup_page.find('div', class_='listing-container')
                        
                        if listing_container:
                            properties = soup_page.find_all('div', class_='listing__item')
                            for prop in properties:
                                id_property, link_property = id_info(prop)
                                if id_property and link_property:
                                    data['id_property'].append(id_property)
                                    data['link_property'].append(link_property)
                        else:
                            print("No hay listado de propiedades")
                    else:
                        print(f"Error fetching page: {response_page.status_code}")
                        break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching province link: {e}")
            continue
    
    # Puedes guardar o devolver los datos recolectados aquí
    print(data)
