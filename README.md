# drs-import-management-service

DRS Import Management Service (DIMS) is a Python/Flask project written in Python 3.

## Development environment setup

### Create .env file

Create an .env file by copying the existing env.example file from the repository.

### Run development environment

DIMS is intended to be executed in a Docker container, so it has its own Docker Image, which is defined within this repository in a Dockerfile.

To run a DIMS development container on the local machine, there are two supported options: do it using docker-compose-dev.yml file available in the repository, or using Docker commands.

By using docker-compose-dev.yml, docker-compose will also bring up an ActiveMQ development container. If you want to use a remote MQ, all you have to do is to update the corresponding MQ environment variables in the .env file to access the desired MQ.

#### Run using docker-compose

Note that for this option docker-compose must be installed.

Execute docker-compose up command:
````
docker-compose -f docker-compose-dev.yml up
````

#### Run using Docker commands

Note that this option will only run a DIMS container, without any dependent services.

First, build DIMS Docker image:
````
docker build --tag dims .
````

Then, execute Docker run command:
````
docker run -p 13880:5000 -v "$(pwd)"/app/:/home/dimsuser/app dims
````

Remember to add the above run command environment variable and volume mapping to allow automatic updating of code changes in the running container.

## Test environment setup

### Create .test.env file

First, a .test.env file must be created inside /test/integration by copying the existing .test.env.example file which can be found in the same folder.

### Run test environment

Similar to the development environment, for running a local integration test environment there is a docker-compose-test.yml file, which only contains an ActiveMQ service, as it is currently the only external DIMS dependency.

Before executing the integration tests locally, the environment must be up and running:
````
docker-compose -f docker-compose-test.yml up
````

If you want to use a remote test environment for integration testing, you will need to update the environment variables in the .test.env file to access the desired environment.

## Versioning

This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
