"""
Requires python selenium package, as well as driver for Firefox browser:
    http://selenium-python.readthedocs.io/installation.html#
"""

import sys
from selenium import webdriver


url, file = sys.argv[1:]
driver = webdriver.Firefox()
driver.get(url)
with open(file, mode='w') as html:
    html.write(driver.page_source)
driver.quit()
