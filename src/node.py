import json

class Node:
    
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.adjacentVertices = []
        self.age = 0
        self.revenue = 0
    
    

    #
    # Method to generate a key for a node to be 
    # added into a graph
    #
    def generateKey(self):
        return self.name + ':' + self.type
    
    #
    # Method to get the Actors for a movie
    # Method returns nothing if node type is not 'movie'
    #
    def getActors(self):
        if(self.type == 'Movie'):
            return self.adjacentVertices 
        
    #
    # Method to get the Filmography of an actor
    # Method returns nothing if node type is not 'actor'
    #   
    def getMovies(self):
        if(self.type == 'Actor'):
            return self.adjacentVertices

        
    #
    # Method to set the Age of an Actor node
    # Method will raise an exception if node 
    # is not of 'actor' type
    #
    #@param, the age
    #
    def setAge(self, age):
        if(self.type == 'Movie'):
            raise Exception("Invalid Type")
        self.age = age
        
    #
    # Method to set the revenue of a movie node
    # Method will raise an exception if node 
    # is not of 'movie' type
    #
    #@param, the age
    #    
    def setRevenue(self, revenue):
        if(self.type == 'Actor'):
            raise Exception("Invalid Type")
        self.revenue = revenue
        
        
    # Method that will be helpful in graph query for
    # retrieving an actors age
    #
    def getAge(self):
        return self.age
    
    # Method that will be helpful in graph query for
    # retrieving a movie's revenue
    #
    def getRevenue(self):
        return self.revenue
        
    
    #
    # a function to convert a node into a 
    # serializable JSON object
    # source: https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    #
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
    