from flask import jsonify
from flask import abort

#
# Method that will get the valid actors based upon
# user specified queries and boolean operators
# 
# https://stackoverflow.com/questions/23030106/intersection-of-two-lists-of-dict-python
# https://www.geeksforgeeks.org/python-remove-duplicates-list/
#
def get_actors_list(queries, bool_operators, data):
    actor_list = get_actor_query_elements(queries.get(), data)
    while queries.empty() == False:
        query_list = get_actor_query_elements(queries.get(), data)
        bool_operator = bool_operators.get()
        if bool_operator == '&':
            actor_list = [i for i in actor_list for j in query_list if i['name'] == j['name']]
        else:
            final_list = [] 
            actor_list.extend(query_list)
            for dictionary in actor_list:
                if dict not in final_list:
                    final_list.append(dictionary)
            actor_list = final_list
    return jsonify(actor_list)
    
            
                

#
# Method that splits a query into its parameter name and value
# then returns all actor elements with the relevant information
#
def get_actor_query_elements(query, data):
    query_vals = query.split('=')
    query_list = []
    if query_vals[0] == 'name':
        query_list = get_actors_by_name(query_vals[1], data)
    elif query_vals[0] == 'age':
        query_list = get_actors_by_age(int(query_vals[1]), data)
    elif query_vals[0] == 'total_gross':
        query_list = get_actors_by_gross(int(query_vals[1]), data)
    else:
        query_list = get_actors_by_film(query_vals[1], data)
    return query_list





#
# Method that returns all actor JSON elements with
# the actor_name 
#
def get_actors_by_name(actor_name, data):
    actors_list = []
    for element in data.keys():
        if actor_name in element:
            actors_list.append(data[element])
    if not actors_list:
        abort(400) # actor not in data
    else:
        return actors_list

#
# Method that returns all actor JSON elements with
# the actor_age 
#  
def get_actors_by_age(actor_age, data):
    actors_list = []
    for element in data.keys():
        if data[element]['age'] == actor_age:
            actors_list.append(data[element])
    if not actors_list:
        abort(400)
    else:
        return actors_list
 
#
# Method that returns all actor JSON elements >=
# the actor_gross 
#   
def get_actors_by_gross(actor_gross, data):
    actors_list = []
    for element in data.keys():
        if data[element]['total_gross'] == actor_gross:
            actors_list.append(data[element])
    if not actors_list:
        abort(400)
    else:
        return actors_list

#
# Method that returns all actor JSON elements with
# the actor_film
#  
def get_actors_by_film(actor_film, data):
    actors_list = []
    for element in data.keys():
        filmography = data[element]['movies']
        for film in filmography:
            if actor_film in film:
                actors_list.append(data[element])
                break
    if not actors_list:
        abort(400)
    else:
        return actors_list
    

#
# A method to create an actor element for 
# the JSON table in memory. Only used for
# POST HTTP Requests
#
def create_actor(modification, data):
    actor_name = modification['name']
    if actor_name in data.keys():
        modify_actor(actor_name, modification, data)
    else:
        data[actor_name] = modification
        return jsonify(data[actor_name])


#
# A method to modify an already existing actor 
# element from the JSON table in memory. Can be 
# used for POST and PUT HTTP Requests
#
def modify_actor(name, modification, data):
    element = data[name] 
    for key in modification.keys():
        element[key] = modification.get(key) 
    return jsonify(element)

