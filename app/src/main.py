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

def sendResults():
    try:
        with open(filePath) as f:
            csv_length = sum(1 for line in f)
            print("TOTAL FOUND: " + str(csv_length - 1))
            if csv_length > 1:
                subject = "INFORME DIA " + simple_date
                to_email = ["pau.campanya.soler@gmail.com"]
                sendMail.sendMail(subject, fileName, to_email)
            else:
                print ("EMPTY CSV. NOT SENT")

    except Exception as e:
        print("***EXCEPTION SENDING MAIL: " + type(e).__name__ + " ***")




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


def get_set_house(urls):
    max_workers = 5
    houses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        results = executor.map(get_houses, urls)
        for url, house, e in results:
            if e is None:
                houses.append(house)
            else:
                print("***NOT ADDED. CHECK: " + url + " *** EXCEPTION: " + type(e).__name__ )
            
            
    write_csv(houses)
    return;


def write_csv(houses):
    with open(filePath, 'a') as f:
        writer = csv.writer(f, dialect='myDialect')
        for house in houses:
            writer.writerow(house.getDataAsList())
    f.close()
    return;


WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images':2})
chrome_options.add_argument("--remote-debugin-port=9222")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)


url_fotocasa = "https://www.pisos.com"
# url_start = "/es/alquiler/casas/barcelona-capital/todas-las-zonas/l/"
# url_end = "?combinedLocationIds=724,9,8,232,376,8019,0,0,0"
url_start = "/venta/pisos-esparreguera/"
url_end = ""
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




        

page = 0
safe_finish = 1 #Numbers of pages that need to have 0 links to finish searching
continue_searching = True
while continue_searching:
    links = []  
    r  = requests.get(url_fotocasa + url_start + str(page) + url_end)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    data_all_houses = soup.findAll('div',attrs={'itemtype':'http://schema.org/SingleFamilyResidence'})
    print(data_all_houses[0].find('meta',attrs={'itemprop':'url'}))
    for data_house in data_all_houses:
        link = data_house.find('a')
        if link is not None:
            links.append(url_fotocasa + link['href'])
    print("found: " + str(len(links)) + " in page: " + str(page))
    if len(links) == 0:
        safe_finish -= 1
        if safe_finish <= 0:
            continue_searching = False
    else:
        ##get_set_house(links)  
        safe_finish = 3     
    page += 1;
    continue_searching = False

#sendResults()








