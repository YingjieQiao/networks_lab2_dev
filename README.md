# Networks Lab 2

Qiao Yingjie

1004514

TODO:

1. docker script
2. offset queries
3. etc

## Setup

Using FastAPI and PostgreSQL.

### To run the API server locally

run the following:

```bash

```
using a cusomized script instead of `uvicorn app.main:app --reload` to populate the tables with some initial rows.


### checkoff

The checkoff deliverables can be observed in the terminal by running ``.

Alternatively, you can refer to which endpoint correspond to which checkoff deliverable with my comments in the checkoff section.



### if you want to create your own table...

```
psql networks_lab2
CREATE ROLE networks_lab2_user WITH LOGIN PASSWORD '123456';
ALTER ROLE networks_lab2_user CREATEDB;
\q
psql networks_lab2 -U networks_lab2_user
```

## API endpoints

| endpoint   | description        | Success  |  Failure  | Remarks  |
| --- | --- | --- | --- | --- |
| GET `heartbeat` | returns a string "The connection is up" | 200 if success |  --- | --- |
| POST `/course` | creates a new `Course` in the table `Course` |  200 if successfully created | 400 if already exists | --- |
| POST `/student` | creates a new `Student` in the table `Student` |200 if successfully created | 400 if already exists | --- |
| GET `course_all` | returns all rows in table `Course` | 200 if success | 500 for unexpected server side errors | --- |
 | GET `student_all` | returns all rows in table `Student` | 200 if success | 500 for unexpected server side errors | --- |
| GET `/course/{course_id}` | get a new `Course` in the table `Course` given a `course_id` | 200 if successfully retrieved | 404 if not found | --- |
| GET `/student/{student_id}` | get a new `Student` in the table `Student` given a `student_id` |200 if successfully retrieved | 404 if not found | --- |


## Checkoff Requirements

- A REST-over-HTTP API written in any programming language, in any framework, to imitate any real life service (e.g. fake myportal, fake edimension), backed with any other supporting services (redis, mysql, etc):
    - Can be deployed on any docker host using `docker compose` - you fail if I need to install any other dependencies on my computer!
- With accompanying `.http` unit test files, showcasing your API's ability to respond to:
    - a GET request ...
        - with no query parameters
            - see GET `heartbeat`, GET `course_all` and GET `student_all` (db optional query param ok ??? gist link)
        - with a `sortBy` query parameter, to transform the order of the items returned
            - up to you to decide what attributes can be sorted
        - with a `count` query parameter, to limit the number of items returned
        - with a `offset` query parameter, to "skip" ahead by a number of items
        - with any combination of the above query parameters
    - a POST request ...
        - that creates a new resource with the given attributes in the body
            - see POST `/course`, POST `/student`, to create with scheme
            - see POST `/course`, POST `/student`, to create with attributes
            - schema vs attributes ?
        - show that the resource has indeed been created through another HTTP request
            - see GET `/course/{course_id}`, GET `/student/{student_id}`
        - has validation and returns an appropriate HTTP response code if the input data is invalid (e.g. missing name)
            - see `xxx` ???
    - either a DELETE or PUT request...
        - that deletes or updates a _single_ resource respectively
        - show that the resource has indeed been modified through another HTTP request 
        = has validation and returns an appropiate HTTP response code if the input data is invalid 
        (e.g. trying to delete a nonexistent user)
- Identify which routes in your application are _idempotent_, and provide proof to support your answer.
- Implement at least two of the following challenges:
    - File upload in a POST request, using multipart/form-data
    - Have a route in your application that returns a content type that is not _plaintext_
    - Some form of authorization through inspecting the request headers
    - A special route that can perform a batch delete or update of resources matching a certain condition

> You must provide ample documentation on how to build & run your code and how to make the HTTP requests to your API, 
>as well as what are the expected responses for each request. 
>You will not be deducted if your program is slow or unoptimised, 
>but bonus points may be given if you show meaningful thought in analysing how performance was / can be improved 
>in your application.