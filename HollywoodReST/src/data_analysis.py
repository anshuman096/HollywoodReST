import json
import hollywood
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants.constants import alpha

#
# A helper function for get_max_hub_actor. This function
# calculates the number of connections for an individual actor.
#
def get_num_connections(name, data):
    connections = set()
    # first get all unique connections from JSON movie elements
    for movie in data[1].keys():
        if name in data[1][movie]["actors"] and movie not in data[0][name]["movies"]:
            # a movie the actor worked in that is NOT listed in his/her filmography
            for actor in data[1][movie]["actors"]:
                connections.add(actor) 
    # second get all unique connections from JSON actor elements
    filmography = data[0][name]["movies"]
    for actor_name in data[0].keys():
        if name != actor_name:
            for movie in data[0][actor_name]["movies"]:
                if movie in filmography:
                    connections.add(actor_name)
                    break
    return len(connections)

#
# A method that returns all 'hub' actors within the given JSON
# data file. A 'hub' actor is an actor with the most number of
# connections via movies with other actors. Method returns a list
# with the actors that have the most hub connections
#            
def get_max_hub_actor(data):
    # iterate through all actors
    max_connections = 0 # max number of connections of an actor
    max_actors = []
    max_actor = ''
    for actor in data[0].keys():
        num_connections = get_num_connections(actor, data)
        max_connections = max(max_connections, num_connections)
        if max_connections == num_connections:
            #max_connections was updated
            max_actor = actor
            max_actors.append(actor)
    return max_actors


def display_top_hub_actors(data):
    top_actors = get_max_hub_actor(data)
    top_connections = []
    for actor in top_actors:
        top_connections.append(get_num_connections(actor, data))
    for i in range(len(top_actors)):
        print top_actors[i] + ": " + str(top_connections[i])
    num_actors = range(len(top_connections))
    plt.figure()
    plt.bar(num_actors, top_connections, align='center', alpha = 0.5)
    plt.title('Top 7 Hub Actors')
    plt.xlabel('Actors')
    plt.ylabel('Number of Connections')
    plt.savefig('max_num_connections.png')
    plt.show()


#
# Helper function to print out age group based on
# index
#
def get_age_group(age_index):
    return (age_index * 10, (age_index + 1) * 10)

#
# Method to calculate the gross income of each age group of 
# actors (age groups are every 10 years). Method prints
# a statement for richest age group then returns list with
# all of the age group gross incomes.
#
def get_richest_age_group(data):
    age_groups = [0] * 10
    for actor in data[0].keys():
        actor_age = data[0][actor]['age']
        age_groups[actor_age/10] = age_groups[actor_age/10] + data[0][actor]['total_gross']
    max_age_index = age_groups.index(max(age_groups))
    age_group = get_age_group(max_age_index)
    print "ages " + str(age_group[0]) + " to " + str(age_group[1]) + ": " + str(age_groups[max_age_index])
    return age_groups

#
# A method to create a matplotlib figure
# for the age groups and their income
#
def display_age_groups(age_groups):
    num_groups = range(len(age_groups))
    plt.figure()
    plt.plot(num_groups, age_groups)
    plt.xlabel("Age Group")
    plt.ylabel("Overall Gross Earning")
    plt.title("Gross Income by Age Group")
    plt.savefig('age_group.png')
    plt.show()
    

    
data = hollywood.get_json_data()
display_top_hub_actors(data)
age_groups = get_richest_age_group(data)
display_age_groups(age_groups)
