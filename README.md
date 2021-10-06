#Elastic search demo
This project is responsive web application on Flask framework and elastic search

## Project Stack

1. Python
2. Flask
3. Elastic search
4. Docker

## Steps for setup using Docker

### Install Docker

Please follow below links to install Docker Enginer/Docker Desktop on your respective environment

- [MacOS](https://docs.docker.com/desktop/mac/install/)
- [Linux](https://docs.docker.com/engine/install/ubuntu/)
- [Windows](https://docs.docker.com/desktop/windows/install/)

### Running Docker Compose Services

Note:

- Change .env.example to .env, and make the required config changes

- Build project by running next command: 
> `docker-compose build` 
- Start project by running next command: 
> `docker-compose up -d` 
- Build and up container in one command: 
> `docker-compose up --build -d`		

The server runs at `http://localhost:5000`
elastic search server runs at: `http://localhost:9200`

## Local Installation Steps

If you are not using docker then please refer local_setup.md to setup the project
