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
import concurrent.futures
import logging

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

    titulo = scraping.get_string_from_class(soup, "h1", 'title')
    logging.debug("titulo " + titulo)
    zona = scraping.get_string_from_class(soup, "h2", 'position')
    logging.debug("zona " + zona)
    precio = scraping.get_string_from_class(soup, "span", 'h1 jsPrecioH1').replace("€", "")
    logging.debug("precio " + precio)

    num_hab = ""
    num_bano = ""
    metro_q = ""
    basicData = soup.find('div',attrs={'class':'basicdata-info'})
    divBasicDatas = basicData.findAll("div")
    for divBasicData in divBasicDatas:
        if divBasicData.find('div',attrs={'class':'icon-habitaciones'}) is not None:
            num_hab = divBasicData.text.replace("habs", "")
        if divBasicData.find('div',attrs={'class':'icon-banyos'}) is not None:
            num_bano = divBasicData.text.replace("baño", "")
        if divBasicData.find('div',attrs={'class':'icon-superficie'}) is not None:
            metro_q = divBasicData.text.replace("m²", "")
        if divBasicData.find('div',attrs={'class':'icon-planta'}) is not None:
            planta = divBasicData.text.split()[0]
        if divBasicData.find('div',attrs={'class':'icon-eurmetro2'}) is not None:
            precio_m = divBasicData.text.split()[0]
    logging.debug("num_hab " + num_hab)
    logging.debug("num_bano " + num_bano)
    logging.debug("metro_q " + metro_q)
    logging.debug("planta " + planta)
    logging.debug("precio_m " + precio_m)


    description = soup.find('div',{"id":"descriptionBody"}).text.lstrip()
    logging.debug("descripcion " + description)


    num_planta = scraping.get_first_word(scraping.get_string_from_id(soup, "span", 'litFloor'))
    contacto = scraping.get_string_from_class(soup, 'a', 'agency-microsite bold')
    if contacto == "":
        contacto = scraping.string_one_line(scraping.get_string_from_id(soup, "div", 'ctl00_ucInfoRequestGeneric_divAdvertisement'))
    contacto_tel = scraping.get_input_value_from_id(soup, "input", 'hid_AdPhone')
    if contacto_tel != "":
        contacto_tel= contacto_tel.split(":")[-1]
    contacto_extra = scraping.string_one_line(scraping.get_string_from_class_last(soup, "div", 'agency-contact-container'))
    caracteristicas = scraping.get_all_elements_ul(soup, "ul", "detail-caracteristics--list")
    extras = scraping.get_all_elements_ul(soup, "ul", "detail-extras")
    referenciaFotocasa = scraping.get_last_string(scraping.get_string_from_id(soup, "div", "detailReference"))
    images = scraping.get_all_elements_ul_by_id(soup, "ul", "containerSlider")


    ubicacion = scraping.get_string_from_class_last(soup, "div", 'detail-section-content')
    descripcion = scraping.delete_empty_lines(scraping.get_string_from_class(soup, "p", 'detail-description'))
    res_house = House(titulo, zona, precio, num_hab, num_bano, metro_q, num_planta,
                      contacto, contacto_tel, contacto_extra, caracteristicas, extras, ubicacion, descripcion, images, referenciaFotocasa, url)
    return res_house;


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
            print('EXCEPTION')
            print(e)
            refresh_retries -= 1
            if refresh_retries <= 0:
                return url, None, e


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
first_row = ["Zona", "Precio (€/mes)", "Habitaciones", "Baños", "Metros cuadrados", "Planta",
             "Ubicación", "Caracteristicas", "Extras", "Contacto", "Telefono", "Detalles contacto",
             "Descripcion", "Imagenes",  "ref. Fotocasa","url"]
with open(filePath, 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(first_row)
        f.close()






page = 1
continue_searching = True
main_links =  [] ## avoid being redirected to first page
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
