from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class BaseElements(object):
    def __init__(self, **kwargs):
        self.driver = kwargs.get('driver')
        self.by = kwargs.get('by')
        self.id = kwargs.get('id')
        self.value = kwargs.get('value')
        self.locator = (self.by, self.value)
        # self.locator = kwargs.get('locator')
        # self.text = kwargs.get('text')
        # self.name = kwargs.get('name')

        self.web_element = None
        self.find()

    def find(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator=self.locator))
        self.web_element = element
        return None

    def click(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(by=self.by, id=self.id))
        element.click()
        return None

    @property
    def text(self):
        text = self.web_element.text
        return text


if __name__ == '__main__':
    url = 'https://techstepacademy.com/'
    test_inst = BaseElements(url=url)
    test_inst.new_func()
    test_inst.tearDown()
