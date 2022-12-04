# Simple FastAPI service

Minimal reproducible example to showcase [Issue #1624](https://github.com/tiangolo/fastapi/issues/1624)
> The memory usage piles up over the time and leads to OOM

## Requirements

* Python 3.10.8
* Poetry
* Docker

## Setup

* building the wheel within a py 3.10 docker container  
  (Note: you can skip this step, wheel available in repo)
    ```bash
    docker run --rm -v $PWD:/repo -w /repo -it python:3.10 bash
    pip install poetry==1.2.2
    poetry build -f wheel
    ```
* building the docker image
    ```bash
    docker build -t simple_api .
    ```
* starting up the container
    ```bash
    docker run --rm -p 8080:8080 --name simple_api simple_api
    ```
* keep an eye on docker memory usage
    ```bash
    docker stats
    ```
* send random sized requests to the service
    * only valid input
        ```bash
        ./send_ok_requests.sh
        ```
    * mixed valid and invalid input
        ```bash
        ./send_mixed_requests.sh
        ```

Note: the memory increase is most visible on invalid requests

## Rule out other possible culprits

### Check only the logic + pydantic validation

* building the docker image
    ```bash
    docker build -f Dockerfile.check_validation -t simple_api_check_validation .
    ```
* starting up the container
    ```bash
    docker run --rm --name simple_api_check_validation simple_api_check_validation
    ```
* keep an eye on docker memory usage
    ```bash
    docker stats
    ```

Note: don't see any change here

### Check only the api without uvicorn server

* building the docker image
    ```bash
    docker build -f Dockerfile.check_client -t simple_api_check_client .
    ```
* starting up the container
    ```bash
    docker run --rm --name simple_api_check_client simple_api_check_client
    ```
* keep an eye on docker memory usage
    ```bash
    docker stats
    ```

Note: 
* still see the memory increase here
* trying to kill the interactive container with CTRL+C will keep generating new PIDs, stop it with `docker stop <container_id>`

### Check the api with hypercorn server

* building the docker image
    ```bash
    docker build -f Dockerfile.hypercorn -t simple_api_hypercorn .
    ```
* starting up the container
    ```bash
    docker run --rm --name simple_api_hypercorn simple_api_hypercorn
    ```
* keep an eye on docker memory usage
    ```bash
    docker stats
    ```
* send random sized requests to the service
    ```bash
    ./send_mixed_requests.sh &
    # wait a few minutes
    ./send_mixed_requests.sh "ceci est un texte aléatoire. " &
    # wait a few minutes
    ./send_mixed_requests.sh "Dies ist ein Zufallstext." &
    ```

Sample grafana panel
![grafana_simple_api_hypercorn.png](grafana_simple_api_hypercorn.png)

## Track memory increse over time

* starting the server
    ```bash
    docker run --rm -p 8080:8080 -v $PWD:/repo -w /repo -it python:3.10 bash
    pip install dist/*.whl
    pip install memory_profiler
    pip install hypercorn
    mprof run hypercorn --bind 0.0.0.0:8080 simple_api.app:app
    ```
* send random sized requests to the service
    ```bash
    ./send_mixed_requests.sh &
    # wait a few minutes
    ./send_mixed_requests.sh "ceci est un texte aléatoire. " &
    # wait a few minutes
    ./send_mixed_requests.sh "Dies ist ein Zufallstext." &
    ```
* stop the server and plot the memory increase
    ```bash
    mprof plot
    ```

Sample plot: ![mprof_plot_hypercorn.png](mprof_plot_hypercorn.png)