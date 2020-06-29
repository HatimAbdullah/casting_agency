# casting_agency

# Introduction

this is a sample casting agency web app, where you can manage the movies and actors that your studio poduce, you can kist and unlist movies, and actors. you can also cast and fire actors from your projects.

# Development Setup

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip3 install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=app.py
  $ export FLASK_ENV=development # enables debug mode
  $ flask run --reload
  ```
  
  # RBAC 
  
  in this web app there's three roles in addtion to the anonymous and feshly signed up user.
  
  1- Casting-asistant
    this user can view actors and movies in list and in detalis 
  
  2- Casting-director
    this user can view actors and movies in list and in detalis, also they can post new projects (movies) and new actor profiles and patch those models and also they can cast actors to movies and fire actors from movies
  
  3- Executive-producer
    this user can do all of the above and delete movies and actors.
    
    # Endpoints
    
    in this web app there's endpoints to view actors and movies in list and in details, 
    there's endpoints to to add movies and actors and also to patch and delete them, there is also an endpoint to cast actor to movies and fire them 
