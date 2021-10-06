# Installation for local setup without Docker

## Install Python 3.8 & Pip

Linux -

> `sudo apt-get update`
> `sudo apt-get install python3.8`

Windows-

Download Python 3.8 from <https://www.python.org/downloads/> and install

### Install Virtualenv

> `pip install virtualenv`</br>
> `Set enviornment path for python, pip and virtualenv`

### Create and activate a virtualenv for the project

> `virtualenv venv`

Windows-

> `venv\Scripts\activate`

Linux-

>`source venv/bin/activate`

You should see `(venv)` added to the beginning of your Terminal input line, which indicates that the virtualenv is active.

The virtualenv must be activated during development.

### Install Requirements

Install the Python requirements for the project

> `pip install -r requirements.txt`


### Change environment variables

- Change .env.example to .env, and make the required config changes and please change HOST_NAME value to localhost

### Populate db 
Open data_populate.txt and populate data by running curl commands

### Run Consumer Search

> `python app.py`

The server runs at `http://localhost:5000`
elastic search server runs at: `http://localhost:9200`