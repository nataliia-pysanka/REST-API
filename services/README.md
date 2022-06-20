# Movies API

This is pet-project for collection and integration of knowledge about API 
services on Flask.  

#### The following requirements are implemented:
* The search for movies returns partial matches.
* Pagination for display search movies results.
* Only authorized user could add new movies.
* Only authorized user added the movie or Admin could delete and edit it.
* Everybody could search the movie.
* Movies can be filtered by: genres, release year range, director.
* The movies attribute: title, genre, date of release, director, description, rating, poster, user who added
* Using validations, error codes, messages, logging.
* Authorization.

#### The following requirements are being developed:
* Movies can be sorted by: rating, release date.
* Many-to-many relationships between Movie and Genre/Director/Poster/User.
* When removing a director, the movie should NOT be removed, instead director = 'unknown' should be set.


## Synopsis

* `Flask` 
* `Flask-Login`
* `Flask-Migrate` 
* `Postgres` 
* `Flask_sqlalchemy`
* `Pydantic`
* `Flask-restx`
* `Mock-alchemy`
* `pytest-mock`
* `Faker`
* `mock-alchemy`
* `Python-dotenv`
* `Config`
* `pipenv`
* `git`
* `Docker-compose`


The application is organized around a Repository pattern. 

```bash
.
├── wsqi.py
├── nginx
├── Makefile
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
└── app 
    ├── crud        # repositories
    ├── domain      # logic
    ├── models      # SQLAlchemy models
    ├── resources   # routes
    └── shemas      # pydantic models
    └── seed         
    └── tests
    └── util
    └── __init__.py
    └── auth.py     # authorization
    └── db.py       # database
    
```
## API

### Swagger-documentation:
```bash
{URI}/api/doc
```

### Routes:
```bash
{URI}/api/movies(users/genres/roles/directors/posters)
{URI}/api/movie(user/genre/role/director/poster)/
```

### Authorization:
```bash
{URI}/auth/login
{URI}/auth/signin
{URI}/auth/user_info
{URI}/auth/logout
```

## Installation

### Requirements

Docker-compose (https://docs.docker.com/compose/)

### Deploy

```bash
# Clone this repository using git
sudo cd services
# Build the container
make up
# Create database
make db
# Init the database
make init
# Make migrations
make migrate
# Upgrade database
make upgrade
# Seed database (values for quantity in .env.prod file)
make seed
# Navigate to http://localhost/api/doc
```

### Destroy

```bash
sudo docker-compose down -v
```


