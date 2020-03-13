from House import House
from bs4 import BeautifulSoup
from selenium import webdriver 
import scraping
import sendMail
import requests
import csv
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import concurrent.futures


def get_house_from_html_fotocasa(soup, url):
    titulo = scraping.get_string_from_class(soup, "h1", 'property-title')
    zona = scraping.get_string_from_id(soup, "span", 'ctl00_content1_PaginationTop_breadcrumbclassic_lbl_LocalizationUpperLevelwithLink')
    precio = scraping.delete_point_from_text(scraping.get_first_word(scraping.get_string_from_id(soup, "span", 'priceContainer')))
    num_hab = scraping.get_first_word(scraping.get_string_from_id(soup, "span", 'litRooms'))
    num_bano = scraping.get_first_word(scraping.get_string_from_id(soup, "span", 'litBaths'))
    metro_q = scraping.get_first_word(scraping.get_string_from_id(soup, "span", 'litSurface'))
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
    # print("........:")
    # ul = soup.findAll("ul",attrs={'class':"detail-extras"})
    # # result = []
    # # if ul is not None:
    # #     elements = ul.findAll("li")
    # #     for elem in elements:
    # #         result.append(get_text(elem))
    # print(ul)
    # print("..........")

    ubicacion = scraping.get_string_from_class_last(soup, "div", 'detail-section-content')
    descripcion = scraping.delete_empty_lines(scraping.get_string_from_class(soup, "p", 'detail-description'))
    res_house = House(titulo, zona, precio, num_hab, num_bano, metro_q, num_planta, 
                      contacto, contacto_tel, contacto_extra, caracteristicas, extras, ubicacion, descripcion, images, referenciaFotocasa, url)
    return res_house;

def get_houses(url):
    refresh_retries = 3
    while(refresh_retries > 0):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)  
            driver.set_page_load_timeout(15)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            myhouse = get_house_from_html_fotocasa(soup, url)
            driver.close() ##If all are closed, try with driver.close() 
            refresh_retries = 0
            return url, myhouse, None
        except Exception as e:
            refresh_retries -= 1
            if refresh_retries <= 0:    
                return url, None, e  




WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images':2})
chrome_options.add_argument("--remote-debugin-port=9222")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)


url = "https://www.fotocasa.es/vivienda/martorell/aire-acondicionado-calefaccion-terraza-trastero-ascensor-martorell-149721234?RowGrid=1&tti=3&opi=300"
u, res, e = get_houses(url)
print(e)
print(res.getData())
