# drs-import-management-service

DRS Import Management Service (DIMS) is a Python/Flask project written in Python 3.

## Development environment setup

### Create .env file

Create an .env file by copying the existing .env.example file from the repository.

### Run development environment

DIMS is intended to be executed in a Docker container, so it has its own Docker Image, which is defined within this repository in a Dockerfile.

To run an DIMS development container on the local machine, there are two supported options: do it using the docker-compose file available in the repository or using Docker commands.

#### Run using docker-compose

Note that for this option docker-compose must be installed.

Execute docker-compose up command:
````
docker-compose up
````

#### Run using Docker commands

First, build DIMS Docker image:
````
docker build --tag dims .
````

Then, execute Docker run command:
````
docker run -p 13880:5000 -v "$(pwd)"/app/:/home/imsuser/app dims
````

Remember to add the above run command environment variable and volume mapping to allow automatic updating of code changes in the running container.

## Versioning

This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
