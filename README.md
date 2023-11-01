# Email Index Service
![](https://i.imgur.com/huxtR0i.png)


This Email Index Service is a REST HTTP web service modularized into several layers and components. 

1. At the front is a FastAPI endpoint (/v1/emails) that provides an API for ingesting and searching for/retrieving ingested emails. The API layer is responsible for only validating requests and validing and serializing responses and errors. Pydantic is used for the majority of the request data definitions and validation. The API layer forwards the rest of the work to the Service layer.
2. The Service layer is responsible for performing business logic, such as parsing, sanitizing, and transforming email request data so that it can be optimized for search and packaged for storing.
3. The Repository layer serves as an intermediary between the domain/business objects of the Service layer, and the mapping of that domain data for storage. It allows us to swap between data persistence solutions as well as ORM's. Here, we're using PeeWee ORM because it is lighter weight than ORM's such as SQLAlchemy & Django's.
4. For storage, we're using a SQLite database. We have a many-to-many table for carbon copies of emails, so that we can reduce the amount of duplicate emails to scan.

The code can be considered fairly self-describing due to the limited complexity of the project, so the amount of comments provided is also limited. I understand that comment usage will vary based on the culture of a team/project and can be adaptable depending on what the needs are.

Languages: Python 3.11.0
Dependency Management: Poetry
Testing: pytest
Storage: SQLite3
Containerzation: Docker

To run as a container:
```sh
docker build -t email-index-service .
docker run -p 8000:8080 email-index-service
```
To bootstrap the service with test data:
```sh
docker ps
docker exec -it <container_id_or_name> sh
python bootstrap.py
```
You can access a GUI for importing and retrieving emails at http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc
![](https://i.imgur.com/LKMwq7X.png)
![](https://i.imgur.com/Qg5qg4D.png)

Things missing from this project that would otherwise be considered important for best-practices:

* Logging
* Error Handling
* Migrations for data definitions
* Config management
* Paginating query results
* More defined constraints for DB field definitions and request schema validation
