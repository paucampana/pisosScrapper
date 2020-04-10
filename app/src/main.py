from bs4 import BeautifulSoup

import sendMail
import Houses
import requests
import config
import concurrent.futures
import logging
import numpy as np
import pandas as pd
logging.basicConfig(level=logging.INFO)


def get_set_house(urls):
    subset_df = pd.DataFrame(columns=["Titulo", "Zona", "Precio", "Habitaciones", "Aseos", "Metros cuadrados",
                 "Planta", "Precio (€/m²)", "Antigüedad", "Estado conservacion", "URL", "Descripcion"])
    max_workers = config.MAX_WORKERS
    houses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        results = executor.map(Houses.get_house, urls)
        for url, house_item, e in results:
            if e is None:
                subset_df = subset_df.append(house_item, ignore_index=True)
            else:
                logging.error(e)
                logging.error("***NOT ADDED. CHECK: " + url + " *** EXCEPTION: " + type(e).__name__ )
    return subset_df;



page = 1
continue_searching = True
main_links =  [] ## avoid being redirected to pisos.com first page

#like_house("https://www.pisos.com/comprar/piso-esparreguera_centro_urbano-97582198372_519327")
df = pd.DataFrame(columns=["Titulo", "Zona", "Precio", "Habitaciones", "Aseos", "Metros cuadrados",
             "Planta", "Precio (€/m²)", "Antigüedad", "Estado conservacion", "URL", "Descripcion"])
while continue_searching:
    links = []
    r  = requests.get(config.URL_PISOS + config.URL_PLACE + str(page))
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    data_all_houses = soup.findAll('div',attrs={'itemtype':'http://schema.org/SingleFamilyResidence'})
    for data_house in data_all_houses:
        meta_tag = data_house.find('meta',attrs={'itemprop':'url'})
        link = meta_tag.attrs['content']
        if link is not None:
            links.append(config.URL_PISOS + link)
    logging.info("found: " + str(len(links)) + " in page: " + str(page))
    if links == main_links:
        continue_searching = False
    if page == 1:
        main_links = links
    if config.TEST_MODE:
        links = [links[1]]
        continue_searching = False
    subset_df = get_set_house(links)
    df = df.append(subset_df)
    page += 1

logging.info('Finish webscrapping proces. Creating CSV')
df = df.replace(np.nan, '-', regex=True)
df.to_csv(config.FILEPATH)
sendMail.sendResults()
