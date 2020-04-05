import privateConfig
from selenium.webdriver.chrome.options import Options

URL_PISOS = "https://www.pisos.com"
URL_PLACE = "/venta/pisos-esparreguera/"

URL_LOG_IN = "https://www.pisos.com/Login"

USER_PISOS = "informe.casas@gmail.com"
PW_PISOS = "17InformeCasas"
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FILEPATH  = './excels/houses_dataframe.csv'
MAIL_TO_SEND = "informe.casas@gmail.com"
TEST_MODE = False

MAX_WORKERS = 1

def get_Chrome_Options ():
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images':2})
    chrome_options.add_argument("--remote-debugin-port=9222")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    if privateConfig.PathNeeded:
        chrome_options.binary_location = privateConfig.ChromeDriverPath
    return chrome_options
