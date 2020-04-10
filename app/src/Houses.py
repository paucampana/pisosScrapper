from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import scraping
import config
import logging
import pandas as pd
import time
logging.basicConfig(level=logging.INFO)


def get_house_from_html_pisos(soup, url):
    #logging.debug(soup.encode('utf-8'))
    mapHouse = {}
    mapHouse["URL"] = url
    mapHouse["Titulo"] = scraping.get_string_from_class(soup, "h1", 'title')
    mapHouse["Zona"] = scraping.get_string_from_class(soup, "h2", 'position')
    mapHouse["Precio"] = scraping.get_string_from_class(soup, "span", 'h1 jsPrecioH1').replace("€", "").replace(".", "")
    num_hab = ""
    num_bano = ""
    metro_q = ""
    basicData = soup.find('div',attrs={'class':'basicdata-info'})
    divBasicDatas = basicData.findAll("div")
    for divBasicData in divBasicDatas:
        if divBasicData.find('div',attrs={'class':'icon-habitaciones'}) is not None:
            mapHouse["Habitaciones"] = divBasicData.text.replace("habs", "").strip()
        if divBasicData.find('div',attrs={'class':'icon-banyos'}) is not None:
            mapHouse["Aseos"] = divBasicData.text.replace("baño", "").replace("s","")
        if divBasicData.find('div',attrs={'class':'icon-superficie'}) is not None:
            mapHouse["Metros cuadrados"] = divBasicData.text.replace("m²", "")
        if divBasicData.find('div',attrs={'class':'icon-planta'}) is not None:
            mapHouse["Planta"] = divBasicData.text.split()[0]
        if divBasicData.find('div',attrs={'class':'icon-eurmetro2'}) is not None:
            mapHouse["Precio (€/m²)"] = divBasicData.text.split()[0]
    mapHouse["Descripcion"] = soup.find('div',{"id":"descriptionBody"}).text.strip().replace("\n"," ")
    antic_icon = soup.find('span',{'class' : 'icon-antiguedad'})
    if antic_icon is not None:
        mapHouse["Antigüedad"] = antic_icon.find_parent('li').find_all('span')[1].text.replace(': ', '')
    conservacion_icon = soup.find('span',{'class' : 'icon-estadoconservacion'})
    if conservacion_icon is not None:
        mapHouse["Estado conservacion"] = conservacion_icon.find_parent('li').find_all('span')[1].text.replace(': ', '')
    caracteristicas = soup.find_all('div', {'class' : 'charblock'})
    """
    for caracteristica in caracteristicas:
        first_element = True
        caracteristica_info = ""
        tipoCaracteristica = scraping.get_string_from_class(caracteristica, "h2", 'title')
        tags = caracteristica.find_all('li',{'class': 'charblock-element'})
        for tag in tags:
            info = tag.find_all('span')
            if len(info) > 0:
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
            mapHouse['Caracteristicas'] = caracteristica_info
        if "Muebles" in tipoCaracteristica:
            mapHouse['Muebles y acabados'] = caracteristica_info
        if "Equipamiento" in tipoCaracteristica:
            mapHouse['Equipamiento e instalaciones'] = caracteristica_info
        if "Certificado" in tipoCaracteristica:
            mapHouse['Certificado energetico'] = caracteristica_info
    """
    house_item = pd.Series(mapHouse)
    return house_item;


def is_house_favorite(house_item):
    if not 'Habitaciones' in house_item.keys() or not 'Precio'  in house_item.keys() or not "Metros cuadrados" in house_item.keys():
        logging.debug("Some parameters are empty. Not a favorite house candidate")
        return False
    else:
        m2 = house_item["Metros cuadrados"]
        precio = house_item["Precio"]
        habitaciones = house_item["Habitaciones"]
    try:
        if (int(m2) >= 80 and int(precio) <= 120000 and int(habitaciones) >= 3):
            logging.debug("Is a favorite house candidate")
            return True
        else:
            logging.debug("It is not a  favorite house candidate")
    except Exception as e:
        logging.debug("Some parameters can not be converted to integer. Not a favorite house candidate")
        return False

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
        if button_fav == "icon icon-fav selected":
            logging.debug("already liked. Doing nothing")
        else:
            driver.find_element_by_id("dvGuardarFavoritos").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close() ##If all are closed, try with driver.close()
        refresh_retries = 0
        return None
    except Exception as e:
        logging.error('EXCEPTION with LIKING url ' + url)
        logging.error(e)
        return e


def get_house(url):
    refresh_retries = 2
    while(refresh_retries > 0):
        try:
            chrome_options = config.get_Chrome_Options()
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(10)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            house_item = get_house_from_html_pisos(soup, url)
            if is_house_favorite(house_item):
                like_house(url)
            driver.close() ##If all are closed, try with driver.close()
            return url, house_item, None
        except Exception as e:
            logging.error('EXCEPTION with url ' + url)
            logging.error(e)
            refresh_retries -= 1
            if refresh_retries <= 0:
                return url, None, e
