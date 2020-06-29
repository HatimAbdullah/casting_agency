import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class TriviaTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "betadb"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.sample_actor = {
        'name': 'joe mad man',
        'gender': 'large male',
        'age': 10,
        'place_of_birth': 'swiss',
        'contact': '128-man-is-big',
        'image_link': 'image.com.jpg',
        'has_bio': True,
        'bio': 'not for that i wont'
        }

        self.sample_movie = {
        'name': 'Thinking of a mster plan, and start your mission .. leave your residence, Thinking how you could get some dead presidents',
        'release_date': 'next fall',
        'image_link': 'image.com.png',
        'film_summary': 'it was very sad once it ended'
        }

        self.casting_assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4YnJxTVBfWVpZcjYtMmQxblRiRiJ9.eyJpc3MiOiJodHRwczovL2Zpc2hsYW5kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWY4YmQyYTM1MmQ4ZjAwMTNjM2ViMGMiLCJhdWQiOlsiY2FzdGluZ19hZ2VuY3kiLCJodHRwczovL2Zpc2hsYW5kLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTM0NDIwNzQsImV4cCI6MTU5MzUyODQ3NCwiYXpwIjoiOUNCdWhhOFU2bE5IbVM3eHA1U2pEVEV6QTRZdVRMa0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicmVhZDpjYXN0aW5nLWFzc2lzdGFudCJdfQ.UK0BgzkUeIp3Twcn0c1xvf-oqigJX74r7_I6l97pIIPTYhrmoN7YBEwNGVNncFoKM0dwUzoyMvfLADBO3t1HwU-AEg7U9tv4xIdEogscNKAZdxdNB-5hcPvHMXdyJ2HTYbCixxpaiuVZMfbWQcC83vPj0MihTh-SVQ_7Q9Z9Vya0NS7_3t6687cBmYal1XQ6SDdPBib4H9b8x6UoI6FCy-Yoh543WutWMyk0vIUpMzhom2Zutsg-77wsBnCwcJj6Ch4_6t-BPDZILVs4eeH7ogsmxBqDib5c428AMooKLiw7rnMawF8sCPqRYb6reiNH0NKKhskrpJzMK11WWnsJrQ"
        self.casting_director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4YnJxTVBfWVpZcjYtMmQxblRiRiJ9.eyJpc3MiOiJodHRwczovL2Zpc2hsYW5kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWY5ODllNGU4MjRhNTAwMTkyMWEwNDEiLCJhdWQiOlsiY2FzdGluZ19hZ2VuY3kiLCJodHRwczovL2Zpc2hsYW5kLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTM0NDIxNTUsImV4cCI6MTU5MzUyODU1NSwiYXpwIjoiOUNCdWhhOFU2bE5IbVM3eHA1U2pEVEV6QTRZdVRMa0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicmVhZDpjYXN0aW5nLWFzc2lzdGFudCIsIndyaXRlOmNhc3RpbmctZGlyZWN0b3IiXX0.Us8yfBhUF0rawGiWkkAU-Xi3Cfh-E-gCtcanbLKI5Kr6O0I9b5J-vFkKoY0y8wTRYm12qQ34y4CZi5qmxFauAGW0KXhYtEs25yPPbhR9KEVR2-EGDz3shDWF673B7ZRkkwLAX7paq2Jp5ISccohY_Cdy3CaSNbGDNF8E8tJaKoEQ7nWGG7clCPjTfTtsGaGAnxD1mYVIC3Kx8GWMOI8gUFqdXElAApQjbCTQ2l22YmQPYAGwmjhDAz6Wl1_guou590kM6GGREReuP7zeAYk8YGDt35gi1Y2TwpPLPgTJM5ouEdYg7xKfP14IAfeHJccReJITv1vsXAlVE4rMXvUrsA"
        self.executive_producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4YnJxTVBfWVpZcjYtMmQxblRiRiJ9.eyJpc3MiOiJodHRwczovL2Zpc2hsYW5kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWY4YmVmYzg5ODE3NDAwMTNkOGM4MTMiLCJhdWQiOlsiY2FzdGluZ19hZ2VuY3kiLCJodHRwczovL2Zpc2hsYW5kLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTM0NDIyMjQsImV4cCI6MTU5MzUyODYyNCwiYXpwIjoiOUNCdWhhOFU2bE5IbVM3eHA1U2pEVEV6QTRZdVRMa0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZnVsbDpleGVjdXRpdmUtcHJvZHVjZXIiLCJyZWFkOmNhc3RpbmctYXNzaXN0YW50Iiwid3JpdGU6Y2FzdGluZy1kaXJlY3RvciJdfQ.sjw03wlQr_RQGP6Bb-SXPX-rAzB-WnQ8ySR6EwU5hY4DphHNbn7Cynz4yjzu3NStYz6tILiGp6SI48xAi47OhBkg--6eetp37aff_G3B6V215zvdEEM6cZl8BEW8wGWmIYBYhvIpsmjuXdWjsHV9TDXcWPND1AXBjyxTtOM7jJNvdfJzbcegmslYYtLKVOnr98wTs2L5vYYWmfF48hFcqbiKaOAe-x7j8Qnbj85FWlwJ888u9kcu2S4VFQvKX5DA26Lgf5IXRqqKHRXsoKPltMhvxuO07HNHWOtmUtINQwwGJ4zXSPdEOsGNUY7Z1tmaBH70RyrFrntLzRiD7KqQgw"


    
    def tearDown(self):
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_actorsـunauthorized(self):
        response = self.client().get('/actors')
        
        self.assertEqual(response.status_code, 401)
       

    def test_get_actorsـauthorized(self):
        c = self.client()
        c.set_cookie('localhost:5000/actors', 'user_token', self.casting_assistant_token)
        response = c.get('/actors')
      
        self.assertEqual(response.status_code, 200)
    

    def test_get_moviesـunauthorized(self):
        response = self.client().get('/movies')
        
        self.assertEqual(response.status_code, 401)
    

    def test_get_moviesـauthorized(self):
        c = self.client()
        c.set_cookie('localhost:5000/movies', 'user_token', self.casting_assistant_token)
        response = c.get('/movies')
      
        self.assertEqual(response.status_code, 200)

    
    def test_post_movieـunauthorized(self):
        c = self.client()
        response = c.post(
        	'/movies',
        	data = dict(name="yo", release_date="ho", image_link="wo", film_summary="no"),
        	)

        self.assertEqual(response.status_code, 401)


    def test_post_movieـauthorized(self):
        c = self.client()
        c.set_cookie('localhost:5000/movies', 'user_token', self.casting_director_token)
        response = c.post(
        	'/movies',
        	data = dict(name="yo", release_date="ho", image_link="wo", film_summary="no"),
        	)

        self.assertEqual(response.status_code, 201)


    def test_post_actorـunauthorized(self):
        c = self.client()
        c.set_cookie('localhost:5000/actors', 'user_token', self.casting_assistant_token)
        response = c.post(
        	'/actors',
        	data = dict(name="yo", gender="ho", age=22, place_of_birth="no", contact="do", image_link="to", has_bio=True, bio="go"),
        	)
        
        self.assertEqual(response.status_code, 401)


    def test_post_actorـauthorized(self):
        c = self.client()
        c.set_cookie('localhost:5000/actors', 'user_token', self.casting_director_token)
        response = c.post(
        	'/actors',
        	data = dict(name="yo", gender="ho", age=22, place_of_birth="no", contact="do", image_link="to", has_bio=True, bio="go"),
        	)
        
        self.assertEqual(response.status_code, 201)


    def test_get_actorـunauthorized(self):
        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id
        response = self.client().get(f'/actors/{actor_id}')
        
        self.assertEqual(response.status_code, 401)
    

    def test_get_actorـnot_found(self):
        c = self.client()
        c.set_cookie('localhost:5000/actors', 'user_token', self.casting_assistant_token)
        response = c.get('/actors/14568')
      
        self.assertEqual(response.status_code, 401)

       
    def test_get_actorـauthorized(self):
        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id
        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.casting_assistant_token)
        response = c.get(f'/actors/{actor_id}')
      
        self.assertEqual(response.status_code, 200)
    
    
    def test_get_movieـunauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id
        response = self.client().get(f'/movies/{movie_id}')
        
        self.assertEqual(response.status_code, 401)
    

    def test_get_movieـnot_found(self):
        c = self.client()
        c.set_cookie('localhost:5000/movies', 'user_token', self.casting_assistant_token)
        response = c.get('/movies/455655')
      
        self.assertEqual(response.status_code, 401)
    

    def test_get_movieـauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id
        c = self.client()
        c.set_cookie('localhost:5000/movies', 'user_token', self.casting_assistant_token)
        response = c.get(f'/movies/{movie_id}')
      
        self.assertEqual(response.status_code, 200)


    def test_cast_actorـunauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id

        c = self.client()
        c.set_cookie('localhost:5000/cast-actor-to-movie', 'user_token', self.casting_assistant_token)
        response = c.post(
        	'/cast-actor-to-movie',
        	data = dict(actor_id=actor_id, movie_id=movie_id),
        	)
        
        self.assertEqual(response.status_code, 401)


    def test_cast_actorـauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id

        c = self.client()
        c.set_cookie('localhost:5000/cast-actor-to-movie', 'user_token', self.casting_director_token)
        response = c.post(
        	'/cast-actor-to-movie',
        	data = dict(actor_id=actor_id, movie_id=movie_id),
        	)
        
        self.assertEqual(response.status_code, 201)

    
    def test_fire_actorـunauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id

        movie.cast.append(actor)
        movie.update()

        c = self.client()
        c.set_cookie('localhost:5000/fire-actor-from-movie', 'user_token', self.casting_assistant_token)
        response = c.get(f'/fire-actor-from-movie/{movie_id}/{actor_id}')
        
        self.assertEqual(response.status_code, 401)


    def test_fire_actorـauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id

        movie.cast.append(actor)
        movie.update()

        c = self.client()
        c.set_cookie('localhost:5000/fire-actor-from-movie', 'user_token', self.casting_director_token)
        response = c.get(f'/fire-actor-from-movie/{movie_id}/{actor_id}')
        
        self.assertEqual(response.status_code, 200)



    def test_patch_movieـunauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.casting_assistant_token)
        response = c.post(
        	f'/movies/{movie_id}/patch',
        	data = dict(name="yo", release_date="ho", image_link="wo", film_summary="no"),
        	)

        self.assertEqual(response.status_code, 401)


    def test_patch_movieـauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.casting_director_token)
        response = c.post(
        	f'/movies/{movie_id}/patch',
        	data = dict(name="yo", release_date="ho", image_link="wo", film_summary="no"),
        	)

        self.assertEqual(response.status_code, 202)


    def test_patch_actorـunauthorized(self):
        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id

        c = self.client()
        response = c.post(
        	f'/actors/{actor_id}/patch',
        	data = dict(name="yo", gender="ho", age=22, place_of_birth="no", contact="do", image_link="to", has_bio=True, bio="go"),
        	)
        
        self.assertEqual(response.status_code, 401)


    def test_patch_actorـauthorized(self):
        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id

        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.casting_director_token)
        response = c.post(
        	f'/actors/{actor_id}/patch',
        	data = dict(name="yo", gender="ho", age=22, place_of_birth="no", contact="do", image_link="to", has_bio=True, bio="go"),
        	)
        
        self.assertEqual(response.status_code, 202)

    def test_delete_movieـunauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.casting_director_token)
        response = c.get(f'/movies/{movie_id}/delete')

        self.assertEqual(response.status_code, 401)


    def test_delete_actorـunauthorized(self):
        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id
        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.casting_director_token)
        response = c.get(f'/actors/{actor_id}/delete')

        self.assertEqual(response.status_code, 401)

    
    def test_delete_movie_not_found(self):
        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.executive_producer_token)
        response = c.get('/movies/1845858/delete')

        self.assertEqual(response.status_code, 401)


    def test_delete_actor_not_found(self):
        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.executive_producer_token)
        response = c.get('/actors/14877488/delete')

        self.assertEqual(response.status_code, 401)


    def test_delete_movieـauthorized(self):
        movie = Movie(name=self.sample_movie['name'], release_date=self.sample_movie['release_date'], 
                       image_link=self.sample_movie['image_link'], film_summary=self.sample_movie['film_summary'])
        movie.insert()
        movie_id = movie.id

        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.executive_producer_token)
        response = c.get(f'/movies/{movie_id}/delete')

        self.assertEqual(response.status_code, 204)


    def test_delete_actorـauthorized(self):
        actor = Actor(name=self.sample_actor['name'], age=self.sample_actor['age'],
                            gender=self.sample_actor['gender'], place_of_birth=self.sample_actor['place_of_birth'], contact=self.sample_actor['contact'],
                            has_bio=self.sample_actor['has_bio'], bio=self.sample_actor['bio'], image_link=self.sample_actor['image_link'])
        actor.insert()
        actor_id = actor.id

        c = self.client()
        c.set_cookie('localhost:5000', 'user_token', self.executive_producer_token)
        response = c.get(f'/actors/{actor_id}/delete')

        self.assertEqual(response.status_code, 204)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
