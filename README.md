# Networks Lab 2

Qiao Yingjie

1004514


## Intro

Using FastAPI and PostgreSQL. This implements a student - course system where each course could enroll multiple students, but
a student can have at most 1 course. (see a command-line illustration of the one-to-many relationship [here](./one2many.md)),
and a gallery to showcase some beautiful images.

## Setup

Run the API server and database service with containers locally.

1. run the following to start the containers:

    ```bash
    docker-compose build
    docker-compose up
    ```
   
   Wait until both `db` and `rest_api` are up and running,
   
   ```bash
    db_1        | 2021-10-06 13:23:38.591 UTC [47] LOG:  database system was shut down at 2021-10-06 13:23:38 UTC
    db_1        | 2021-10-06 13:23:38.604 UTC [1] LOG:  database system is ready to accept connections
    rest_api_1  | INFO:     Started server process [1]
    rest_api_1  | INFO:     Waiting for application startup.
    rest_api_1  | INFO:     Application startup complete.
    rest_api_1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

   ```
   
   then proceed to then next step to go into the container.

2. Find the container IDs

    After the containers are up, run `docker container ls` to find the container with the name `networks_lab2_rest_api_1` 
    and the container with the name `networks_lab2_db_1`. Note down their container IDs.

3. Access the terminal of the API server container

    With the <rest_api_container_id> of the API server, run the following to go to the API server's terminal:

    ```bash
    docker exec -it <rest_api_container_id> bash
    ```

    After going into the terminal for the API server container, run the following to populate the database:
    
    ```bash
    python init_test.py
    ```

4. Access the terminal of the database container

    With the <db_container_id> of the database service, run the following to go to the terminal for the database container:
    
    ```bash
    docker exec -it <db_container_id> bash
    
    ```

    After going into the terminal for the database container, run the following to go to PostgreSQL command line:
    
    ```bash
    psql -U postgres
    ```

    Now, after you have run `python init_test.py` in Step 3 to populate the database tables, you should be able to see the 
    table names and inital values in table `course` and table `student`:
    
    
    ```bash
    bash-5.1# psql -U postgres
    psql (13.4)
    Type "help" for help.
    
    postgres=# \dt
              List of relations
     Schema |  Name   | Type  |  Owner   
    --------+---------+-------+----------
     public | course  | table | postgres
     public | file    | table | postgres
     public | student | table | postgres
    (3 rows)
    
    postgres=# SELECT * FROM course;
     id |         title          |          description          
    ----+------------------------+-------------------------------
      1 | Intro to Algo          | leetcode
      2 | Digital World          | use jupyter notebook
      3 | Computation Structures | most difficult module in ISTD
    
    postgres=# SELECT * FROM student;
     id |       name       |           email            | gpa | course_id 
    ----+------------------+----------------------------+-----+-----------
      1 | Walter White     | walter_white@sutd.edu      | 5.3 |          
      2 | Jesse Pinkman    | jess_pinkman@sutd.edu      | 0.5 |          
      3 | Gus String       | gus_string@sutd.edu        | 4.5 |          
      4 | Hank Schrader    | hank_schrader@sutd.edu     | 4.5 |          
      5 | Stannis Bar      | stannis_bar@sutd.edu       | 2.5 |          
      6 | Jon Snow         | jon_snow@sutd.edu          |   2 |          
      7 | Tyrion Lannister | tyrion_lanniester@sutd.edu |   5 |          
      8 | Cersei Lannister | cersei_lannister@sutd.edu  |   1 |          
    (8 rows)
    
    postgres=# 

    ```


---

when you terminate the containers, run

```bash
docker-compose down --volumes
```




## Checkoff Requirements


- A REST-over-HTTP API written in any programming language, in any framework, to imitate any real life service (e.g. fake myportal, fake edimension), backed with any other supporting services (redis, mysql, etc):
    - Can be deployed on any docker host using `docker compose` - you fail if I need to install any other dependencies on my computer!
        - see the [Setup](#setup) section above. 
        - In short, run `docker-compose up` at project root folder, and then attach to the FastAPI container.
  
**IMPORTANT**: 

Please run `python init_test.py` to populate the tables with some initial rows as shown in 
the [Setup](#setup) section above, so that the `GET` endpoints could work.

Running the tests with `pytest testfile.py::test_function -s`, with `-s` to capture stdout in terminal. All `pytest`
 commands should be run in the `rest_api` container and the commands that check the database tables should be run in the
  `db` container.

With accompanying `pytest` unit test files, showcasing your API's ability to respond to:


- a GET request ...
    - with no query parameters
        - GET `/course` and GET `/student`
        - make the request:
            ```bash
            pytest tests/test_get.py::test_get_student_all -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py [{"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":null},{"name":"Jesse Pinkman","email":"jess_pinkman@sutd.edu","gpa":0.5,"id":2,"course_id":null},{"name":"Gus String","email":"gus_string@sutd.edu","gpa":4.5,"id":3,"course_id":null},{"name":"Hank Schrader","email":"hank_schrader@sutd.edu","gpa":4.5,"id":4,"course_id":null},{"name":"Stannis Bar","email":"stannis_bar@sutd.edu","gpa":2.5,"id":5,"course_id":null},{"name":"Jon Snow","email":"jon_snow@sutd.edu","gpa":2.0,"id":6,"course_id":null},{"name":"Tyrion Lannister","email":"tyrion_lanniester@sutd.edu","gpa":5.0,"id":7,"course_id":null},{"name":"Cersei Lannister","email":"cersei_lannister@sutd.edu","gpa":1.0,"id":8,"course_id":null}]                                                                                                                                                                                                                                                                           
            ```
      
        - make the request:
            ```bash
            pytest tests/test_get.py::test_get_course_all -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py [{"title":"Intro to Algo","description":"leetcode","id":1,"enrolled_students":[]},{"title":"Digital World","description":"use jupyter notebook","id":2,"enrolled_students":[]},{"title":"Computation Structures","description":"most difficult module in ISTD","id":3,"enrolled_students":[]}]                                                                                                                                                                                                                                                                                    
            ```
      
    - with a `sortBy` query parameter, to transform the order of the items returned
        - GET `/student?sort_by=gpa` - sort the students by GPA in ascending order
        - make the request:
            ```bash
            pytest tests/test_get.py::test_get_student_sort_by -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py [{"name":"Jesse Pinkman","email":"jess_pinkman@sutd.edu","gpa":0.5,"id":2,"course_id":null},{"name":"Cersei Lannister","email":"cersei_lannister@sutd.edu","gpa":1.0,"id":8,"course_id":null},{"name":"Jon Snow","email":"jon_snow@sutd.edu","gpa":2.0,"id":6,"course_id":null},{"name":"Stannis Bar","email":"stannis_bar@sutd.edu","gpa":2.5,"id":5,"course_id":null},{"name":"Hank Schrader","email":"hank_schrader@sutd.edu","gpa":4.5,"id":4,"course_id":null},{"name":"Gus String","email":"gus_string@sutd.edu","gpa":4.5,"id":3,"course_id":null},{"name":"Tyrion Lannister","email":"tyrion_lanniester@sutd.edu","gpa":5.0,"id":7,"course_id":null},{"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":null}]
            ```
      
    - with a `count` query parameter, to limit the number of items returned
        - GET `/student?count=3` - return first 3 student rows in the table
        - make the request:
            ```bash
            pytest tests/test_get.py::test_get_student_count -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py [{"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":null},{"name":"Jesse Pinkman","email":"jess_pinkman@sutd.edu","gpa":0.5,"id":2,"course_id":null},{"name":"Gus String","email":"gus_string@sutd.edu","gpa":4.5,"id":3,"course_id":null}]
            ```
      
    - with a `offset` query parameter, to "skip" ahead by a number of items
        - GET `/student?offset=3` - skip first 3
        - make the request:
            ```bash
            pytest tests/test_get.py::test_get_student_offset -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py [{"name":"Hank Schrader","email":"hank_schrader@sutd.edu","gpa":4.5,"id":4,"course_id":null},{"name":"Stannis Bar","email":"stannis_bar@sutd.edu","gpa":2.5,"id":5,"course_id":null},{"name":"Jon Snow","email":"jon_snow@sutd.edu","gpa":2.0,"id":6,"course_id":null},{"name":"Tyrion Lannister","email":"tyrion_lanniester@sutd.edu","gpa":5.0,"id":7,"course_id":null},{"name":"Cersei Lannister","email":"cersei_lannister@sutd.edu","gpa":1.0,"id":8,"course_id":null}]
            ```
      
    - with any combination of the above query parameters
        - GET `/student?sort_by=gpa&count=5`
        - make the request:
            ```bash
            pytest tests/test_get.py::test_get_student_limit_sort_by -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py [{"name":"Jesse Pinkman","email":"jess_pinkman@sutd.edu","gpa":0.5,"id":2,"course_id":null},{"name":"Cersei Lannister","email":"cersei_lannister@sutd.edu","gpa":1.0,"id":8,"course_id":null},{"name":"Jon Snow","email":"jon_snow@sutd.edu","gpa":2.0,"id":6,"course_id":null},{"name":"Stannis Bar","email":"stannis_bar@sutd.edu","gpa":2.5,"id":5,"course_id":null},{"name":"Hank Schrader","email":"hank_schrader@sutd.edu","gpa":4.5,"id":4,"course_id":null}]
            ```

- a POST request ...
    - that creates a new resource with the given attributes in the body
        - POST `/course`, POST `/student`
        - make valid requests: - add student `Samwell Tarly` and course `Discrete Math` to the tables
            ```bash
            pytest tests/test_create.py::test_create_student_success -s
            pytest tests/test_create.py::test_create_course_success -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    
    
            tests/test_create.py {"name":"Samwell Tarly","email":"samwell_tarly@sutd.edu","gpa":5.0,"id":9,"course_id":null}
            
          
            collected 1 item                                                                                                                                                                                                                                                                                    
    
            tests/test_create.py {"title":"Discrete Math","description":"sutd doesnt teach","id":4,"enrolled_students":[]}
            ```
        - check the database tables - you can see new rows added:
            ```bash
            postgres=# SELECT * FROM course;
             id |         title          |          description          
            ----+------------------------+-------------------------------
              1 | Intro to Algo          | leetcode
              2 | Digital World          | use jupyter notebook
              3 | Computation Structures | most difficult module in ISTD
              4 | Discrete Math          | sutd doesnt teach
            (4 rows)
            
            postgres=# SELECT * FROM student;
             id |       name       |           email            | gpa | course_id 
            ----+------------------+----------------------------+-----+-----------
              1 | Walter White     | walter_white@sutd.edu      | 5.3 |          
              2 | Jesse Pinkman    | jess_pinkman@sutd.edu      | 0.5 |          
              3 | Gus String       | gus_string@sutd.edu        | 4.5 |          
              4 | Hank Schrader    | hank_schrader@sutd.edu     | 4.5 |          
              5 | Stannis Bar      | stannis_bar@sutd.edu       | 2.5 |          
              6 | Jon Snow         | jon_snow@sutd.edu          |   2 |          
              7 | Tyrion Lannister | tyrion_lanniester@sutd.edu |   5 |          
              8 | Cersei Lannister | cersei_lannister@sutd.edu  |   1 |          
              9 | Samwell Tarly    | samwell_tarly@sutd.edu     |   5 |          
            (9 rows)
            
            postgres=# 
            
            ```
          
    - show that the resource has indeed been created through another HTTP request
        - GET `/course/{course_name}` and GET `/student/{student_name}`
        - make the requests: GET `/course/Discrete%20Math` and GET `/student/Samwell%20Tarly` 
            ```bash
            pytest tests/test_get.py::test_get_course_by_name -s
            pytest tests/test_get.py::test_get_student_by_name -s
            ```
        - expected stdout: 
        
            ```bash                                                                                                                                                                                                                                                                      
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py <app.app.models.Course object at 0x7f2c7f2d4100>
            {"title":"Discrete Math","description":"sutd doesnt teach","id":4,"enrolled_students":[]}
      
      
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py {"name":"Samwell Tarly","email":"samwell_tarly@sutd.edu","gpa":5.0,"id":9,"course_id":null}
            ```
      
    - has validation and returns an appropriate HTTP response code if the input data is invalid 
    (e.g. missing name)
        - invalid requests: row already exists. Try insert the same `Student` into table:
            ```bash
            pytest tests/test_create.py::test_create_student_fail_1 -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    
    
            tests/test_create.py {"detail":"This student has already been created."}
            ```
        - check the table `student` and no duplicated row is added:
            ```bash
            postgres=# SELECT * FROM student;
             id |       name       |           email            | gpa | course_id 
            ----+------------------+----------------------------+-----+-----------
              1 | Walter White     | walter_white@sutd.edu      | 5.3 |          
              2 | Jesse Pinkman    | jess_pinkman@sutd.edu      | 0.5 |          
              3 | Gus String       | gus_string@sutd.edu        | 4.5 |          
              4 | Hank Schrader    | hank_schrader@sutd.edu     | 4.5 |          
              5 | Stannis Bar      | stannis_bar@sutd.edu       | 2.5 |          
              6 | Jon Snow         | jon_snow@sutd.edu          |   2 |          
              7 | Tyrion Lannister | tyrion_lanniester@sutd.edu |   5 |          
              8 | Cersei Lannister | cersei_lannister@sutd.edu  |   1 |          
              9 | Samwell Tarly    | samwell_tarly@sutd.edu     |   5 |          
            (9 rows)
    
            ```
        - invalid requests - missing name/field in the request body, using a Bad Request Body missing a necessary field:
            ```json
            CREATE_COURSE_FAIL_1 = {
                "title": "missing description"
            }
            ``` 
            To make the request:
            ```bash
            pytest tests/test_create.py::test_create_course_fail_1 -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_create.py {"detail":[{"loc":["body","description"],"msg":"field required","type":"value_error.missing"}]}
            ```
        - check database table:
            ```bash
            postgres=# SELECT * FROM course;
             id |         title          |          description          
            ----+------------------------+-------------------------------
              1 | Intro to Algo          | leetcode
              2 | Digital World          | use jupyter notebook
              3 | Computation Structures | most difficult module in ISTD
              4 | Discrete Math          | sutd doesnt teach
            (4 rows)
            ```
        
- either a DELETE or PUT request...
    - that deletes or updates a _single_ resource respectively
        - DELETE `/course`, DELETE `/student`, PUT `/course/{course_id}/{student_id}`
        
        - make the requests: delete student `Samwell Tarly`, course `Discrete Math` and enroll the first student in the 
        table to the first course in he table
        
            ```bash
            pytest tests/test_delete.py::test_delete_course -s
            pytest tests/test_delete.py::test_delete_student -s
            pytest tests/test_put.py::test_single_update -s
            ```
        
        - expected stdout for DELETE:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_delete.py {"title":"Discrete Math","description":"sutd doesnt teach","id":4,"enrolled_students":[]}

          
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_delete.py {"name":"Samwell Tarly","email":"samwell_tarly@sutd.edu","gpa":5.0,"id":9,"course_id":null}
            ```
        
        - expected stdout for PUT:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    
    
            tests/test_put.py {"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}
            ```
            
    - show that the resource has indeed been modified through another HTTP request 
        - for the DELETE, use GET `/course/{course_name}`, GET `/student/{student_name}`
        - make the requests:  GET `/student/Samwell%20Tarly` and GET `/course/Discrete%20Math`
            ```bash
            pytest tests/test_get.py::test_get_student_by_name_for_delete -s  
            pytest tests/test_get.py::test_get_course_by_name_for_delete -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py {"detail":"Student not found"}

            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py {"detail":"Course not found"}
            ```
        indicating that they are indeed already deleted from the table.
      
        - for the PUT, use GET `/course/byid/{course_id}`, GET `/student/byid/{student_id}`
        - make the requests: GET `/course/byid/1` and GET `/student/byid/1`
            ```bash
            pytest tests/test_get.py::test_get_course_by_id -s 
            pytest tests/test_get.py::test_get_student_by_id -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py {"title":"Intro to Algo","description":"leetcode","id":1,"enrolled_students":[{"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}]}

            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_get.py {"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}
            ```
        We can see that the `Course` with title `Intro to Algo` has a new `Student` added to its `enrolled_students`, 
        and the `course_id` of the `Student`, whose name is `Walter White`, is also updated.
        
        - check the effect of DELETE and PUT by observing the table:
        - the newly added rows are deleted, and the foreign key of `Walter White` is updated to the `course_id` he has enrolled in.
            ```bash
            postgres=# SELECT * FROM student;
             id |       name       |           email            | gpa | course_id 
            ----+------------------+----------------------------+-----+-----------
              2 | Jesse Pinkman    | jess_pinkman@sutd.edu      | 0.5 |          
              3 | Gus String       | gus_string@sutd.edu        | 4.5 |          
              4 | Hank Schrader    | hank_schrader@sutd.edu     | 4.5 |          
              5 | Stannis Bar      | stannis_bar@sutd.edu       | 2.5 |          
              6 | Jon Snow         | jon_snow@sutd.edu          |   2 |          
              7 | Tyrion Lannister | tyrion_lanniester@sutd.edu |   5 |          
              8 | Cersei Lannister | cersei_lannister@sutd.edu  |   1 |          
              1 | Walter White     | walter_white@sutd.edu      | 5.3 |         1
            (8 rows)
            

            ```
        
    - has validation and returns an appropiate HTTP response code if the input data is invalid 
    (e.g. trying to delete a nonexistent user)
        - To validate the request and check if he rows exist in the table for the DELETE `/course`, 
        because we have already executed it once previously 
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
            collected 1 item                                                                                                                                                                                                                                                                                    
    
            tests/test_delete.py {"detail":"Trying to delete nonexistent rows."}
    
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_delete.py {"detail":"Trying to delete nonexistent rows."}
            ```
      
        - To validate the request and check if he rows exist in the table for the PUT
         `/course/{course_id}/{student_id}` endpoint, we need to reject the request if either `Student` or `Course`
         do not exist
        - make the requests:
            ```bash
            pytest tests/test_put.py::test_single_update_validate_course_not_found -s
            pytest tests/test_put.py::test_single_update_validate_student_not_found -s
            ```
        - expected stdout:
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_put.py {"detail":"Course not Found."}

            
            collected 1 item                                                                                                                                                                                                                                                                                    

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
        collected 1 item                                                                                                                                                                                                                                                                                    
    
        tests/test_put.py {"name":"Walter White","email":"walter_white@sutd.edu","gpa":5.3,"id":1,"course_id":1}
        ```
    which is the same result as making the request only once.
    
- Implement at least two of the following challenges:
    - File upload in a POST request, using multipart/form-data
        - POST `/file` - add a new row to table `file` and save the image to a folder on disk `./app/object_store`. 
        returns the path to the file saved localtion on server;
            - make a request:
            ```bash
            pytest tests/test_file.py::test_upload -s
            ```
        - expected stdout: 
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    
    
            tests/test_file.py "/app/app/object_store/cat.png"
            ```
        - And you can see a `cat.png` under `./app/object_store`.
        
        - A side note: To my knowledge, I think the best way to store large binary assets like image and video is to
        save them to an Object Store service like AWS S3, or a base64 string in the database table (for images), 
        or, save a path to the asset in the database table and keep
        the asset somewhere on the server, which is more efficient. For simplicity, I am saving the images here to a 
        server disk and the name of the file to the table `file` - the filename in the table will be used to construct 
        the path to the file for the GET request.
        
    - Have a route in your application that returns a content type that is not _plaintext_
        - GET `/file/{filename}`, which returns a `FileResponse`.
        - make a request:
            ```bash
            pytest tests/test_file.py::test_download -s
            ```
        - expected stdout: 
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_file.py <Response [200]>
            ```
        - I was initially trying to return a base64 string so I could return a HTML text that can be copy-pasted 
        into a browser
        to render into an image. But since this is requiring something not plaintext, 
        I am returning a `FileResponse` of FastAPI here.
        
    - Some form of authorization through inspecting the request headers
        - the authorization is done with `check_request_header()` in `main.py`. 
        A request can only be accepted if the header has a `x-token`
        and the value is the same as `SECRET_KEY` in the backend server (the value can be found in `.env`). 
        This `check_request_header()` is passed 
        as a dependency to all endpoints in `main.py`.
        - make a request with the correct header:
            ```bash
            pytest tests/test_heartbeat.py::test_pass_verification -s
            ```
        - expected stdout: 
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    
    
            tests/test_heartbeat.py "The connection is up"
    
            ```
        - make a request without the correct header:
            ```bash
            pytest tests/test_heartbeat.py::test_fail_verification -s
            ```
        - expected stdout: error message
            ```bash
            collected 1 item                                                                                                                                                                                                                                                                                    

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
            collected 1 item                                                                                                                                                                                                                                                                                    

            tests/test_put.py 4
            ```
        - check the database table: you can see the students whose GPA is lower than 4.0 are pulled up by 0.5
        (Jesse Pinkman, Stannis Bar, Jon Snow, Cersei Lannister)
            ```bash
            postgres=# SELECT * FROM student;
             id |       name       |           email            | gpa | course_id 
            ----+------------------+----------------------------+-----+-----------
              3 | Gus String       | gus_string@sutd.edu        | 4.5 |          
              4 | Hank Schrader    | hank_schrader@sutd.edu     | 4.5 |          
              7 | Tyrion Lannister | tyrion_lanniester@sutd.edu |   5 |          
              1 | Walter White     | walter_white@sutd.edu      | 5.3 |         1
              2 | Jesse Pinkman    | jess_pinkman@sutd.edu      |   1 |          
              5 | Stannis Bar      | stannis_bar@sutd.edu       |   3 |          
              6 | Jon Snow         | jon_snow@sutd.edu          | 2.5 |          
              8 | Cersei Lannister | cersei_lannister@sutd.edu  | 1.5 |          
            (8 rows)
            ``` 

> You must provide ample documentation on how to build & run your code and how to make the HTTP requests to your API, 
>as well as what are the expected responses for each request. 
>You will not be deducted if your program is slow or unoptimised, 
>but bonus points may be given if you show meaningful thought in analysing how performance was / can be improved 
>in your application.
