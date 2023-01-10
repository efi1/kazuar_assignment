from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.clients.locator import Locator

EXPECTED_CONDITIONS_ELEMENT = {
    'visability': 'visibility_of_element_located',
    'presence': 'presence_of_element_located',
    'clickable': 'element_to_be_clickable'
}

EXPECTED_CONDITIONS_ELEMENTS = {
    'visability': 'visibility_of_all_elements_located',
    'presence': 'presence_of_all_elements_located'
}


class BaseElements(object):

    def __init__(self, driver):
        self.element = None
        self.driver = driver

    def find(self, by, value, *args, element=None, expected_condition=None):
        locator = BaseElements.get_locator(by, value)
        if expected_condition:
            element = WebDriverWait(element if element else self.driver, 10).until(
                getattr(EC, EXPECTED_CONDITIONS_ELEMENT.get(expected_condition))(locator))
        else:
            element = getattr(element if element else self.driver, 'find_element')(locator.by, locator.value)
        return element

    def find_elements(self, by, value, *args, element=None, phrase=None, expected_condition=None, timeout=10):
        def _get_elements_by_text(_elements):
            for _element in _elements:
                if phrase.lower() in _element.text.lower():
                    yield _element

        locator = BaseElements.get_locator(by, value)
        if expected_condition:
            elements = WebDriverWait(element if element else self.driver, 10).until(
                getattr(EC, EXPECTED_CONDITIONS_ELEMENTS.get(expected_condition))(locator))
        else:
            elements = getattr(element if element else self.driver, 'find_elements')(locator.by, locator.value)
        if phrase:
            return list(_get_elements_by_text(elements))
        else:
            return elements

    @staticmethod
    def get_locator(by, value):
        return Locator(by, value)
