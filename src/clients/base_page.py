from pathlib import Path

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class BasePage:
    def __init__(self, *args, **kwargs):

        def _convert_arg_to_bool(arg, default=None):
            return arg.lower() in ('yes', 'true', 'y') if arg is not None and len(arg) > 0 else default

        is_run_silently = args[0].is_run_silently
        chrome_driver_path = args[0].chrome_driver_path
        self.options = Options()
        if _convert_arg_to_bool(is_run_silently):
            self.options.add_argument("headless")
        self.options.add_argument('ignore-certificate-errors')
        window_size = kwargs.get('window_size', 'start-maximized')
        self.options.add_argument(window_size)
        if not chrome_driver_path:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager
                                                           ().install()), options=self.options)
            print(self.driver.service.path)
        else:
            service = Service(chrome_driver_path)
            self.driver = webdriver.Chrome(service=service, options=self.options)

    @property
    def tear_down(self):
        self.driver.quit()
