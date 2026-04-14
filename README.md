# pytest-selenium_plugin_examples
A web test automation framework example using pytest-selenium plugin

Along with pytest-html, which demonstrates the following features:
* HTML report embedded screenshots for assert failures AND exceptions like element not found!
* Browser type is defined in pytest.ini and can be overwritten in pytest CLI parameters.
* setup to start browser, teardown to close browser is already taken care by pytest-selenium plugin framework.
* webdriver browser and common settings (fixtures) are defined in conftest.py, and you can move to test files if you like.
* Exceptions will cause test to fail and terminate just as assert failure.

# Set up
1. Install Python3
2. Install required packages by pip (pip3 in Linux)

`pip install -U pytest selenium pytest-html pytest-selenium`

or 

`pip install -r requirements.txt`

3. Download WebDriver executables

Download WebDriver executables for your respective browsers under test, e.g. [chromedriver](https://chromedriver.chromium.org/downloads), [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and [Firefox webdriver](https://github.com/mozilla/geckodriver/releases), to a path (e.g. d:/webdriver/) and add this path to system path so that the WebDriver executables can be called anywhere. 

# Run
Download the code, and run 'pytest' in the same folder. More options are defined in pytest.ini or you can overwrite in CLI parameters.

```
# run test
pytest

# overwrite browser type
pytest --driver Chrome
```

