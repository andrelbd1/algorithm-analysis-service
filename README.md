# Algorithm Analysis Service
[![GitHub last commit](https://img.shields.io/github/last-commit/andrelbd1/algorithm-analysis-service.svg)](https://github.com/andrelbd1/algorithm-analysis-service) 
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/andrelbd1/algorithm-analysis-service.svg)](https://github.com/andrelbd1/algorithm-analysis-service) 

## Overview
This project serves as a sandbox for experimenting with and evaluating various algorithms and development tools.

It features a RESTful API that enables users to execute algorithms and analyze essential performance metrics, including `runtime`, `memory consumption`, `node and edge counts`, and `cycle detection`.

## Prerequisites
- Python 3.12.6
- Required dependencies (see `requirements.txt`)

### Run cover test
```sh
    py.test --cov=src tests
```

## Installation
Clone the repository and start application:
```bash
   git clone https://github.com/andrelbd1/algorithm-analysis-service.git
   cd algorithm-analysis-service
   docker compose up
```

## Usage

Once the application is running, you can access the interactive API documentation via Swagger UI:

[http://localhost:8001/doc#/](http://localhost:8001/doc#/)

Use this interface to explore available endpoints, execute requests, and review responses directly from your browser.

![alt text](assets/swagger.png)

### Endpoints

The following endpoints are available in this project:

- **GET /healthcheck**  
    Returns the health status of the service.

- **DELETE v1/algorithm/{algorithm_id}**  
    Deletes the algorithm identified by the specified `algorithm_id`.

- **GET v1/algorithm/list**  
    Retrieves a list of available algorithms.


## Project Structure
```
.
├── main.py                             # Entry point for executing tasks
├── migrations/                         # 
│   ├── versions/                       # 
│   ├── env.py                          # 
├── src/                                # Source code directory
│   ├── api/                            # 
│   │   ├── v1/                         # 
│   │   │   ├── swagger/                # 
│   │   │   │   ├── __init__.py         # Module initializer
│   │   │   │   ├── algorithm.py        # 
│   │   │   │   ├── execution.py        # 
│   │   │   ├── __init__.py             # Module initializer
│   │   │   ├── algorithm.py            # 
│   │   │   ├── execution.py            # 
│   │   ├── __init__.py                 # 
│   │   ├── healthcheck.py              # 
│   ├── codes/                          # 
│   │   ├── dijkstra/                   # 
│   │   ├── factorial/                  # 
│   │   ├── fibonacci/                  # 
│   │   ├── __init__.py                 # 
│   │   ├── base.py                     # 
│   ├── common/                         # Common utilities and helper functions
│   │   ├── __init__.py                 # Module initializer
│   │   ├── functions.py                # Common helper functions
│   ├── controllers/                    # Business logic for processing tasks
│   │   ├── __init__.py                 # Module initializer
│   │   ├── algorithm.py                # 
│   │   ├── criteria.py                 # 
│   │   ├── execution.py                # 
│   │   ├── input.py                    # 
│   │   ├── payload.py                  # 
│   │   ├── result.py                   # 
│   ├── evaluation/                     # 
│   │   ├── count_edges/                # 
│   │   ├── count_nodes/                # 
│   │   ├── detect_cycle/               # 
│   │   ├── memory_consume/             # 
│   │   ├── running_time/               # 
│   │   ├── __init__.py                 # Module initializer
│   │   ├── base.py                     # 
│   ├── external_services/              # External service integrations
│   │   ├── __init__.py                 # Module initializer
│   │   ├── aws_interface.py            # AWS service interactions
│   ├── internal_services/              # Internal service integrations
│   │   ├── __init__.py                 # Module initializer
│   │   ├── app_request.py              # 
│   │   ├── app_ulid.py                 # 
│   ├── logs/                           # 
│   │   ├── formats/                    # 
│   │   ├── __init__.py                 # Module initializer
│   │   ├── handler_service.py          # 
│   │   ├── service_logger.py           # 
│   ├── models/                         # 
│   │   ├── __init__.py                 # Module initializer
│   │   ├── base.py                     # 
│   │   ├── orm.py                      # 
│   │   ├── src_orm.py                  # 
│   │   ├── src_orm.py                  # 
│   │   ├── tb_algorithm_criteria.py    #
│   │   ├── tb_algorithm.py             #
│   │   ├── tb_criteria.py              #
│   │   ├── tb_execution.py             #
│   │   ├── tb_input.py                 #
│   │   ├── tb_payload.py               #
│   │   ├── tb_result.py                #
│   ├── tasks/                          # Task management directory
│   │   ├── __init__.py                 # Celery task configuration
│   │   ├── execution.py                # 
│   ├── __init__.py                     # 
│   ├── config.py                       # Application configurations
│   ├── exceptions.py
│   ├── routes.py
│   ├── server.py
├── tests/                              # Unit tests for the application
├── alembic.ini                         # 
├── docker-compose.yml                  # 
├── Dockerfile                          # Docker configuration
├── requirements.txt                    # Dependencies list
├── requirements-dev.txt                # Dependencies list to development
├── README.md                           # Documentation
├── run-redis.sh                        # Script to start a local queue using redis
```


## ER Diagram
![alt text](assets/ER_Diagram.png)
