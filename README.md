# drs-import-management-service

DRS Import Management Service (DIMS) is a Python/Flask project written in Python 3.

## Local setup
    
1. Make a copy of the env.example to .env and modify the user and password variables.

2. Start the container
    
```
docker-compose -f docker-compose-local.yml up -d --build --force-recreate
```

## Testing
Note, testing uses its own queues so they will not interfere with the queues used by the actual program.

1. Start the container up as described in the <b>Local Setup</b> instructions.

2. Exec into the container:

```
docker exec -it dims bash
```

3. Run the tests

```
pytest
```

## Invoking the task manually

### invoke-task.py (add message to the DIMS queue)

- Clone this repo from github 

- Create the .env from the env-example and replace with proper values (use LPE Shared-DAIS for passwords)

- Start up docker  

`docker-compose -f docker-compose-local.yml up --build -d --force-recreate`

- Exec into the docker container

`docker exec -it dims bash`

- Run invoke task python script

`python3 scripts/invoke-task.py`

- Bring up [DEV DAIS Rabbit UI](https://b-e9f45d5f-039d-4226-b5df-1a776c736346.mq.us-east-1.amazonaws.com/)  - credentials in LPE Shared-DAIS

- Look for the queue with `-dryrun` (eg `dims-data-ready-dryrun`) appended to its name and verify a message made it

### invoke-dlq-task.py (add message that will be rejected to the queue)

- Clone this repo from github 

- Create the .env from the env-template.txt and replace with proper values (use LPE Shared-DAIS for passwords)

- Start up docker  

`docker-compose -f docker-compose-local.yml up --build -d --force-recreate`

- Exec into the docker container

`docker exec -it dims bash`

- Run invoke task python script

`python3 scripts/invoke-dlq-task.py`

- Bring up [DEV DAIS Rabbit UI](https://b-e9f45d5f-039d-4226-b5df-1a776c736346.mq.us-east-1.amazonaws.com/)  - credentials in LPE Shared-DAIS

- Look for the DLQ queue that you named in your .env (eg `dais-dead-letter-queue-dd`) verify the message lands here


## Versioning

This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## DLX/DLQ

The DAIS services use a dead letter queue to collect messages that were rejected after a configurable amount of retries.  Information on the DLX/DLQ setup and use can be found on this [LTS internal wiki](https://wiki.harvard.edu/confluence/pages/viewpage.action?pageId=337150659).
