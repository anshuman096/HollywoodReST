#!/usr/bin/env python

import json
from sets import Set

data = json.loads(open("data.json").read())
actors = data[0]
movies = data[1]

actor_id = 1
id = 1000

myNodes = []
myEdges = []

# this python file prints out nodes and edges that can be inputted
# into a vis.js script and rendered into a visual graph. Most of the HTML
# code for displaying the graph was taken from vis.js source code
# view-source:http://visjs.org/examples/network/nodeStyles/colors.html
#
 

# 100 actors and their movies
for name in actors.keys():
    myNodes.append({ 'id':actor_id, 'label': name, 'type' : 'actor', 'age' : actors[name]['age'] })
    #  10  movies per actor max for better visualization
    max_for_actor = 10
    for mname in actors[name]['movies']:
        if (max_for_actor <= 0):
            break
        if (mname in movies):
            myNodes.append({ 'id':id, 'label':mname, 'type' : 'movie', 'gross' : movies[mname]['box_office']})
            myEdges.append({'to': id,'from':actor_id})
            id += 1
        max_for_actor -= 1
    actor_id += 1
    #Stop at 100 actors 
    if (actor_id == 100):
        break

#
# Print the actor and movie information for the nodes of graph
#
for node in myNodes:
    if (node['type'] == "actor"):
        star_name = node['label'] + "(" + str(node['age']) + ")"
        print ("{id : %s, label : %c%s%c, shape : \'star\', size : 35, color : \'orange\'},"%(node['id'] , "\"", star_name, "\""))
    else:
        movie_name = node['label'] + "(" + str(node['gross']) + ")"
        print ("{id : %s, label : %c%s%c, shape : \'square\'},"%(node['id'], "\"", movie_name, "\""))

#
# Print all the edges
#
for edge in myEdges:
    print ("{from : %s, to : %s},"%(edge['from'], edge['to']))


