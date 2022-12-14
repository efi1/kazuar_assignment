=================
Kazuar Assignment
=================

This assignment validating various data of Linux (Fedora) OS.

First It collects various system information using Selenium webdriver and saves it into a json file.

Then it uses this information to check its validity.


Usage:

- Run "python setup.py install" (run it first)

- It is recommended to use a virtual env.

- All testing variables resides in settings.py under the tests folder.
they can be updated directly at the settings.py or can alternatively used by the command line as flags.

e.g. python -m pytest --url <url address>

- If not using a flag for a certain variable it will be taken from the setting.py

- There are two parameterized tests - "test_cat_options1", "test_cat_options2".
They have the same functionality, but implemented differently.

- As the parameterized tests take relatively long time to run, you might want to avoid (deselect) running it at the beginning.
  you might use for that the configured pytest marker slow (e.g. python -m pytest -m "not slow").


- Under src.clients you may find the tests_client.py which include all main activities for creating the json data files as well
for performing the tests. Other available clients are secondary in use and they support the Selenium webdriver activities.


 - The products of section 1 and 2 in the assignment's instructions are being generated by src.utils.create_json_data.py which is 
called by the conftest.py . All data are saved in data.json file under the target folder.

- The data.json data are being used in test_logon_period and test_is_sata.


- Test execution will write into a log file logfile.log (under tests folder) as well it prints the running log to the console.
log level can be changed within the pytest.ini file.


- Another last issue - in regard section 1.c. , the disk is nvme0n1 (not SATA), therefore its elements description are also absence.
Nevertheless, I did add disk's nvme0n1 information in the data.json file.
