#!/usr/bin/env python
from flask import *
from actor import get_actors_list
from actor import create_actor
from actor import modify_actor
from movies import get_movies_list
from movies import create_movie
from movies import modify_movie
import Queue as queue
import hollywood

data = hollywood.get_json_data()
app = Flask(__name__)


@app.route('/actors', methods = ['GET', 'POST'])
def get_actors():
    global data
    if request.method == 'GET':
        query_string = request.query_string
        if len(query_string) == 0:
            abort(400)
        bool_operators = get_bool_operators(query_string)
        queries = get_query_list(query_string)
        return get_actors_list(queries, bool_operators, data[0])
    elif request.method == 'POST':
        return create_actor(request.get_json(), data[0]), 201
 
 
   
@app.route('/actors/<actor_name>', methods = ['GET', 'PUT', 'DELETE'])
def actor(actor_name):
    global data
    name = actor_name.replace("_", " ")
    if request.method == 'GET':
        if name not in data[0].keys():
            abort(400)
        else:
            return jsonify(data[0][name])
    elif request.method == 'PUT':
        return modify_actor(name, request.get_json(), data[0])
    else:
        try:
            del data[0][name]
        except Exception:
            abort(400)
        return jsonify(data)






@app.route('/movies', methods = ['GET', 'POST'])
def get_movies():
    global data
    if request.method == 'GET':
        query_string = request.query_string
        if len(query_string) == 0:
            abort(400)
        bool_operators = get_bool_operators(query_string)
        queries = get_query_list(query_string)
        return get_movies_list(queries, bool_operators, data[1])
    elif request.method == 'POST':
        return create_movie(request.get_json(), data[1]), 201
    
        

@app.route('/movies/<movie_name>', methods = ['GET', 'PUT', 'DELETE'])
def movie(movie_name):
    global data
    name = movie_name.replace("_", " ")
    if request.method == 'GET':
        if name not in data[1].keys():
            abort(400)
        else:
            return jsonify(data[1][name])
    elif request.method == 'PUT':
        return modify_movie(name, request.get_json(), data[1])
    else:
        try:
            del data[1][name]
        except Exception:
            abort(400)
        return jsonify(data)
    
#
# Took most of the code from vis.js library source code
# view-source:http://visjs.org/examples/network/nodeStyles/colors.html
#
@app.route('/visualize')
def visualize():
    return open("visualize.html").read()
        
#
# A method to list out all the boolean operators in
# a url query string
#
def get_bool_operators(query_string):
    bool_operators = queue.Queue()
    for ch in query_string:
        if ch == '&' or ch == '|':
            bool_operators.put(ch)
    return bool_operators

#
# A method to list out all the queries in a 
# url query string
#
def get_query_list(query_string):
    arg_list = queue.Queue()
    arg = ""
    for char in query_string:
        if char == '&' or char == '|':
            arg_list.put(arg)
            arg = ""
            continue
        arg = arg + char
    arg_list.put(arg)
    return arg_list


if __name__ == '__main__':
    app.run(debug=True)
