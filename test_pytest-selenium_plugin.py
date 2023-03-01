'''
Description:
    A pytest-selenium plugin example, perfect framework to work with pytest html plugin for HTML reports with screenshots.
    https://pytest-selenium.readthedocs.io/en/latest/user_guide.html

Install:
pip3 install -r requirements.txt

Notes:
- HTML report embedded screenshots for assert failures AND exceptions like element not found!
- Browser type is defined in pytest.ini and can be overwritten in pytest CLI parameters.
- setup to start browser, teardown to close browser is already taken care by pytest-selenium plugin framework.
- webdriver browser and common settings (fixtures) are defined in conftest.py, and you can move to test files if you like.
- Exceptions will cause test to fail and terminate just as assert failure.
'''
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By       
#from selenium.webdriver.support.events import EventFiringWebDriver
#from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import inspect

# explicit wait time after loading a new page to check page match.
TIMEWAIT_PAGE_LOAD = 3

# %(levelname)7s to align 7 bytes to right, %(levelname)-7s to left.
common_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)-7s][%(lineno)-3d]: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",
)

# Note: To create multiple log files, must use different logger name.
def setup_logger(log_file, level=logging.INFO, name="", formatter=common_formatter):
    """Function setup as many loggers as you want."""
    handler = logging.FileHandler(log_file, mode="w")  # default mode is append
    # Or use a rotating file handler
    # handler = RotatingFileHandler(log_file,maxBytes=1024, backupCount=5)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# default debug logger
log = setup_logger("debug.log", logging.INFO, name=__name__)
    
# Page Object Model            
class TestPythonOrgPageModel():
    def test_python_homepage_pageObject(self,selenium): 
        self.wd = selenium
        # Test function
        self.wd.get('https://www.python.org/')
        homepage = PythonOrgHomepage(self.wd)
        # Always check if it is the right page first
        assert homepage.is_page_matched()
        # Test Validations 
        # assert homepage.getTitle() == 'Failed Title'
        pyPiHomepage = homepage.click_pypi()
        # Check it redirects to PyPi website.
        assert pyPiHomepage.is_page_matched()
        
        # Search by 'selenium' and check 1st result is selenium package.
        searchText = 'selenium'
        searchResultPage = pyPiHomepage.searchPackage(searchText)
        assert searchResultPage.is_page_matched()
        check_result_row = 1
        expected_resultText = 'selenium99'
        actual_resultText = searchResultPage.getSearchResultText(check_result_row) 
        assert actual_resultText == expected_resultText, 'search result not matched'        

# Page Object design 
# https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#page-object-design-pattern (Java Example only)
# https://selenium-python.readthedocs.io/page-objects.html
# https://github.com/gunesmes/page-object-python-selenium
''' Principles
When a page is changed, you only need to change that page object, not the test functions.
Page objects themselves should never make verifications or assertions. 
There is one verification which can, and should, be within the page object and that is to verify that the page, and possibly critical elements on the page, were loaded correctly.
'''
       
class PythonOrgHomepage(): 
    def __init__(self, webdrive):
        self.wd = webdrive   
    
    # Call this to verify if page is matched (1st check) right after initialization
    def is_page_matched(self):
        # Check if it is the right page by title
        # return self.wd.title == 'Welcome to Python.org'
        try:
            ret = WebDriverWait(self.wd, TIMEWAIT_PAGE_LOAD).until( EC.title_is('Welcome to Python.org' ))
        except:
            ret = False
        return ret
        
    def getTitle(self):
        return self.wd.title
    
    # return None if there are exceptions
    def click_pypi(self):
        # Catch find element failure to get better reading log prints 
        try:
            elem = self.wd.find_element_by_xpath('//*[@title="Python Package Index"]')            
        except NoSuchElementException:
            log.info('Failed to locate PyPi link.')
            return None
            
        elem.click()
        return PyPiHomepage(self.wd)

class PyPiHomepage(): 
    def __init__(self, webdrive):
        self.wd = webdrive   
    
    def is_page_matched(self):
        try:
            ret = WebDriverWait(self.wd, TIMEWAIT_PAGE_LOAD).until(EC.title_is('Search results · PyPI' ))
        except:
            ret = False
        return ret
        
    def searchPackage(self,searchText):       
        self.wd.find_element_by_id("search").clear()
        self.wd.find_element_by_id("search").send_keys(str(searchText).strip())
        self.wd.find_element_by_id("search").send_keys(Keys.ENTER)
        # wait for page to load, find an element on next page, order dropdown in this case. --- Removed and move to is_page_matched with wait-until function in next Page 
        # wait_element_nextPage = self.wd.find_element_by_xpath('//*[@id="order"]')
        return PyPiSearchResultPage(self.wd)

class PyPiSearchResultPage(): 
    def __init__(self, webdrive):
        self.wd = webdrive   
    
    def is_page_matched(self):
        log.info('Current page tile:' + self.wd.title)
        # return self.wd.title == 'Search results · PyPI'
        try:
            ret = WebDriverWait(self.wd, TIMEWAIT_PAGE_LOAD).until( EC.title_is('Search results · PyPI' ))
        except:
            ret = False
        return ret
        
    
    # index starts with 1
    def getSearchResultText(self,index):
        self.result_index = index
        elem_found = True
        try:
            self.elem = self.wd.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/form/div[3]/ul/li[%s]/a/h3/span[1]' 
                                                      % self.result_index)
        except NoSuchElementException:
            log.info('Search result row not found.')
            elem_found = False
            return None   
        if elem_found == True:
            log.info('Found search result row .')
            log.info('elem text:'+ self.elem.text)
            return self.elem.text
 
    