Data driven applications project
===

Kajaani UAS practice project

2023


# Development

## Requirements

Python 3.8.10 https://www.python.org/downloads/

Docker https://docs.docker.com/get-docker/

Poetry https://python-poetry.org/docs/

Node.JS and NPM https://docs.npmjs.com/downloading-and-installing-node-js-and-npm


## Installation

1. Clone repository

2. (optional) Create and activate Python virtual environment: https://docs.python.org/3/library/venv.html

3. Install Python dependencies: 

```
poetry install
```

4. Install frontend packages:

```
cd frontend

npm install
```


## Poetry package management

Add new dependency: 

```
poetry add <package name>==<version>
```

Add new dev dependency: 

```
poetry add <package name>==<version> -G dev
```


## Unit tests

Running tests from command line:

```
python -m pytest tests
```

Tests can be also run from tests.ipynb notebook with VS Code debugger. Some tests can take up to two minutes because of importing issues. Running from a notebook makes testing and development much faster.

# Scripts

## Starting the services locally for development

1. Start backend to run backend as Python script (terminal 1) (activate Virtualenv before, if created): 

    ```
    ./dev_run_backend_locally.sh
    ```

Backend will reload on code changes.


2. Start MongoDB database as a Docker container (terminal 2): 

    ```
    ./dev_mongodb_docker_start.sh
    ```

To reinstate database, delete 'mongodbdata' folder locally and run the script again.

File 'mongo-init.sh' is used to create MongoDB user.


3. Start frontend React application (terminal 3): 

    ```
    cd frontend
    npm run start
    ```

Web application opens on http://localhost:3000

Frontend will reload on code changes.

## Starting the services in locally

Start backend, MongoDB and frontend in Docker containers

```
./dev_build_and_start_services.sh
```

Web application opens on http://localhost:3000

## Creating production builds locally

1. Build and start backend and frontend production builds (terminal 1):

    ```
    ./prod_build_and_start_services.sh
    ```



2. Start MongoDB database as a Docker container (terminal 2):

    ```
    ./dev_mongodb_docker_start.sh
    ```


## Pushing images to personal Docker Hub

1. Create my_env.env file and add line:

    ```
    REPOSITORY=<your Docker Hub repository>
    ```

2. Run push script

    ```
    ./prod_push_images.sh
    ```




# Known issues

- After starting the service locally for development, the first prediction can take up to 2 minutes.
- Running unit tests can be quite slow. Recommended to run from tests.ipynb while developing.


# Authors

Hannu Karstu

Pose estimation related stuff by Tensorflow team


# Licence

Open for all use
