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
  # Deployed Web app link
     https://fish-studios.herokuapp.com/
     
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
    
 #### get '/movies'
  Returns a list of all the movies storeed in the db in a web-page where they are grouped by thier release date
  
 #### get '/actors'
  Returns a list of all the actors storeed in the db in a web-page where they are listed with thier names, age, and gender
  
 #### get '/movies/1'
  Returns a detalid page for the movie with id 1 (if it exsist) in a web-page where all the movie's detalis are listed along with the cast
  
 #### get '/actors/1'
  Returns a detalid page for the actor with id 1 (if it exsist) in a web-page where all the actor's detalis are listed along with the movies they have been in

 #### get '/movies/create'
  Returns a form in the browser where you can fill the movie's information in order to create on
  
 #### get '/actors/create'
  Returns a form in the browser where you can fill the actor's information in order to create on
  
 #### post '/movies'
  a form with all the movie's info (name, release_date, image_link, film_summary) has to be sent with this along when you call this endpoint in order to add a movie to the database 
  
 #### post '/actors'
  a form with all the actor's info (name, age, gender, place_of_birth, contact, image_link, has_bio, bio) has to be sent with this along when you call this endpoint in order to add an actor to the database 
  
#### get '/movies/1/patch'
  Returns a form in the browser where you can change the movie with id 1 information and submits them to db
  
#### get '/actors/1/patch'
   Returns a form in the browser where you can change the actor with id 1 information and submits them to db
   
#### post '/movies/1/patch'
  submits the changes you did in the form to the db and the movie gets updated accordingly 
  
#### post '/actors/1/patch'
   submits the changes you did in the form to the db and the actor gets updated accordingly
   
#### get '/movies/1/delete'
  Deletes the movie with id from db and therfore it will not appear in your movies page anymore
  
#### get '/actors/1/delete'
   Deletes the actor with id from db and therfore it will not appear in your actor page anymore
   
#### get '/cast'
   retuns a web-page that includes a form where you can choose one of the actors in your system to be casted in one of the movies in your system, both actors and      movies are provided in a drop down list
   
#### post '/cast-actor-to-movie'
   takes the submittesd form in the /cast end point and then makes a relatioship between the two parties you provided by appending the actors to the movie's cast 
   
#### get '/fire-actor-from-movie/1/2'
   breakes the relationship between movie with id 1 and actor with id 2 by removing the actor from the movie's cast
   
#### get '/login'
   redirects the user to auth0 login page where the user can log in or sign up to the website
   
