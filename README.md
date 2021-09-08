# Mcmaster Student Services Spam Bot

Refreshes page and resends request to speak with SSP upon receiving the message: "We apologize but we are currently experiencing higher than normal chat volume. To avoid lengthy wait times in the queue, we ask you to try connecting with us at a later time.  Thank you."
## Description

Script creates a browser instance where interaction with MAC bot is handled through Selenium. Since the form and chat are generated asynchronously, the code is only possible through a combination "sleep" and "WebDriverWait" functions which are not guarenteed to work if the response times exceed the sleep times; if you are encountering consistent timeout errors, increase the length of these sleep functions accordingly. 

If you want to enable email notifications in order to receive status updates, follow the directions outlined in the py-mail submodule.

## Getting Started

### Dependencies

* python 3
* pip
* geckodriver

### Installing

* Install [Geckodriver](https://github.com/mozilla/geckodriver/releases) and ensure that the  ./geckodriver executable is located somewhere in your system $PATH
* Install pip for python 3
* (recommended) Create Python [Virtual Environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) to locally install dependencies and run code --- on Unix-like OS, run
```
python3 -m venv env
source env/bin/activate
```
* From within virtual environment, install  dependencies with:
```
(env)[user@host]$ pip install -r requirements.txt
```

### Executing program

* Fill out your student information for the form fields in form_fields.yaml.
* Start program with 
```
python main.py
```
* Close program with Ctrl+C

## Help

Any advise for common problems or issues.


## License

This project is licensed under the MIT License - see the LICENSE file for details