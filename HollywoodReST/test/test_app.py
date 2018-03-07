import json
import unittest
import requests
from flask import Flask
from flask import jsonify
from flask_testing import TestCase
#from flask_testing import LiveServerTestCase
import flask_testing

class MyTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        app.config['LIVESERVER_TIMEOUT'] = 5
        return app

    def test_server(self):
        print "TEST SERVER"
        response = requests.get('http://localhost:5000/actors?name=Bruce')
        self.assertEqual(response.status_code, 200)




    def test_get_actor(self):
        print "GET ACTOR"
        response = requests.get('http://localhost:5000/actors/Gary_Oldman')
        data = json.loads(response.content)
        self.assertEqual(data['name'], "Gary Oldman")
        
        response = requests.get('http://localhost:5000/actors?name=Bruce')
        data = json.loads(response.content)
        self.assertEqual(data[0]['name'], "Bruce Willis")
        self.assertEqual(data[1]['name'], "Bruce Dern")
        
        response = requests.get('http://localhost:5000/actors?name=Morgan&age=79')
        data = json.loads(response.content)
        self.assertEqual(data[0]['name'], "Morgan Freeman")
        
        # Test this live, Flask Unit testing cannot parse the '|' character
        response = requests.get('http://localhost:5000/actors?name=Bruce&age=61|name=Morgan')
        self.assertEqual(response.status_code, 500)
        
        
        
        
        
    def test_put_actor(self):
        print "PUT ACTOR"
        header = {"Content-Type":"application/json"}
        response = requests.put('http://localhost:5000/actors/Gary_Oldman', headers = header, data = '{"age":55}')
        r = requests.get('http://localhost:5000/actors/Gary_Oldman')
        data = json.loads(r.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['age'], 55)
        
        response = requests.put('http://localhost:5000/actors/Bruce_Willis', headers = header, data = '{"age":20}')
        r = requests.get('http://localhost:5000/actors/Bruce_Willis')
        data = json.loads(r.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['age'], 20)
        
        response = requests.put('http://localhost:5000/actors/Morgan_Freeman', headers = header, data = '{"total_gross":12456}')
        r = requests.get('http://localhost:5000/actors/Morgan_Freeman')
        data = json.loads(r.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_gross'], 12456)
        
        
    def test_post_actor(self):
        print "POST ACTOR"
        header = {"Content-Type":"application/json"}
        payload = '{"age":21, "json_class": "Actor", "name":"Anshuman Dikhit", "total_gross":1234}'
        response = requests.post('http://localhost:5000/actors', headers = header, data = payload)
        self.assertEqual(response.status_code, 201)
        r = requests.get("http://localhost:5000/actors/Anshuman_Dikhit")
        data = json.loads(r.content)
        self.assertEqual(data['name'], "Anshuman Dikhit")
        
        payload = '{"age":41, "json_class": "Actor", "name":"Chadwick Boseman", "total_gross":709000000}'
        response = requests.post('http://localhost:5000/actors', headers = header, data = payload)
        self.assertEqual(response.status_code, 201)
        r = requests.get("http://localhost:5000/actors/Chadwick_Boseman")
        data = json.loads(r.content)
        self.assertEqual(data['name'], "Chadwick Boseman")
        
    def test_delete_actor(self):
        print "DELETE ACTOR"
        header = {"Content-Type":"application/json"}
        payload = '{"age":21, "json_class": "Actor", "name":"Anshuman Dikhit", "total_gross":1234}'
        requests.post('http://localhost:5000/actors', headers = header, data = payload)

        request = requests.delete('http://localhost:5000/actors/Anshuman_Dikhit', headers = header)
        self.assertEqual(request.status_code, 200)
        
        request = requests.delete('http://localhost:5000/actors/Anshuman_Dikhit', headers = header)
        self.assertEqual(request.status_code, 400)
        
    def test_movie(self):
        print("GET MOVIE")
        response = requests.get('http://localhost:5000/movies/The_Bye_Bye_Man')
        data = json.loads(response.content)
        self.assertEqual(data['name'], "The Bye Bye Man")
        
        response = requests.get('http://localhost:5000/movies/Ed')
        data = json.loads(response.content)
        self.assertEqual(data['name'], "Ed")
        
        response = requests.get('http://localhost:5000/movies?name=Aphrodite')
        data = json.loads(response.content)
        self.assertEqual(data[0]['name'], "Mighty Aphrodite")
        
        response = requests.get('http://localhost:5000/movies?year=1990')
        data = json.loads(response.content)
        self.assertEqual(len(data[0]), 6)
        
        response = requests.get('http://localhost:5000/movies?actors=Bruce&year=1998')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        
        
    def test_put_movie(self):
        print("PUT MOVIE")
        header = {"Content-Type":"application/json"}
        response = requests.put('http://localhost:5000/movies/Hudson_Hawk', headers = header, data = '{"year":2017}')
        self.assertEqual(response.status_code, 200)
        r = requests.get('http://localhost:5000/movies/Hudson_Hawk')
        data = json.loads(r.content)
        self.assertEqual(data['year'], 2017)
        
        response = requests.put('http://localhost:5000/movies/Mortal_Thoughts', headers = header, data = '{"box_office":2017}')
        self.assertEqual(response.status_code, 200)
        r = requests.get('http://localhost:5000/movies/Mortal_Thoughts')
        data = json.loads(r.content)
        self.assertEqual(data['box_office'], 2017)
        
        
    def test_post_movie(self):
        print("POST MOVIE")
        header = {"Content-Type":"application/json"}
        payload = '{"json_class":"Movie", "name": "Black Panther", "year":2018, "box_office":709000000}'
        response = requests.post('http://localhost:5000/movies', headers = header, data = payload)
        self.assertEqual(response.status_code, 201)
        r = requests.get("http://localhost:5000/movies/Black_Panther")
        data = json.loads(r.content)
        self.assertEqual(data['name'], "Black Panther")
        
        payload = '{"json_class":"Movie", "name": "Thor Ragnarok", "year":2017, "box_office":629000000}'
        response = requests.post('http://localhost:5000/movies', headers = header, data = payload)
        self.assertEqual(response.status_code, 201)
        r = requests.get("http://localhost:5000/movies/Thor_Ragnarok")
        data = json.loads(r.content)
        self.assertEqual(data['name'], "Thor Ragnarok")
        
        
    def test_delete_movie(self):
        print("DELETE MOVIE")
        header = {"Content-Type":"application/json"}
        payload = '{"json_class":"Movie", "name": "Black Panther", "year":2018, "box_office":709000000}'
        requests.post('http://localhost:5000/movies', headers = header, data = payload)
               
        request = requests.delete('http://localhost:5000/movies/Black_Panther', headers = header)
        self.assertEqual(request.status_code, 200)
        
        request = requests.delete('http://localhost:5000/movies/Black_Panther', headers = header)
        self.assertEqual(request.status_code, 400)
        
        
        


# your test cases

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


