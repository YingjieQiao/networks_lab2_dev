# Networks Lab 2

Qiao Yingjie

1004514

TODO:

1. docker script
2. validate post body
3. do the tests in docker and check the stdout and id for the get endpoints

## Setup

Using FastAPI and PostgreSQL. This implements a student - course system where each course could enroll multiple students, but
a student can have at most 1 course. (see a command-line illustration of the one-to-many relationship [here](one2many.md)),
and a gallery to showcase some beautiful images.

### Run the API server locally

run the following:

```bash
docker-compose build
docker-compose up
```


when you terminate the container, run

```bash
docker-compose down --volumes
```


### if you want to create your own table...

```
psql networks_lab2
CREATE ROLE networks_lab2_user WITH LOGIN PASSWORD '123456';
ALTER ROLE networks_lab2_user CREATEDB;
\q
psql networks_lab2 -U networks_lab2_user
```


## Checkoff Requirements


- A REST-over-HTTP API written in any programming language, in any framework, to imitate any real life service (e.g. fake myportal, fake edimension), backed with any other supporting services (redis, mysql, etc):
    - Can be deployed on any docker host using `docker compose` - you fail if I need to install any other dependencies on my computer!
        - see the [Run the API server locally](#run-the-api-server-locally) section above. 
        - In short, run `docker-compose up` at project root folder, and then attach to the FastAPI container.
  
**IMPORTANT**: 

please run `python init_test.py` to populate the tables with some initial rows, so that 
the `GET` endpoints could work.


Running the tests with `pytest testfile.py::test_function -s`, with `-s` to capture stdout in terminal:

With accompanying `pytest` unit test files, showcasing your API's ability to respond to:


- a GET request ...
    - with no query parameters
        - GET `/course` and GET `/student`
        ```bash
        pytest tests/test_get.py::test_get_student_all -s
        pytest tests/test_get.py::test_get_course_all -s
        ```
    - with a `sortBy` query parameter, to transform the order of the items returned
        - GET `/student?sort_by=gpa`
        ```bash
        pytest tests/test_get.py::test_get_student_sort_by -s
        ```
    - with a `count` query parameter, to limit the number of items returned
        - GET `/student?count=3`
        ```bash
        pytest tests/test_get.py::test_get_student_count -s
        ```
    - with a `offset` query parameter, to "skip" ahead by a number of items
        - GET `/student?offset=3`
        ```bash
        pytest tests/test_get.py::test_get_student_offset -s
        ```
    - with any combination of the above query parameters
        - GET `/student?sort_by=gpa&count=5`
        ```bash
        pytest tests/test_get.py::test_get_student_limit_sort_by -s
        ```

- a POST request ...
    - that creates a new resource with the given attributes in the body
        - POST `/course`, POST `/student`
        - make valid requests: 
        ```bash
        pytest tests/test_create.py::test_create_student_success -s
        pytest tests/test_create.py::test_create_course_success -s
        ```
        - expected stdout:
        ```bash
        later
        ```
      
        - invalid requests: ;ovghawerilurgliaewubhgaowhue
        row already exists
        ```bash
        pytest tests/test_create.py::test_create_student_fail_1 -s
        ```
        bad input TODOTODOTODO `validator`
        ```bash
        pytest tests/test_create.py::test_create_course_fail_1 -s
        ```
        - expected stdout:
        ```bash
        later
        ```

    - show that the resource has indeed been created through another HTTP request
        - GET `/course/{course_name}` and GET `/student/{student_name}`
        - make the requests: 
        ```bash
        pytest tests/test_get.py::test_get_course_by_name -s
        pytest tests/test_get.py::test_get_student_by_name -s
        ```
        expected stdout: 
        
        ```bash                                                                                                                                                                                                                                                                      
        LATERRRR
        tests/test_get.py {"name":"Samwell Tarly","email":"samwell_tarly@sutd.edu","gpa":5.0,"id":10,"course_id":null}
        ```
      
    - has validation and returns an appropriate HTTP response code if the input data is invalid 
    (e.g. missing name)
        - see the invalid requests stated above. TODOTODOTODO
        
- either a DELETE or PUT request...
    - that deletes or updates a _single_ resource respectively
        - DELETE `/course`, DELETE `/student`, PUT `/course/{course_id}/{student_id}`
        
        - make the requests:
        
        ```bash
        pytest tests/test_delete.py::test_delete_course -s
        pytest tests/test_delete.py::test_delete_student -s
        pytest tests/test_put.py::test_single_update -s
        ```
        
        - expected stdout for DELETE:
        ```bash
        tests/test_delete.py {"title":"Discrete Math","description":"sutd doesnt teach","id":4,"enrolled_students":[]}
        
        tests/test_delete.py {"name":"Samwell Tarly","email":"samwell_tarly@sutd.edu","gpa":5.0,"id":10,"course_id":null}

        ```
        
        - expected stdout for PUT:
        ```bash
        tests/test_put.py {"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}
        ```
            
    - show that the resource has indeed been modified through another HTTP request 
        - for the DELETE, use GET `/course/{course_name}`, GET `/student/{student_name}`
        - make the requests:
        ```bash
        pytest tests/test_get.py::test_get_student_by_name_for_delete -s  
        pytest tests/test_get.py::test_get_course_by_name_for_delete -s
        ```
        - expected stdout:
        ```bash
        tests/test_get.py {"detail":"Student not found"}
        tests/test_get.py {"detail":"Course not found"}
        ```
        indicating that they are indeed already deleted from the table.
      
        - for the PUT, use GET `/course/byid/{course_id}`, GET `/student/byid/{student_id}`
        - make the requests:
        ```bash
        pytest tests/test_get.py::test_get_course_by_id -s 
        pytest tests/test_get.py::test_get_course_by_id -s
        ```
        - expected stdout:
        ```bash
        tests/test_get.py {"title":"Intro to Algo","description":"leetcode","id":1,"enrolled_students":[{"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}]}
        tests/test_get.py {"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}
        ```
        We can see that the `Course` with title `Intro to Algo` has a new `Student` added to its `enrolled_students`, 
        and the `course_id` of `Student` is also updated.
        
    - has validation and returns an appropiate HTTP response code if the input data is invalid 
    (e.g. trying to delete a nonexistent user)
        - For the DELETE `/course`, because we have already executed it once previously 
        and there is no `Course` row with `title: Discrete Math` and `description: sutd doesnt teach` 
        and `Student` row with `name: Samwell Tarly` now,
        we can make the DELETE requests again - because these rows do not exist, 
        it will return a `404: Trying to delete nonexistent rows`
        - make the request:
        ```bash
        pytest tests/test_delete.py::test_delete_course_validate -s
        pytest tests/test_delete.py::test_delete_student_validate -s
        ```
        - expected stdout:
        ```bash
        tests/test_delete.py {"detail":"Trying to delete nonexistent rows."}
        tests/test_delete.py {"detail":"Trying to delete nonexistent rows."}
        ```
      
        - For the PUT `/course/{course_id}/{student_id}`, we can validate whether `Student` and `Course` exist in the table
        and raise `404` if not found.
        - make the requests:
        ```bash
        pytest tests/test_put.py::test_single_update_validate_course_not_found -s
        pytest tests/test_put.py::test_single_update_validate_student_not_found -s
        ```
        - expected stdout:
        ```bash
        tests/test_put.py {"detail":"Course not Found."}
        tests/test_put.py {"detail":"Student not Found."}
        ```
    
- Identify which routes in your application are _idempotent_, 
and provide proof to support your answer.
    - `PUT /course/{course_id}/{student_id}` is idempotent: 
    calling it once or several times successively has the same effect (that is no side effect). 
    For example, calling `PUT /course/1/1` will make sure the `Student` with `student_id = 1` 
    is under `Course` with `course_id = 1` and that `Course` with `course_id = 1` 
    will have `Student` with `student_id = 1` in its `enrolled_student` - calling multiple times
    will have the same effect as calling it once. 
    - To prove it, you can make the PUT request `PUT /course/1/1` multiple times:
    ```bash
    pytest tests/test_put.py::test_single_update -s
    pytest tests/test_put.py::test_single_update -s
    pytest tests/test_put.py::test_single_update -s
    pytest tests/test_put.py::test_single_update -s
    ...
    ```
    
    - The stdout is always:
    ```bash
    tests/test_put.py {"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}
    ```
    which is the same result after making the request only once.
    
- Implement at least two of the following challenges:
    - File upload in a POST request, using multipart/form-data
        - POST `/file` - add a new row to table `file` and save the image to a folder on disk `object_store`. 
        returns the path to the file saved localtion on server;
        - make a request:
        ```bash
        pytest tests/test_file.py::test_upload -s
        ```
        - expected stdout: 
        ```bash
        tests/test_file.py "/Users/yingjieqiao/Desktop/term6/networks_labs/networks_lab2/app/object_store/cat.png"
        ```
        
        - A side note: To my knowledge, I think the best way to store large binary assets like image and video is to
        save them to an Object Store service like AWS S3, or a base64 string in the database table (for images), 
        or, save a path to the asset in the database table and keep
        the asset somewhere on the server, which is more efficient. For simplicity, I am saving the images here to a 
        server disk. 
        
    - Have a route in your application that returns a content type that is not _plaintext_
        - GET `/file/{filename}`, which returns a `FileResponse`.
        - make a request:
        ```bash
        pytest tests/test_file.py::test_download -s
        ```
        - expected stdout: 
        ```bash
        tests/test_file.py "/Users/yingjieqiao/Desktop/term6/networks_labs/networks_lab2/app/object_store/cat.png"
        ```
        - I was initially trying to return a base64 string so I could return a HTML text that can be copy-pasted into a browser
        to render into an image. But since this is requiring something not plaintext, I am returning a `FileResponse` of FastAPI here,
        which can be rendered as an image if you try out this endpoint in the SwaggerUI.
        
    - Some form of authorization through inspecting the request headers
        - the authorization is done with `check_request_header()` in `main.py`. A request can only be accepted if the header has a `x-token`
        and the value is the same as `SECRET_KEY` in the backend server. This `check_request_header()` is passed 
        as a dependency for all endpoints in `main.py`.
        - make a request with the correct header:
        ```bash
        pytest tests/test_heartbeat.py::test_pass_verification -s
        ```
        - expected stdout: 
        ```bash
        tests/test_heartbeat.py "The connection is up"
        ```
        - make a request without the correct header:
        ```bash
        pytest tests/test_heartbeat.py::test_fail_verification -s
        ```
        - expected stdout: error message
        ```bash
        tests/test_heartbeat.py {"detail":"Unauthorized"}
        ```
    - A special route that can perform a batch delete or update of resources 
    matching a certain condition
        - PUT `/student/pullup_gpa/{threshold}/{delta}` - pull up all students whose gpa is lower than `threshold` by `delta`
        - make the request: PUT `/student/pullup_gpa/4.0/0.5`
        ```bash
        pytest tests/test_put.py::test_batch_update -s
        ```
        - expected stdout: number of updated rows
        ```bash
        tests/test_put.py 4
        ```

> You must provide ample documentation on how to build & run your code and how to make the HTTP requests to your API, 
>as well as what are the expected responses for each request. 
>You will not be deducted if your program is slow or unoptimised, 
>but bonus points may be given if you show meaningful thought in analysing how performance was / can be improved 
>in your application.
