import json
from node import *


#
# A method that returns a dictionary structure
# of a JSON file
#   
def get_json_data():
    with open('data.json') as json_data:
        data = json.load(json_data)
        json_data.close()
        return data

#
# A method to convert the JSON data file
# into a graph data structure using my
# node class
#
def convert_json_to_graph():
    data = get_json_data()
    #add all actors to graph data structure
    graph = {}
    for element in data[0].keys():
        node_type = data[0][element]['json_class']
        actor_name = data[0][element]['name']
        actor = Node(node_type, actor_name)
        actor_age = data[0][element]['age']
        actor.setAge(actor_age)
        for film in data[0][element]['movies']:
            actor.adjacentVertices.append(film)
        graph[actor_name] = actor
    #add all films to graph data structure
    for element in data[1].keys():
        node_type = data[1][element]['json_class']
        movie_name = data[1][element]['name']
        movie = Node(node_type, movie_name)
        revenue = data[1][element]['box_office']
        movie.setRevenue(revenue)
        for actor in data[1][element]['actors']:
            movie.adjacentVertices.append(actor)
        graph[movie_name] = movie  
    return graph