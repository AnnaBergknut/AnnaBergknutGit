""" Transitions 
this is where everything will be happening. these are the funktions that main will call on.
these funtions will call on the oter classes to make adustmaent and run the simulation."""
import Places
import Resources

class House:
    """ randomly decie if one or two workerd will join.
    if we have a produckt and a worker the worker will get more life
    if we have a produckt and two workers then three workers will walk out."""
    def __init__(self):
        """ My attributes """
        self._road = Places.Roads()  
    
    def checkResourcesHouse(self):
        """ check if we places have the resources that we need. 
        if we are missing resources we will skip this thing."""
        print("hi") # all of the print hi is tempoary just a place holder until i start coding   
        
    def life(self):
        """ start with checkResources the check if we have one worker or two then do the things """
        print("hi")
        
class Foodhall:
    """ workers eat food and change life dependign on how the quality food is."""
    def __init__(self):
        """ My attributes """
        print("hi")
        
    def checkResourcesFoodhall():
        """ check if we places have the resources that we need. 
        if we are missing resources we will skip this thing."""
        print("hi")
        
    def consume():
        """ change life to worker depending on quality of food. 
        when checking food qualirt we creat the quality in resource food"""
        print("hi")
        
class Feild:
    """ creat food and add it to list/q in places and lower life of worker. """
    def __init__(self):
        """ My attributes """
        print("hi")
        
    def checkResourcesFeild():
        """ check if we places have the resources that we need.
        if we are missing resources we will skip this thing."""
        print("hi")
        
    def produse():
        """ creat food and add it to list/q in places and lower life of worker. run accident too"""
        print("hi")
        
class Factory:
    """ creat product and add it to list/q in places and lower life of worker. """
    def __init__(self):
        """ My attributes """
        print("hi")
        
    def checkResourcesFactory():
        """ check if we places have the resources that we need.
        if we are missing resources we will skip this thing."""
        print("hi")
        
    def produse():
        """ creat product and add it to list/q in places and lower life of worker. run accident too. """
        print("hi")
        