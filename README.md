# proxy-parser-api
Simple project with independent parser and API for getting results

## Setting up

Defore building you may need to rename *.env.dist* to *.env* and replace sample values in it (database password etc.) with real values. 

In order to run the service docker and docker-compose are required. 
To run the service with docker-compose:
```bash
docker-compose up --build
```

## API guide

Sample request (giving the service is running at localhost port 8000): 
```
localhost:8000/posts?sort=title&order=desc&limit=3&offset=5
```
Sample result:
```json
[
    {
        "created": "Tue, 12 Nov 2019 15:48:10 GMT",
        "id": 22,
        "title": "Why was it believed that the Aztecs greeted Cortés as a deity?",
        "url": "https://www.laphamsquarterly.org/roundtable/inventing-god"
    },
    ...
]
```
Supported arguments are:
```python
{
        "sort": {
            "type": "nominal",
            "values": ["id", "title"],
            "default": "id",
        },
        "order": {
            "type": "nominal",
            "values": ["asc", "desc"],
            "default": "asc",
        },
        "offset": {
            "type": "interval",
            "values": (0, 100),
            "default": 0,
        },
        "limit": {
            "type": "interval",
            "values": (0, 1000),
            "default": 5,
        },
        "update": {
            "type": "nominal",
            "values": ["sync", "async", "none"],
            "default": "none",
        }
    }
```
**sort**, **order**, **limit** and **offset** arguments affect how the server queries the database.

**update** argument works differently. If update is set to *sync*, 
server fetches all new data from the target url before executing query.
Thus, request may take much longer, but new data may be returned right away. 
If update is set to *async*, 
server issues a request for update and immediatly returns confirmation message (without returning any posts). 
In several seconds (depending on network and other conditions) data will be updated. 

## Working app

Working version of the app can be found here: [http://185.251.88.239:8000/posts](http://185.251.88.239:8000/posts) 
It will remain active until 01.12.2019.

## Testing 

Tests can be executed locally or in container. To run in container, use the following command:
```bash
docker-compose -f docker-compose.test.yml up --build && docker-compose -f docker-compose.test.yml down
```
Tests may not pass on the first execution because some time is needed for database, queue and workers to get ready. If this is the case, just wait for few seconds, tests container will be restarted.

To execute tests locally you will need to install all dependancies from Pipfile, run all the services with docker-compose or manualy and run tests with pytest. 
