from House import House
from bs4 import BeautifulSoup
from selenium import webdriver
import scraping
import sendMail
import requests
import config
import privateConfig
import csv
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import concurrent.futures
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def sendResults():
    try:
        with open(filePath) as f:
            csv_length = sum(1 for line in f)
            logging.info("TOTAL FOUND: " + str(csv_length - 1))
            if csv_length > 1:
                subject = "INFORME DIA " + simple_date
                to_email = ["pau.campanya.soler@gmail.com"]
                sendMail.sendMail(subject, fileName, to_email)
            else:
                logging.info("EMPTY CSV. NOT SENT")

    except Exception as e:
        logging.error("***EXCEPTION SENDING MAIL: " + type(e).__name__ + " ***")




def get_house_from_html_pisos(soup, url):
    #logging.debug(soup.encode('utf-8'))
    mapHouse = {}
    mapHouse["url"] = url
    mapHouse["titulo"] = scraping.get_string_from_class(soup, "h1", 'title')
    mapHouse["zona"] = scraping.get_string_from_class(soup, "h2", 'position')
    mapHouse["precio"] = scraping.get_string_from_class(soup, "span", 'h1 jsPrecioH1').replace("€", "")
    
    num_hab = ""
    num_bano = ""
    metro_q = ""
    basicData = soup.find('div',attrs={'class':'basicdata-info'})
    divBasicDatas = basicData.findAll("div")
    for divBasicData in divBasicDatas:
        if divBasicData.find('div',attrs={'class':'icon-habitaciones'}) is not None:
            mapHouse["num_hab"] = divBasicData.text.replace("habs", "")
        if divBasicData.find('div',attrs={'class':'icon-banyos'}) is not None:
            mapHouse["num_bano"] = divBasicData.text.replace("baño", "")
        if divBasicData.find('div',attrs={'class':'icon-superficie'}) is not None:
            mapHouse["metro_q"] = divBasicData.text.replace("m²", "")
        if divBasicData.find('div',attrs={'class':'icon-planta'}) is not None:
            mapHouse["planta"] = divBasicData.text.split()[0]
        if divBasicData.find('div',attrs={'class':'icon-eurmetro2'}) is not None:
            mapHouse["precio_m"] = divBasicData.text.split()[0]
    mapHouse["description"] = soup.find('div',{"id":"descriptionBody"}).text.lstrip()
    antic_icon = soup.find('span',{'class' : 'icon-antiguedad'})
    if antic_icon is not None:
        mapHouse["antic"] = antic_icon.find_parent('li').find_all('span')[1].text.replace(': ', '')
    conservacion_icon = soup.find('span',{'class' : 'icon-estadoconservacion'})
    if conservacion_icon is not None:
        mapHouse["conservacion"] = conservacion_icon.find_parent('li').find_all('span')[1].text.replace(': ', '')
    caracteristicas = soup.find_all('div', {'class' : 'charblock'})
    for caracteristica in caracteristicas:
        first_element = True
        caracteristica_info = ""
        tipoCaracteristica = scraping.get_string_from_class(caracteristica, "h2", 'title')
        tags = caracteristica.find_all('li',{'class': 'charblock-element'})
        for tag in tags:
            info = tag.find_all('span')
            kind = info[0].text
            description = ""
            if len(info) > 1:
                description = info[1].text.replace(': ', '')
            if first_element:
                caracteristica_info += kind + ": " + description
            else: 
                caracteristica_info += ", " + kind + ": " + description
            first_element = False
        if "Datos" in tipoCaracteristica:
            mapHouse['dato_basicos'] = caracteristica_info
        if "Muebles" in tipoCaracteristica:
            mapHouse['muebles_i_acabados'] = caracteristica_info
        if "Equipamiento" in tipoCaracteristica:
            mapHouse['equipamiento_e_instalaciones'] = caracteristica_info
        if "Certificado" in tipoCaracteristica:
            mapHouse['certificado_energetico'] = caracteristica_info
    house = House(mapHouse)
    return house;


def get_houses(url):
    refresh_retries = 1
    while(refresh_retries > 0):
        try:
            chrome_options = config.get_Chrome_Options()
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(10)
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            myhouse = get_house_from_html_pisos(soup, url)
            driver.close() ##If all are closed, try with driver.close()
            refresh_retries = 0
            return url, myhouse, None
        except Exception as e:
            logging.error('EXCEPTION with url ' + url)
            logging.error(e)
            refresh_retries -= 1
            if refresh_retries <= 0:
                return url, None, e


def like_house(url):
    try:
        chrome_options = config.get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)
        driver.get(config.URL_LOG_IN)
        driver.find_element_by_id("Email").send_keys(config.USER_PISOS)
        driver.find_element_by_id("Password").send_keys(config.PW_PISOS)
        driver.find_elements_by_xpath("//input[@data-id='loginButton']")[0].submit();
        time.sleep(5)
        #At this point we are logged in
        driver.get(url)
        time.sleep(5)
        button_fav = driver.find_element_by_id("dvGuardarFavoritos").get_attribute("class")
        print(button_fav)
        if button_fav == "icon icon-fav selected":
            logging.debug("already liked. Doing nothing")
        else:
            driver.find_element_by_id("dvGuardarFavoritos").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close() ##If all are closed, try with driver.close()
        refresh_retries = 0
        return None
    except Exception as e:
        logging.error('EXCEPTION with url ' + url)
        logging.error(e)
        return e

def get_set_house(urls):

    max_workers = config.MAX_WORKERS
    houses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        results = executor.map(get_houses, urls)
        for url, house, e in results:
            if e is None:
                houses.append(house)
            else:
                logging.error("***NOT ADDED. CHECK: " + url + " *** EXCEPTION: " + type(e).__name__ )


    write_csv(houses)
    return;


def write_csv(houses):
    with open(filePath, 'a') as f:
        writer = csv.writer(f, dialect='myDialect')
        for house in houses:
            writer.writerow(house.getDataAsList())
    f.close()
    return;




filePath = "excels/" + datetime.now().strftime('%Y-%m-%d--%H-%M-%S') + ".csv"
fileName = datetime.now().strftime('%Y-%m-%d--%H-%M-%S') + ".csv"
simple_date = datetime.now().strftime('%Y/%m/%d')
csv.register_dialect('myDialect',
quoting=csv.QUOTE_ALL,
skipinitialspace=True)
first_row = ["Titulo", "Zona", "Precio", "Habitaciones", "Baños", "Metros quadrados",
             "Planta", "Precio (€/m²)", "Description", "Estado conservacion", "Caracteristicas", "URL"]
with open(filePath, 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(first_row)
        f.close()






page = 1
continue_searching = True
main_links =  [] ## avoid being redirected to first page

like_house("https://www.pisos.com/comprar/piso-esparreguera_centro_urbano-97582198372_519327")

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
    logging.debug("found: " + str(len(links)) + " in page: " + str(page))
    if links == main_links:
        continue_searching = False
    if page == 1:
        main_links = links
    if config.TEST_MODE:
        links = [links[1]]
    get_set_house(links)
    page += 1;

    if config.TEST_MODE:
        continue_searching = False
    
#sendResults()
