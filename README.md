# Python Developer Home Assignment

#### OpenAPI/Swagger Specification:
Provide a detailed specification of the API in OpenAPI/Swagger format - /docs or /redoc

#### Python Web Framework:
Implement the solution using fastAPI microframework

#### Test Data:
test_data.csv test file is in the project's root


#### Setup:

##### Create .env file:
	cp sample_env .env

##### Run in project root directory:
	docker-compose up -d

##### Fow run all unit tests:
    docker exec -it backend pytest

##### Fow run particular unit tests:
    docker exec -it backend pytest -k test_name

##### Fow get coverage report run:
    docker exec -it backend coverage run -m pytest
    docker exec -it backend coverage report -m
