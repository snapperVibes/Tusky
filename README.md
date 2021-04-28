# Tusky
###### Real-time web quiz application
(Work in progress)

## Specification
### Functional
  - Two workflows, dubbed **teacher** and **student**. A user is both a **student** and 
  a **teacher**, depending on if they have **teacher permissions** in a room.
  - A user creates a **room** (and begins the **teacher** workflow)
   The **room** is the core part of user interaction
  - From the **room**, the **teacher** can create / edit / administer **quizzes**
  - **Students** can enter a **teacher's** room and take a **quiz** that is being administered.
  - **Teachers** can edit a **quiz** *while* it is being administered. 
  This is done in a way that is guaranteed not to harm students by both making it clear 
  to the **student** that the question has changed and barring the **teacher** from 
  including the particular result in the final grade.
  - The **teacher** has several views of a quizzes responses
    - A real time, **room** specific aggregate view
    - A view of a specific **student's** responses
    - An all-time view of aggregate responses
    - *Future*: **Class** based view.

### Design
#### Backend
  [comment]: <> ( Figure out what server to use )
  - Tech stack: Linux / ... / Postgres / Python (FastAPI)
  - Easy to build using Docker
  
  [comment]: <> ( Explain typical FastAPI structure )
There are 4 important parts of a FastAPI application:
  - scheams
    Pydantic schemas 
  - models
    Database models (SQL Alchemy)
  - crud (create / read / update / delete)
  - routes
    The actual API Endpoints.  

#### Frontend
  - VueJS (With Axios)

[comment]: <> (
## Misc
### A user signs in. Then what happens?
  - After hitting the login button, a request is made to the backend with the user's details
  - When
)

[comment]: <> (
    Security is hard.
    There is a lot of conflicting advice on managing state.
    Ultimately, I decided to use Json Web Tokens despite the naysayers: http://cryto.net/~joepie91/blog/2016/06/19/stop-using-jwt-for-sessions-part-2-why-your-solution-doesnt-work/
    because FastAPI's documentation recommends JWTs: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    I followed this 2019 guide: https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/
)
