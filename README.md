# Tusky
###### Real-time web quiz application
(Work in progress; Tusky certainly isn't ready to scale to 10,000 users)

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
    - *Future*: **Class** (as in a collection of **students**) based view.

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

### Misc  
The frontend contains low quality code.
  I am not a JavaScript developer, 
  and I just needed a minimum-viable-product.
  Hiring an actual front-end dev would go a long way for this project.
  
The backend contains maintainable, mostly idiomatic Python.

Exceptions are a work in progress. 
  Initially, an attempt was made to treat errors like values 
  (in a similar vain to Go and Rust).
  Although forcing the caller of a function to deal with the error 
  made the code very explicit,
  the code felt extremely un-pythonic.
  
[comment]: <> (
  Although this is true, I will not add this comment until after Tusky is released:
  On a personal note: I am proud of Tusky's design and believe it could be a genuinely useful tool.
  I think the code accurately displays my skill-set for backend DevOps.
  Unfortenetly, this is by no means a professional product.
  There's a laundry list of details that need attention, 
  but they will be ironed out over time.
)

[comment]: <> (
 -- Misc: A user signs in, then what?
)

[comment]: <> (
    Security is hard.
    There is a lot of conflicting advice on managing state.
    Ultimately, I decided to use Json Web Tokens despite the naysayers: http://cryto.net/~joepie91/blog/2016/06/19/stop-using-jwt-for-sessions-part-2-why-your-solution-doesnt-work/
    because FastAPI's documentation recommends JWTs: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    I followed this 2019 guide: https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/
)


