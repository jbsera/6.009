# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 23:29:00 2021

@author: joyse
"""

#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).  See the following page for more
# information: https://py.mit.edu/fall21/notes/style


def transform_data(raw_data):
    '''
    Takes the raw data and transforms it into a dictionary with keys as tuples of actor ids 
    like (actor1, actor2) and values with the movie IDs they were in together

    '''
    new_dict=dict()
    for i in raw_data:
        new_dict[(i[0],i[1])]=i[2]
    return new_dict

def transform_data_movies0(transformed_data):
    '''
    Takes the data in the form of (actor1, actor2): movie ID and 
    transforms it into a dictionary of movieID: all actors who worked on that movie

    '''
    new_dict=dict()
    for i in transformed_data.keys():
        if transformed_data[i] not in new_dict: #if it hasn't appeared before, add the other actor to the set
            new_dict[transformed_data[i]]={i[0], i[1]}
        else: #if it has appeared, append the other actor to the set
            new_dict[transformed_data[i]].add(i[0])
            new_dict[transformed_data[i]].add(i[1])
    return new_dict


def transform_data_actors(transformed_data):
    '''
    Takes the data in the form of (actor1, actor2): movie ID and 
    transforms it into a dictionary of actor: all the movies they have been in
    '''
    new_dict=dict()
    for i in transformed_data.keys():
        if i[0] not in new_dict: #if it hasn't appeared before, add the other actor to the set
            new_dict[i[0]]={transformed_data[i]}
        else: #if it has appeared, append the other actor to the set
            new_dict[i[0]].add(transformed_data[i])
        if i[1] not in new_dict:
            new_dict[i[1]]={transformed_data[i]}
        else:
            new_dict[i[1]].add(transformed_data[i])
    return new_dict
    

def transform_data1(transformed_data):
    '''
    Takes in the transformed data from the transform_data function.
    This data is in the form (actor1, actor2): movie 
    
    This transformation is not interested in the movie ID's, 
    but just the actors who have worked together.
    
    So it takes the transformed data dictionary and returns a new dictionary 
    of actorID: set(all the actors who have worked directly with said actor)

    '''
    new_dict=dict()
    for i in transformed_data.keys():
        if i[1]!=i[0]:
            if i[0] not in new_dict: #if it hasn't appeared before, add the other actor to the set
                new_dict[i[0]]={i[1]}
            else: #if it has appeared, append the other actor to the set
                new_dict[i[0]].add(i[1])
            if i[1] not in new_dict:
                new_dict[i[1]]={i[0]}
            else:
                new_dict[i[1]].add(i[0])
    return new_dict

def transform_movies(movie_data):
    '''
    Given the movie data in the form movie title: movie ID
    Creates a new dictionary in reverse, so movie ID: movie title for convenience

    '''
    new_dict={}
    for i in movie_data.keys():
        new_dict[movie_data[i]]=i
    return new_dict



def acted_together(transformed_data, actor_id_1, actor_id_2):
    '''

    Parameters
    ----------
    transformed_data : the transformed data, in this case a dictionary
    actor_id_1 : an int representing ID
    actor_id_2 : an int representing ID

    Returns
    -------
    bool
        True if the actors worked together, false if not

    '''
    if actor_id_1==actor_id_2: #catches the case where the actors are the same person
        return True
    if (actor_id_1, actor_id_2) in transformed_data.keys() or (actor_id_2, actor_id_1) in transformed_data.keys(): #if they are listed as working together in the dictionary
        return True
    return False


def actors_with_bacon_number(transformed_data, n):
    '''
    
    Given a data set, returns a set of the actors with a bacon number of n

    '''
    transformed_data=transform_data1(transformed_data) #gets into a form with only actors
    overallset=set() #keeps track of all the actors we've seen
    
    #iterate through all the bacon numbers
    for i in range(n+1): 
        baconset=set() #resets the baconset/answer to empty for each bacon number
        if i==0: #sets the answer to 4724 since i==0 corresponds to Mr. Bacon himself
            previous_baconset={4724}
            overallset.add(4724)
            baconset.add(4724)
            
        else:
            #iterates through the actors in the previous (n-1) baconset
            for actor_id in previous_baconset: 
                #goes through all the actors that the given actor has worked with
                for actor_worked_with in transformed_data[actor_id]: 
                    if actor_worked_with not in overallset: #only add them to the baconset if they haven't appearred before
                        baconset.add(actor_worked_with)
                        overallset.add(actor_worked_with)
                        
        previous_baconset=baconset #set the previous_baconset for later iterations to the baconset we just calculated
        
        if previous_baconset==set(): #checks if we have an empty set, in which case just return it
            return previous_baconset
        
    return baconset #returns the final baconset

def finding_paths(transformed_data, overalldict, overallset, previous_baconset, actor_id):
    '''
    Helper function to find paths between actors

    Parameters
    ----------
    transformed_data : dictionary storying info about which actors have worked directly together
    overalldict : keeps track of the paths taken to get to actor ID's
    overallset : keeps track of all the actors we've seen
    previous_baconset : equal to the actors that the previous actor worked directly with
    actor_id : the actor we want to find a path to

    Returns
    -------
    A list of the shortest path from the original actor to the given actor_id

    '''
    while True: 
        baconset=set() #resets the baconset/answer to empty for each bacon number

        #iterates through the actors in the previous (n-1) baconset
        for actor in previous_baconset: 
            #goes through all the actors that the given actor has worked with
            for actor_worked_with in transformed_data[actor]: 
                if actor_worked_with in overallset: #skip over if we've already seen the actor
                    continue
                list_copy=overalldict[actor].copy()
                list_copy.append(actor_worked_with)
                overalldict[actor_worked_with]=list_copy #set the path to that actor as the path from the previous actor + the given actor

                if actor_worked_with==actor_id: #return when we've found the actor
                    return overalldict[actor_id]
                
                if actor_worked_with not in overallset: #only add them to the baconset if they haven't appearred before
                    baconset.add(actor_worked_with)
                    overallset.add(actor_worked_with)
               
        previous_baconset=baconset #set the previous_baconset for later iterations to the baconset we just calculated
        
        if previous_baconset==set(): #checks if we have an empty set, in which case just return None
            return None
        
    return None 




def bacon_path(transformed_data, actor_id):
    '''
    Given the data set and a given actor, returns a list of actor IDs 
    giving the shortest path from Kevin Bacon to the given actor

    '''
    if actor_id==4724: #in case Kevin bacon needs a path to himself
        return [4724]
    else:
        transformed_data=transform_data1(transformed_data) #gets into a form with only actors
        overalldict={4724:[4724]} #keeps track the least path to the given actor, set to Kevin Bacon
        overallset={4724} #keeps track of everyone we've seen, so far only Mr. Bacon
        previous_baconset={4724} #Bacon's baconset
        
        return finding_paths(transformed_data, overalldict, overallset, previous_baconset, actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    '''
    Given two actor ids and a database of actors who've worked together, 
    finds the shortest path of actors between them
    and returns this path as a list. 
    '''
    if actor_id_1==actor_id_2: #if the actors are the same, return a list of said actor
        return [actor_id_1]
    else:
        transformed_data=transform_data1(transformed_data) #gets into a form with only actors
        overalldict={actor_id_1:[actor_id_1]} #keeps track of the least path to the given actor, starting with actor 1
        overallset={actor_id_1} #keeps track of everyone we've seen, starting with actor 1
        previous_baconset={actor_id_1}
        return finding_paths(transformed_data, overalldict, overallset, previous_baconset, actor_id_2)

def movie_paths(transformed_data_movies, transformed_data_actors, actor_id_1, actor_id_2):
    '''

    Parameters
    ----------
    transformed_data_movies : a dictionary of the form movie ID: movie title
    transformed_data_actors : a dictionary of the form (actor1, actor2): movie worked on together
    actor_id_1 : id of the first actor
    actor_id_2 : id of the second actor

    Returns
    -------
    movie_title_path : the shortest path of movie titles connecting the actors

    '''
    actor_path=actor_to_actor_path(transformed_data_actors, actor_id_1, actor_id_2) #gets the shortest actor path
    movie_id_path=[]
    movie_title_path=[]
    
    for actors in range(0,len(actor_path)): #iterate over the shortest path
        if tuple(actor_path[actors:actors+2]) in transformed_data_actors.keys(): #find the two actors in the dictionary to get the movie id
            movie_id_path.append(transformed_data_actors[tuple(actor_path[actors:actors+2])])
        elif tuple(actor_path[actors:actors+2][::-1]) in transformed_data_actors.keys(): #find the two actors if appear in reverse order in the dictionary
            movie_id_path.append(transformed_data_actors[tuple(actor_path[actors:actors+2][::-1])])
    
    for movieID in movie_id_path: # find the corresponding titles of the given movie IDs
        movie_title_path.append(transformed_data_movies[movieID])
        
    return movie_title_path
    
    
def actor_path(transformed_data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    
    
    transformed_data_movies=transform_data_movies0(transformed_data) #gets into a form with movies: actors
    if film1==film2:
        return list(transformed_data_movies[film1])[0]
    min_path=actor_to_actor_path(transformed_data, list(transformed_data_movies[film1])[0], list(transformed_data_movies[film2])[0])
    for actor1 in transformed_data_movies[film1]:
        for actor2 in transformed_data_movies[film2]:
            actor_path=actor_to_actor_path(transformed_data, actor1, actor2)
            if len(actor_path)<len(min_path):
                min_path=actor_path
                
    if min_path==set():
        return None
    
    return min_path
    
    
    # transformed_data_actors=transform_data_actors(transformed_data) #gets into a form of actor: movies
    # print('transformed movies', transformed_data_movies)
    # print('transformed actors', transformed_data_actors)
    # if film1==film2: #if the actors are the same, return a list of said actor
    #     return transformed_data[film1][0]
    
    # else:
    #     overalldict={film1:[]} #keeps track of the least path to the given actor, starting with actor 1
    #     overallset_actors=set() #keeps track of everyone we've seen, starting with actor 1
    #     overallset_movies={film1}
    #     previous_actorset=transformed_data_movies[film1]
    #     while True: 
    #         actor_set=set() #resets the baconset/answer to empty for each bacon number
    
    #         #iterates through the actors in the previous (n-1) baconset
    #         for actor in previous_actorset: 
    #             #goes through all the actors that the given actor has worked with
    #             for movie in transformed_data_actors[actor]:
    #                 if movie in overallset_movies: #skip over if we've already seen the actor
    #                     continue
    #                 if actor in overallset_actors:
    #                     continue
    #                 if movie in overalldict.keys():
    #                     overalldict[movie].append(actor)
    #                 else:
    #                     overalldict[movie]=actor

    #                 if movie==film2: #return when we've found the actor
    #                     return overalldict[movie]
                    
    #                 if movie not in overallset_movies and actor not in overallset_actors: #only add them to the baconset if they haven't appearred before
    #                     print('new actors', transformed_data_movies[movie])
    #                     actor_set=transformed_data_movies[movie]
    #                     overallset_movies.add(movie)
    #                     overallset_actors.add(actor)
                   
    #         previous_actorset=actor_set #set the previous_baconset for later iterations to the baconset we just calculated
            
    #         if previous_actorset==set(): #checks if we have an empty set, in which case just return None
    #             return None
        
    # return None 
        


if __name__ == '__main__':
    with open('resources/small.pickle', 'rb') as f:
        smalldb = pickle.load(f)
    with open('resources/names.pickle', 'rb') as f:
        names = pickle.load(f)
    with open('resources/tiny.pickle', 'rb') as f:
        tinydb = pickle.load(f)
    with open('resources/large.pickle', 'rb') as f:
        largedb = pickle.load(f)
    with open('resources/movies.pickle', 'rb') as f:
        moviesdb = pickle.load(f)
    g=transform_movies(moviesdb)
    #print(names['Charles A. Tamburro']) #gives Charles's id number
    # print(acted_together(transform_data(smalldb), 4724, 2876))
    # print(names['Mark Fenton'])
    # print(names['Matt Dillon'])
    # print(names['Christian Campbell'])
    # print(names['Sten Hellstrom'])
    # print(names['Tim Emery'])
    # print(names['Linda Cardellini'])
    # print(names['Ronn Carroll'])
    # print(names['Iva Ilakovac'])
    # for i in names: #prints the person with the corresponding id
    #     if names[i]==78021:
    #         print(i) 
    # print(moviesdb)
    # x=transform_data(largedb)
    # print(movie_paths(g,x, 174248, 1345462))
    # print(actors_with_bacon_number(x,6))
    # a=[(2876, 4724, 617), (4724, 1532, 31932), (1532, 1532, 31932), (1532, 4724, 617), (1532, 2876, 31932), (2876, 1640, 617), (1640, 1640, 74881)]
    # a=transform_data(a)
    #print(largedb)
    print(actors_connecting_films(transform_data(largedb), 14830,3595))
    expected=[1640,2876]
    # print(bacon_path(a,1640))
    # answer=[4724, 2222, 3146, 13359, 139241, 1014296]
    # answer1=[1442724, 99003, 98999, 78021, 1817]
    # print(actor_to_actor_path(x, 1442724, 1817))
    # print(bacon_path(x,1014296))
    # m={1367972, 1338716, 1345461, 1345462}
    # print(acted_together(transform_data(smalldb), 4724, 2876))
    # print(acted_together(transform_data(smalldb), 19225, 572600))
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
