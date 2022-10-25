import re
import time
from asyncio import wait_for
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from base_clients.page_elements.base_elements import BaseElements
from base_clients.page_elements.element import BasePageElement
from base_clients.page_elements.element import BasePageElement

from selenium.webdriver.common.keys import Keys
from lxml import etree
from contextlib import contextmanager