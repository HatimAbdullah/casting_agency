import os
from flask import Flask, request, abort, jsonify, render_template, flash, session, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import func
from models import setup_db, Actor, Movie
import requests
from auth.auth import AuthError, requires_auth
from forms import ActorForm, MovieForm


SECRET_KEY = os.urandom(32)
ITEMS_PER_PAGE = 10

def paginate_list(request, somethings):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * ITEMS_PER_PAGE
  end = start + ITEMS_PER_PAGE

  jsonified_something = [something.format() for something in somethings]
  jsonified_paginated_something = jsonified_something[start:end]

  return jsonified_paginated_something


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config['SECRET_KEY'] = SECRET_KEY
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  @app.route('/')
  @cross_origin()
  def welcome():
  	return render_template('pages/home.html'), 200
  	'''
  	#API SOULTION
    return jsonify({'message':'welcome to the only api in the world!! you are making history just byy using it..'})
    '''

  @app.route('/login', methods=['GET'])
  @cross_origin()
  def login():
    req = requests.get('https://fishland.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=9CBuha8U6lNHmS7xp5SjDTEzA4YuTLkG&redirect_uri=http://localhost:5000/post-login')

    return Response(
        req.text,
        status = req.status_code,
        content_type = req.headers['content-type'],
    )

  @app.route('/post-login', methods=['GET'])
  @cross_origin()
  def post_login():
    resp = make_response(render_template('pages/home.html'))
    return resp


  @app.route('/actors', methods=['GET'])
  @cross_origin()
  @requires_auth('read:casting-assistant')
  def get_actors(payload):
    actors = Actor.query.all()
    
    actors_data = []
    for actor in actors:
      actors_data.append({
        "id": actor.id,
        "name": actor.name, 
        "age": actor.age, 
        "gender": actor.gender
      })

    return render_template('pages/actors.html', actors=actors_data), 200

  '''
  	#API SOULTUION
    actors = Actor.query.all()

    if len(actors) == 0:
      abort(404)

    jsonified_paginated_actors = paginate_list(request,actors)

    if (len(jsonified_paginated_actors) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'actors': jsonified_paginated_actors,
      'total_actors': len(actors),
      })
    '''
  @app.route('/movies', methods=['GET'])
  @cross_origin()
  @requires_auth('read:casting-assistant')
  def get_movies(payload):
    filtered_movies = Movie.query.with_entities(func.count(Movie.id), Movie.release_date).group_by(Movie.release_date).all()
    data = []

    for fm in filtered_movies:
      movie_date = Movie.query.filter_by(release_date=fm.release_date).all()
      movies_data = []
      for movie in movie_date:
        movies_data.append({
          "id": movie.id,
          "name": movie.name, 
          "cast": movie.cast
        })
        
      data.append({
        "release_date": fm.release_date,
        "movie_data": movies_data
      })

    return render_template('pages/movies.html', movies=data), 200  
  '''
  	#API SOULTION

  	movies = Movie.query.all()

  	if len(movies) == 0:
  	  abort(404)

  	jsonified_paginated_movies = paginate_list(request,movies)

  	if (len(jsonified_paginated_movies) == 0):
  	  abort(404)

  	return jsonify({
      'success': True,
      'movies': jsonified_paginated_movies,
      'total_movies': len(movies),
      })
      '''

  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('read:casting-assistant')
  def get_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)

    if actor is None:
      abort(404)

    movies_starred = actor.movies
    frontend_structure = []

    for movie in movies_starred:
      frontend_structure.append({
        "name": movie.name,
        "id": movie.id,
        "film_summary": movie.film_summary,
        "movie_image_link": movie.image_link,
        "release_date": movie.release_date
      })


    actor_details = {
      "id": actor.id,
      "name": actor.name,
      "gender": actor.gender,
      "age": actor.age,
      "place_of_birth": actor.place_of_birth,
      "contact": actor.contact,
      "has_bio": actor.has_bio,
      "bio": actor.bio,
      "image_link": actor.image_link,
      "featured_movies": frontend_structure,
      "featured_movies_count": len(frontend_structure),
    }

    return render_template('pages/show_actor.html', actor=actor_details), 200

  '''
#APISOLTION
    actor = Actor.query.get(actor_id)

    if actor is None:
      abort(404)

   
    return jsonify({
      'success': True,
      'actor': actor.format(),
    })
    '''

  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth('read:casting-assistant')
  def get_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)

    if movie is None:
      abort(404)

    cast = movie.cast
    frontend_structure = []

    for actor in cast:
      frontend_structure.append({
        "name": actor.name,
        "id": actor.id,
        "bio": actor.bio,
        "actor_image_link": actor.image_link,
        "gender": actor.gender
      })


    movie_details = {
      "id": movie.id,
      "name": movie.name,
      "film_summary": movie.film_summary,
      "release_date": movie.release_date,
      "image_link": movie.image_link,
      "cast": frontend_structure,
      "cast_count": len(frontend_structure),
    }

    return render_template('pages/show_movie.html', movie=movie_details), 200    

    '''
    movie = Movie.query.get(movie_id)

    if movie is None:
      abort(404)

   
    return jsonify({
      'success': True,
      'movie': movie.format(),
    })
   '''
  @app.route('/actors/create', methods=['GET'])
  @requires_auth('write:casting-director')
  def create_actor_form(payload):
    form = ActorForm()
    return render_template('forms/new_actor.html', form=form), 200

  @app.route("/actors", methods=['POST'])
  @requires_auth('write:casting-director')
  def add_actor(payload):
  	error_flag = False

  	name = request.form['name']
  	age = request.form['age']
  	gender = request.form['gender']
  	place_of_birth = request.form['place_of_birth']
  	contact = request.form['contact']
  	image_link = request.form['image_link']
  	if request.form['has_bio'] == 'n':
  	  has_bio = False
  	else:
  	  has_bio = True
  	bio = request.form['bio']

  	try: 
  	  actor = Actor(name=name, age=age, gender=gender, place_of_birth=place_of_birth, contact=contact, image_link=image_link, has_bio=has_bio, bio=bio)
  	  actor.insert()
  	except: 
  	 error_flag = True

  	if error_flag: 
  	  flash('An error occurred. Actor ' + name + ' could not be listed.')
  	  abort(422)
  	if not error_flag: 
  	  flash('Actor ' + name + ' was successfully listed!')

  	return render_template('pages/home.html'), 201


  	'''
  	#APISOULTION
    actor_info = request.get_json()
    
    if not ('name' in actor_info and 'age' in actor_info and 'gender' in actor_info):
      abort(422)
    
    actor_name = actor_info.get('name')
    actor_age = actor_info.get('age')
    actor_gender = actor_info.get('gender')
   
    try:
	    actor = Actor(name=actor_name, gender=actor_gender, age=actor_age)
	    actor.insert()

	    return jsonify({
	      'success': True,
	      'created_with_id': actor.id,
	      })

    except:
      abort(422)
'''
  @app.route('/movies/create', methods=['GET'])
  @requires_auth('write:casting-director')
  def create_movie_form(payload):
    form = MovieForm()
    return render_template('forms/new_film.html', form=form), 200

  @app.route("/movies", methods=['POST'])
  @requires_auth('write:casting-director')
  def add_movie(payload):
  	error_flag = False

  	name = request.form['name']
  	release_date = request.form['release_date']
  	image_link = request.form['image_link']
  	film_summary = request.form['film_summary']

  	try: 
  	  movie = Movie(name=name, release_date=release_date, image_link=image_link, film_summary=film_summary)
  	  movie.insert()
  	except: 
  	  error_flag = True

  	if error_flag: 
  	  flash('An error occurred. Film ' + name + ' could not be listed.')
  	  abort(422)
  	if not error_flag: 
  	  flash('Film ' + name + ' was successfully listed!')

  	return render_template('pages/home.html'), 201



  	'''
  	#APISOULTION
    movie_info = request.get_json()
    
    if not ('name' in movie_info and 'release_date' in movie_info):
      abort(422)
    
    movie_name = movie_info.get('name')
    movie_release_date = movie_info.get('release_date')

    try:
	    movie = Movie(name=movie_name, release_date=movie_release_date)
	    movie.insert()

	    return jsonify({
	      'success': True,
	      'created_with_id': movie.id,
	      })

    except:
      abort(422)
'''

  @app.route('/cast')
  @requires_auth('write:casting-director')
  def cast_actor(payload):
    movies = Movie.query.all()
    actors = Actor.query.all()
    return render_template('forms/cast.html', movies=movies, actors=actors), 200


  @app.route("/cast-actor-to-movie", methods=['POST'])
  @requires_auth('write:casting-director')
  def link_actor_to_movie(payload):
  	actor_id = request.form['actor_id']
  	movie_id = request.form['movie_id']
  	error_flag = False

  	try:
  	  movie = Movie.query.get(movie_id)
  	  actor = Actor.query.get(actor_id)

  	  if actor is None or movie is None:
  	  	abort(404)

  	  movie.cast.append(actor)
  	  movie.update()

  	except:
  	  error_flag = True

  	if error_flag: 
  	  flash('An error occurred. Actor with id ' + actor_id + ' could not be casted.')
  	  abort(422)
  	if not error_flag: 
  	  flash('Actor ' + actor.name + ' was successfully casted to ' + movie.name)

  	return render_template('pages/home.html'), 201



  	'''
    linkage_info = request.get_json()
    
    if not ('movie_id' in linkage_info and 'actor_id' in linkage_info):
      abort(422)
    
    movie_id = linkage_info.get('movie_id')
    actor_id = linkage_info.get('actor_id')

    try:
      movie = Movie.query.get(movie_id)
      actor = Actor.query.get(actor_id)

      if actor is None or movie is None:
        abort(404)

      movie.cast.append(actor)
      movie.update()

      return jsonify({
        'success': True,
        'movie': movie.format(),
      })

    except:
      abort(422)
'''

  @app.route("/fire-actor-from-movie/<int:movie_id>/<int:actor_id>", methods=['GET'])
  @requires_auth('write:casting-director')
  def fire_actor_from_movie(payload, movie_id, actor_id):
  	error_flag = False

  	try:
  	  movie = Movie.query.get(movie_id)
  	  actor = Actor.query.get(actor_id)

  	  if actor is None or movie is None:
  	  	abort(404)

  	  movie.cast.remove(actor)
  	  movie.update()

  	except:
  	  error_flag = True

  	if error_flag: 
  	  flash('An error occurred. Actor with id ' + actor_id + ' could not be fired.')
  	  abort(422)
  	if not error_flag: 
  	  flash('Actor ' + actor.name + ' was successfully fired from ' + movie.name)

  	return render_template('pages/home.html'), 200
  	'''
    linkage_info = request.get_json()
    
    if not ('movie_id' in linkage_info and 'actor_id' in linkage_info):
      abort(422)
    
    movie_id = linkage_info.get('movie_id')
    actor_id = linkage_info.get('actor_id')

    try:
      movie = Movie.query.get(movie_id)
      actor = Actor.query.get(actor_id)
    
      if actor is None or movie is None:
        abort(404)

      movie.cast.remove(actor)
      movie.update()

      return jsonify({
        'success': True,
        'movie': movie.format(),
      })

    except:
     abort(422)
   '''
  @app.route('/movies/<int:movie_id>/patch', methods=['GET'])
  @requires_auth('write:casting-director')
  def edit_movie(payload, movie_id):
    form = MovieForm()
    movie = Movie.query.get(movie_id)

    if not movie: 
      abort(404)

    if movie: 
      form.name.data = movie.name
      form.release_date.data = movie.release_date
      form.image_link.data = movie.image_link
      form.film_summary.data = movie.film_summary

  
    return render_template('forms/edit_movie.html', form=form, movie=movie), 200

  @app.route('/movies/<int:movie_id>/patch', methods=['POST'])
  @requires_auth('write:casting-director')
  def patch_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    error_flag = False

    if not movie: 
      abort(404)

    
    try:
      new_name = request.form['name']
      movie.name = new_name
      new_release_date = request.form['release_date']
      movie.release_date = new_release_date
      new_image_link = request.form['image_link']
      movie.image_link = new_image_link
      new_film_summary = request.form['film_summary']
      movie.film_summary = new_film_summary

      movie.update()
    except:
      error_flag = True

    if error_flag: 
      flash('An error occurred. Movie ' + new_name + ' could not be editid.')
      abort(422)

    if not error_flag:
      flash('Movie ' + new_name + ' was successfully editid')

    return render_template('pages/home.html'), 202

  '''
    movie = Movie.query.get(movie_id)

    if movie is None:
      abort(404)

    movie_info = request.get_json()

    if ('name' in movie_info):
      try:
      	new_name = movie_info.get('name')
      	movie.name = new_name
      except:
      	abort(422)

    if ('release_date' in movie_info):
      try:
      	new_release_date = movie_info.get('release_date')
      	movie.release_date = new_release_date
      except:
      	abort(422)

    movie.update()
    patched_movie = Movie.query.get(movie_id)

    if patched_movie is None:
      abort(500) 

    return jsonify({
      'success': True,
      'patched_actor': patched_movie.format(),
    })
    '''
  

  @app.route('/actors/<int:actor_id>/patch', methods=['GET'])
  @requires_auth('write:casting-director')
  def edit_actor(payload, actor_id):
    form = ActorForm()
    actor = Actor.query.get(actor_id)

    if not actor: 
      abort(404)

    if actor: 
      form.name.data = actor.name
      form.age.data = actor.age
      form.gender.data = actor.gender
      form.contact.data = actor.contact
      form.place_of_birth.data = actor.place_of_birth
      form.has_bio.data = actor.has_bio
      form.image_link.data = actor.image_link
      form.bio.data = actor.bio

  
    return render_template('forms/edit_actor.html', form=form, actor=actor), 200

  @app.route('/actors/<int:actor_id>/patch', methods=['POST'])
  @requires_auth('write:casting-director')
  def patch_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)
    error_flag = False

    if not actor: 
      abort(404)

    
    try:
      new_name = request.form['name']
      actor.name = new_name
      new_gender = request.form['gender']
      actor.gender = new_gender
      new_age = request.form['age']
      actor.age = new_age
      new_place_of_birth = request.form['place_of_birth']
      actor.place_of_birth = new_place_of_birth
      new_contact = request.form['contact']
      actor.contact = new_contact
      new_image_link = request.form['image_link']
      actor.image_link = new_image_link
      if request.form['has_bio'] == 'n':
        new_has_bio = False
      else:
        new_has_bio = True
      actor.has_bio = new_has_bio
      new_bio = request.form['bio']
      actor.bio = new_bio

      actor.update()
    except:
      error_flag = True

    if error_flag: 
      flash('An error occurred. Actor ' + new_name + ' could not be editid.')
      abort(422)

    if not error_flag:
      flash('Actor ' + new_name + ' was successfully editid')

    return render_template('pages/home.html'), 202
    

    '''
    actor = Actor.query.get(actor_id)

    if actor is None:
      abort(404)

    actor_info = request.get_json()

    if ('name' in actor_info):
      try:
      	new_name = actor_info.get('name')
      	actor.name = new_name
      except:
      	abort(422)

    if ('gender' in actor_info):
      try:
      	new_gender = actor_info.get('gender')
      	actor.gender = new_gender
      except:
      	abort(422)

    if ('age' in actor_info):
      try:
      	new_age = actor_info.get('age')
      	actor.age = new_age
      except:
      	abort(422)

    actor.update()
    patched_actor = Actor.query.get(actor_id)

    if patched_actor is None:
      abort(500) 

    return jsonify({
      'success': True,
      'patched_actor': patched_actor.format(),
    })
    '''


  @app.route("/movies/<int:movie_id>/delete", methods=['GET'])
  @requires_auth('full:executive-producer')
  def delete_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    error_flag = False
    
    if movie is None:
      abort(404)
    try:
      movie.delete()
    except:
      error_flag = True

    if error_flag: 
      flash('An error occurred. The movie could not be deleted.')
      abort(422)

    if not error_flag:
      flash('The movie was successfully deleted')

    return render_template('pages/home.html'), 204

  '''
  	movie = Movie.query.get(movie_id)
  	
  	if movie is None:
  	  abort(404)
  	try:
  	  movie.delete()
  	  return jsonify({
        'success': True,
        'deleted': movie_id
        })
  	except:
  	  abort(422)
  '''

  @app.route("/actors/<int:actor_id>/delete", methods=['GET'])
  @requires_auth('full:executive-producer')
  def delete_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)
    error_flag = False
    
    if actor is None:
      abort(404)
    try:
      actor.delete()
    except:
      error_flag = True

    if error_flag: 
      flash('An error occurred. The actor could not be deleted.')
      abort(422)

    if not error_flag:
      flash('The actor was successfully deleted')

    return render_template('pages/home.html'), 204

  '''
  	actor = Actor.query.get(actor_id)
  	
  	if actor is None:
  	  abort(404)
  	
  	try:
  	  actor.delete()
  	  return jsonify({
        'success': True,
        'deleted': actor_id
        })
  	except:
  	  abort(422)
'''

  @app.errorhandler(404)
  def not_found(error):
    return render_template('errors/404.html'), 404

  @app.errorhandler(400)
  def not_found(error):
    return render_template('errors/400.html'), 400

  @app.errorhandler(422)
  def not_found(error):
    return render_template('errors/422.html'), 422

  @app.errorhandler(401)
  def not_found(error):
    return render_template('errors/401.html'), 401

  @app.errorhandler(500)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "there is a problem on the server side"
      }), 500


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)