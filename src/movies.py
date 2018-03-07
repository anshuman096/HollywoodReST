from flask import jsonify
from flask import abort


#
# Method that will get the valid movies based upon
# user specified queries and boolean operators
#
def get_movies_list(queries, bool_operators, data):
    movie_list = get_movie_query_elements(queries.get(), data)
    while queries.empty() == False:
        query_list = get_movie_query_elements(queries.get(), data)
        bool_operator = bool_operators.get()
        if bool_operator == '&':
            movie_list = [i for i in movie_list for j in query_list if i['name'] == j['name']]
        else:
            final_list = [] 
            movie_list.extend(query_list)
            for dictionary in movie_list:
                if dict not in final_list:
                    final_list.append(dictionary)
            movie_list = final_list
    return jsonify(movie_list)


#
# Method that splits a query into its parameter name and value
# then returns all movie elements with the relevant information
#
def get_movie_query_elements(query, data):
    query_vals = query.split('=')
    query_list = []
    if query_vals[0] == 'name':
        query_list = get_movie_by_name(query_vals[1], data)
    elif query_vals[0] == 'box_office':
        query_list = get_movie_by_box_office(int(query_vals[1]), data)
    elif query_vals[0] == 'year':
        query_list = get_movies_by_year(int(query_vals[1]), data)
    else:
        query_list = get_actors_by_film(query_vals[1], data)
    return query_list



#
# Method that returns all movie JSON elements with
# the movie_name 
#
def get_movie_by_name(movie_name, data):
    movies_list = []
    for element in data.keys():
        if movie_name in element:
            movies_list.append(data[element])
    if not movies_list:
        abort(400) # movie not in data
    else:
        return movies_list
    
#
# Method that returns all movie JSON elements with
# the same box_office 
#    
def get_movie_by_box_office(box_office, data):
    movies_list = []
    for element in data.keys():
        if data[element]['box_office'] == box_office:
            movies_list.append(data[element])
    if not movies_list:
        abort(400)
    else:
        return movies_list

#
# Method that returns all movie JSON elements in
# the same year
#    
def get_movies_by_year(year, data):
    movies_list = []
    for element in data.keys():
        if data[element]['year'] == year:
            movies_list.append(data[element])
    if not movies_list:
        abort(400)
    else:
        return movies_list

#
# Method that returns all movie JSON elements with
# the actor_name in cast 
#  
def get_actors_by_film(actor_name, data):
    movies_list = []
    for element in data.keys():
        cast = data[element]['actors']
        for cast_member in cast:
            if actor_name in cast_member:
                movies_list.append(data[element])
                break
    if not movies_list:
        abort(400)
    else:
        return movies_list
    
    
    



#
# A method to create an movie element for 
# the JSON table in memory. Only used for
# POST HTTP Requests
#
def create_movie(modification, data):
    movie_name = modification['name']
    if movie_name in data.keys():
        modify_movie(movie_name, modification, data)
    else:
        data[movie_name] = modification
        return jsonify(data[movie_name])


#
# A method to modify an already existing movie 
# element from the JSON table in memory. Can be 
# used for POST and PUT HTTP Requests
#
def modify_movie(name, modification, data):
    element = data[name]
    for key in modification.keys():
        element[key] = modification.get(key)
    return jsonify(element)
    