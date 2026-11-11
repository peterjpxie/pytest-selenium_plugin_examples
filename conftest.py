# Change common webdriver settings
import pytest
@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium 

# configure firefox options, i.e. headless   
# https://seleniumhq.github.io/selenium/docs/api/py/webdriver_firefox/selenium.webdriver.firefox.options.html
@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument("-headless")
    return firefox_options               
                
# configure Chrome options, i.e. headless   
# https://seleniumhq.github.io/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.options.html
@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options