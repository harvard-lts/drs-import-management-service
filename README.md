# import-management-service

Import Management Service (IMS) is a Python/Flask project written in Python 3.

## Development environment setup

IMS is intended to be executed in a Docker container, so it has its own Docker Image, which is defined within this repository in a Dockerfile.

To run an IMS development container on the local machine, there are two supported options: do it using the docker-compose file available in the repository or using Docker commands.

### Run using docker-compose

Note that for this option docker-compose must be installed.

Execute docker-compose up command:
````
docker-compose up
````

### Run using Docker commands

First, build IMS Docker image:
````
docker build --tag ims .
````

Then, execute Docker run command:
````
docker run -p 5000:5000 -e ENV_CONFIG='development' -e FLASK_DEBUG=1 -v "$(pwd)"/app/:/home/imsuser/app ims
````

Remember to add the above run command options to set the right environment config and allow automatic updating of code changes in the running container.

## Versioning

This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
