import json
import os
import re
import string
import time
from pathlib import Path

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from src.clients.base_elements import BaseElements
from src.clients.base_page import BasePage
from selenium.webdriver.common.keys import Keys


class TestsClient(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = None
        self.url = args[0].url
        self.base_elements = BaseElements(driver=self.driver)

    @property
    def open_page(self):
        self.driver.set_page_load_timeout(3)  # to avoid long page loading
        try:
            self.driver.get(self.url)
        except TimeoutException:
            self.driver.execute_script("window.stop();")

    def get_cmd_output(self, command: str, splitter: str = None, column_idx: int = 1) -> str:
        """
        Run a given command and return its output response
        :param command: linux command to be executed
        :param splitter: char to be used for slicing output data
        :param column_idx: column number to be used for slicing output data
        :return: command's output data of a string type
        """
        lines_start = set(
            item.text for item in self.base_elements.find_elements(By.XPATH, "//*[@class='ace_line_group']"))
        if self.send_command(command):
            res = set(
                item.text.lstrip() for item in
                self.base_elements.find_elements(By.XPATH, "//*[@class='ace_line_group']") if
                not all((item.text.startswith('$'), item.text)))
            command_res = res.difference(lines_start)
            if splitter:
                return ';  '.join(re.sub(' +', ' ', item).split(splitter)[column_idx] for item in command_res)
            else:
                return ';  '.join(command_res)

    def get_pages_output(self, command: str) -> str:
        """
        Run a given command and return its output response which spans several pages
        :param command: linux command to be executed
        :return: command's output data of a string type
        """
        cmd_out = set()
        text_area = self.driver.find_element(By.XPATH, "//div[@id='terminal']/textarea")
        lines_start = set(
            item.text for item in self.base_elements.find_elements(By.XPATH, "//*[@class='ace_line_group']"))
        if self.send_command(command):
            while self.driver.find_element(By.XPATH, "//*[@class='ace_layer ace_text-layer']").location.get('y') < 0:
                ace_line_group = self.base_elements.find_elements(By.XPATH, "//*[@class='ace_line_group']")
                for line in ace_line_group:
                    line_content = line.text
                    if all((not line_content.startswith('$'), line_content)):
                        cmd_out.add(line_content)
                text_area.send_keys(Keys.PAGE_UP)
            text_area.send_keys(Keys.CONTROL, Keys.END)
            self.wait_for_prompt()
            return cmd_out.difference(lines_start)

    def send_command(self, command: str) -> bool:
        """
        Run a command and wait for the prompt to come back
        :param command: command string
        :return: True if the prompt available (False if not)
        """
        text_area = self.driver.find_element(By.XPATH, "//div[@id='terminal']/textarea")
        text_area.send_keys(command)
        text_area.send_keys(Keys.RETURN)
        return self.wait_for_prompt()

    def wait_for_prompt(self, prompt_char: str = '$', prompt_timeout: int = 6) -> bool:
        """
        Wait for the prompt to come back
        :param prompt_char: prompt char to refer
        :param prompt_timeout: time to wait
        :return: True if the prompt available (False if not)
        """
        start_time = time.time()
        while time.time() - start_time <= prompt_timeout:
            text = self.driver.find_element(By.XPATH, "//div[@id='terminal']").text.rstrip()
            prompt = text.splitlines()[-1]
            if prompt == prompt_char:
                return True
            time.sleep(1)
        return False

    @classmethod
    def clean_data(cls, data: dict) -> dict:
        """
        Removes duplicate quotation marks and pipes to make data more readable and valid to be used
        :param data:
        :return:
        """
        for key, val in data.items():
            tmp_lst = []
            if isinstance(val, list):
                for item in val:
                    temp = re.sub(r"[`|]", "", item).strip(' ')
                    tmp_lst.append(temp)
                data[key] = tmp_lst
            if isinstance(val, str):
                data[key] = data[key].replace('\"', '')
        return data

    @property
    def client_tear_down(self):
        self.tear_down

