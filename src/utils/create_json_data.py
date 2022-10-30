import json
from selenium.webdriver.common.by import By


def create_json_data(tests_client, tests_data):
    target_file = tests_data.target_file
    tests_client.base_elements.find(By.XPATH, "//div[@id='terminal']", expected_condition='clickable')
    tests_client.base_elements.find(By.XPATH, "//div[@id='terminal']").click()
    os_name = tests_client.get_cmd_output("grep -i ^name= /etc/*release", splitter='=')
    os_version = tests_client.get_cmd_output("grep -i ^version= /etc/*release", splitter='=')
    cpu_model = tests_client.get_cmd_output("grep -m1 'model name' /proc/cpuinfo", splitter=':')
    disk_type = tests_client.get_cmd_output("lsblk -d -o NAME | tail -1")
    disks = tests_client.get_cmd_output(F"lsblk | grep -i {disk_type}")
    last_login = tests_client.get_cmd_output("last -R --time-format iso | head -1", splitter=' ', column_idx=2)
    current_date = tests_client.get_cmd_output('date +"%Y-%m-%dT%H:%M:%S%:z"', splitter=' ', column_idx=0)
    free_ram = tests_client.get_cmd_output('free -h | tail -2 | head -1', splitter=' ', column_idx=2)
    pci_data = tests_client.get_pages_output("lspci -nn")
    pci_data_dict = {item.split()[0] : ' '.join(item.split()[1:]) for item in pci_data}
    data = {'Linux type': os_name, 'Linux ver.': os_version, 'cpu model': cpu_model, 'disk_type': disk_type,
            'available_disks': disks.split(';'), 'pci_data': pci_data_dict, 'last_login': last_login,
            'current_date': current_date, 'free_ram': free_ram}
    cleaned_data = tests_client.clean_data(data)
    with open(target_file, 'w+') as f:
        f.write(json.dumps(cleaned_data, indent=3))

