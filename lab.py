# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 14:59:38 2021

@author: joyse
"""

"""6.009 Lab 10: Snek Is You Video Game"""

import doctest

# NO ADDITIONAL IMPORTS!

# All words mentioned in lab. You can add words to these sets,
# but only these are guaranteed to have graphics.
NOUNS = {"SNEK", "FLAG", "ROCK", "WALL", "COMPUTER", "BUG"}
PROPERTIES = {"YOU", "WIN", "STOP", "PUSH", "DEFEAT", "PULL"}
WORDS = NOUNS | PROPERTIES | {"AND", "IS"}
Graphical_objects={'snek', 'flag', 'rock', 'wall', 'bug', 'computer'}


class Graph_Object():
    def __init__(self, name, prop, position):
        self.name=name
        self.prop=prop
        self.position=position
        
    def move(self, movement, coordinates, dimensions, board, info=None, seen=None):
        '''
        Moves an element from old coordinate to a new coordinate.
        Returns a tuple of (old coor, new coor) and updates an info list
        with this information
        '''

        if info==None:
            info=[]
        if seen==None:
            seen=set()
         
        #Set original coordinates
        x,y=direction_vector[movement]
        coor_x=coordinates[0]
        coor_y=coordinates[1]

        #Set new coordinates
        dim_x, dim_y=dimensions
        new_x=coor_x+x
        new_y=coor_y+y
        

        #If out of bounds, coors don't change
        if new_x<0 or new_x>dim_x-1 or new_y<0 or new_y>dim_y-1:
            answer=(self, (coor_x, coor_y), (coor_x, coor_y))
            info.append(answer)
            return (self.position, self.position)
        
        #Checking the elements in the same coordinate
        for element in board[coor_x][coor_y]:
            if 'STOP' in element.prop and 'PUSH' not in element.prop:
                if 'YOU' in self.prop:
                    answer=(self, (coor_x, coor_y), (new_x, new_y))
                    info.append(answer)
                    for element in board[new_x][new_y]:
                        element.move(movement, (new_x, new_y), dimensions, board, info, seen)
                elif 'PULL' in self.prop:
                    answer=(self, (coor_x, coor_y), (new_x, new_y))
                    info.append(answer)
                    return ((coor_x, coor_y), (new_x, new_y))
                else:
                    answer=(self, (coor_x, coor_y), (coor_x, coor_y))
                    info.append(answer)
                return (self.position, self.position)

        #Cheking the elements in the new coor
        for element in board[new_x][new_y]:
                if 'PUSH' in element.prop and element not in seen:
                    seen.add(element)
                    answer=element.move(movement, (new_x, new_y), dimensions, board, info, seen)
                    #Check if the final recursive call didn't move
                    if answer[0]==answer[1]:
                        answer=(self, (coor_x, coor_y), (coor_x, coor_y))
                        info.append(answer)
                        return (self.position, self.position)
                elif 'STOP' in element.prop and element not in seen:
                    seen.add(element)
                    answer=(self, (coor_x, coor_y), (coor_x, coor_y))
                    info.append(answer)
                    return (self.position, self.position)

     
        #If element reaches here, then it can move
        answer1=(self, (coor_x, coor_y), (new_x, new_y))
        #Append movement information into info list
        info.append(answer1)
        self.position=(new_x, new_y)
        
        #Check pulling at the end, only if we know original element can move
        if 0<=(coor_x-x)<=dim_x-1 and 0<=(coor_y-y)<=dim_y-1: 
           for element in board[coor_x-x][coor_y-y]:
               if 'PULL' in element.prop and element not in seen:
                   seen.add(element)
                   answer=element.move(movement, (coor_x-x, coor_y-y), dimensions, board, info, seen)
                   if answer[0]==answer[1]:
                       answer=(self, (coor_x, coor_y), (coor_x, coor_y))
                       info.append(answer)
                       return (self.position, self.position)
        
        
        return (self.position, (coor_x, coor_y))
       
            

direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

# def parse_helper(level_description, dim, col_index, row_index, col=True):
    
#     props=[]
#     count=0
#     #First check horizontal rules
#     if col:
#         index=col_index
#     else:
#         index=row_index

        
#     if index+1<dim:
#         if col:
#             cell=level_description[row_index][col_index+1]
#         else:
#             cell=level_description[row_index+1][col_index]
#         if cell!=[] and cell[0] in {'AND', 'IS'}:
#             for num in range(index+1, dim):
#                 if col:
#                     next_cell=level_description[row_index][num]
#                 else:
#                     next_cell=level_description[num][row_index]
                
                
#                 if next_cell==[]:
#                     break
#                 #Find the word at the given index
#                 item1=next_cell[0]
#                 #Don't add 'AND' to rules
#                 if item1=='AND':
#                     continue
#                 #'IS' implies we've found a rule
#                 elif item1=='IS':
#                     #Iterate over everything after the IS
#                     for new_num in range(num, dim):
#                         if col:
#                             cell_after_is=level_description[row_index][new_num]
#                         else:
#                             cell_after_is=level_description[new_num][col_index]
#                         if cell_after_is==[]:
#                             break
#                         item2=cell_after_is[0]
#                         if item2 in WORDS and item2 not in {'AND', 'IS'}:
#                             #If we've found a word, the previous word has to be 'IS'
#                             if col:
#                                 prev_cell=level_description[row_index][new_num-1]
#                                 next_next_cell=level_description[row_index][new_num+1]
#                             else:
#                                 prev_cell=level_description[new_num-1][col_index]
#                                 next_next_cell=level_description[new_num+1][col_index]
                            
#                             if prev_cell[0]=='IS' and count>0:
#                                 break
#                             props.append(item2)
#                             count+=1
#                             #In order to keep going, the next word must be 'AND'
#                             if new_num+1<dim and next_next_cell!=[] and next_next_cell[0]!='AND':
#                                 break
#     return props

def parse_rules(level_description, dimensions):
    '''
    Parses the rules of a given game. Returns a dictionary in the form 
    of {Text object: property assigned to it by rules...}
    '''
    Rules={}
    dim_x, dim_y=dimensions

    for row_index, row in enumerate(level_description):
        for col_index, col in enumerate(row):
            if col!=[]:
                item=col[0]
                if item in NOUNS:
                    props=[]
                    count=0
                    #First check horizontal rules
                    if col_index+1<dim_y and level_description[row_index][col_index+1]!=[] and level_description[row_index][col_index+1][0] in {'AND', 'IS'}:
                        for num in range(col_index+1, dim_y):
                            if level_description[row_index][num]==[]:
                                break
                            #Find the word at the given index
                            item1=level_description[row_index][num][0]
                            #Don't add 'AND' to rules
                            if item1=='AND':
                                continue
                            #'IS' implies we've found a rule
                            elif item1=='IS':
                                #Iterate over everything after the IS
                                for new_num in range(num, dim_y):
                                    if level_description[row_index][new_num]==[]:
                                        break
                                    item2=level_description[row_index][new_num][0]
                                    if item2 in WORDS and item2 not in {'AND', 'IS'}:
                                        #If we've found a word, the previous word has to be 'IS'
                                        if level_description[row_index][new_num-1][0]=='IS' and count>0:
                                            break
                                        props.append(item2)
                                        count+=1
                                        #In order to keep going, the next word must be 'AND'
                                        if new_num+1<dim_y and level_description[row_index][new_num+1]!=[] and level_description[row_index][new_num+1][0]!='AND':
                                            break
                    
                    count=0
                    #Check vertical rules
                    if row_index+1<dim_x and level_description[row_index+1][col_index]!=[] and level_description[row_index+1][col_index][0] in {'AND', 'IS'}:
                        for num in range(row_index+1, dim_x):
                            if level_description[num][col_index]==[]:
                                break
                            for item1 in level_description[num][col_index]:
                                if item1=='AND':
                                    continue
                                elif item1=='IS':
                                    for new_num in range(num, dim_x):
                                        if level_description[new_num][col_index]==[]:
                                            break
                                        item2=level_description[new_num][col_index][0]
                                        if item2 not in {'AND', 'IS'} and item2 in WORDS:
                                            if new_num-1<dim_x and level_description[new_num-1][col_index][0]=='IS' and count>0:
                                                break
                                            props.append(item2)
                                            count+=1
                                            if new_num+1<dim_x and level_description[new_num+1][col_index]!=[] and level_description[new_num+1][col_index][0]!='AND':
                                                break

                    if item in Rules:
                        Rules[item]=Rules[item]+props
                    else:
                        if props!=[]:
                            Rules[item]=props
                    
    return Rules
                                    
   

def get_dimensions(level_description):
    '''
    Finds the dimensions of a given game
    '''
    num_rows=0
    for row_index, row in enumerate(level_description):
        num_rows+=1
        num_columns=0
        for column_index, space in enumerate(row):
            num_columns+=1

    return (num_rows, num_columns)


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, where UPPERCASE
    strings represent word objects and lowercase strings represent regular
    objects (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['snek'], []],
        [['SNEK'], ['IS'], ['YOU']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.


    Returns a board with instances of graphical objects,
    dimensions of the board, a location dict mapping elements to 
    a list of tuples with their coordinates, and a dictionary of Rules
    """

    location_dict={}
    new_board=[]
    dim=get_dimensions(level_description)
    Rules=parse_rules(level_description, dim)
    
    for row_index, row in enumerate(level_description):
        row_list=[]
        for column_index, space in enumerate(row):
            if space==[]:
                row_list.append(space)
                continue
            items_list=[]
            for space_index, item in enumerate(space):
                #Create a location dict
                if item not in location_dict:
                    location_dict[item]=[(row_index, column_index)]
                else:
                    location_dict[item].append((row_index, column_index))
                #Create class instance with associated properties
                if item in Graphical_objects:
                    if item.upper() in Rules:
                        items_list.append(Graph_Object(item, Rules[item.upper()], (row_index, column_index)))
                    else:
                        items_list.append(Graph_Object(item, [None], (row_index, column_index)))
                elif item in WORDS:
                    items_list.append(Graph_Object(item, ['PUSH'], (row_index, column_index)))

            row_list.append(items_list)
        new_board.append(row_list)

    return [new_board, location_dict, dim, Rules]



def move_value(game, coordinates, value, remove=False):
    '''
    Given an array and a coordinate, change the value at the coordinate to the given value
    and return the new array
    '''

    x=game[coordinates[0]]
    coordinate=coordinates[1]

    if remove:

        x[coordinate].remove(value)
    else:

        x[coordinate].append(value)

    return game


def determine_win(game, you, win):
    '''
    Given a game and a set of you states and a set of win states,
    returns True if the game is won, False if otherwise
    '''

    for row_index, row in enumerate(game):
        for col_index, column in enumerate(row):
            victory=0
            char=0
            for item in column:
                if isinstance(item, Graph_Object):
                    if item.name in win and item.name in you:
                        return True
                    elif item.name in win:
                        victory+=1
                    elif item.name in you:
                        char+=1
            #Return True if you've found a victory
            if victory>0 and char>0:
                return True

    return False


def determine_defeat(game, you, defeat):
    '''
    Given a game and a set of you states and a set of defeat states,
    returns (True, list of coords to remove from the board) or (False, []) if
    there is no defeat
    '''
    
    info=[]

    for row_index, row in enumerate(game):
        for col_index, column in enumerate(row):
            lose_score=0
            you_score=0
            for item in game[row_index][col_index]:
                if isinstance(item, Graph_Object):
                    for losing_char in defeat:
                        if losing_char==item.name:
                            lose_score+=1
                    for you_char in you:
                        if you_char==item.name:
                            you_score+=1
                    if lose_score>0 and you_score>0:
                        answer=(item, (row_index, col_index))
                        info.append(answer)
    #Return false is no defeat
    if info==[]:
        return (False, info)
    
    #Return True and info if defeat
    return (True, info)
                        
            

def find_characters(Rules):
    '''
    Given the rules, finds the objects corresponding to 'you' states, to 'win'
    states and to 'defeat' states
    '''
    you=[]
    lost=[]
    win=[]
    for item in Rules.keys():
        if 'YOU' in Rules[item]:
            you.append(item.lower())
        if 'DEFEAT' in Rules[item]:
            lost.append(item.lower())
        if 'WIN' in Rules[item]:
            win.append(item.lower())
    return (you, lost, win)
            



def convert_to_set(character):
    '''
    Helper that returns an input into a set
    '''
    if type(character)==str:
        return {character}
    if type(character)==list:
        return set(character)





def step_game(game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """

    board=game[0]
    location_dict=game[1]
    dimensions=game[2]
    Rules=game[3]
    you=find_characters(Rules)[0]
    
    #If there is no you state on the board
    if you==[]:
        return False
    
    seen=set()
    info=[]
    
    ###FINDING AND MOVING THE YOU ITEMS
    
    #Iterate through the board, reset the properties of the elements
    for row in board:
        for column in row:
            for item in column:
                if isinstance(item, Graph_Object):
                    if item.name in Graphical_objects:
                        if item.name.upper() in game[3]:
                            item.prop=game[3][item.name.upper()]
                        else:
                            item.prop=[None]
                            
    #Find all the coords in the board corresponding to 'you' objects
    you_coords=[]
    for key in location_dict.keys():
        if key in Graphical_objects and key.upper() in Rules and 'YOU' in Rules[key.upper()]:
            you_coords=you_coords+location_dict[key]

    #Find all the movements of the you items
    for coor in you_coords:
        coor1, coor2=coor
        for item in board[coor1][coor2]:
            if item.name in you:
                if item not in seen:
                    #Keeps track of info giving item, old coor, new coor
                    answer=item.move(direction, coor, dimensions, board, info)
                    info=info
    

    #Iterate through all the items to be moved, and move them
    for item in info:
        value, old_coor, new_coor=item
        if value not in seen:
            seen.add(value)
            board=move_value(board, old_coor, value, True)
            board=move_value(board, new_coor, value)
            location_dict[value.name].append(new_coor)
            location_dict[value.name].remove(old_coor)



    #Update the rules
    game[3]=parse_rules(convert_board(board), dimensions)
    values_to_change=[]
    new_values=[]

    Rules=game[3]

    ###SECTION FOR DEALING WITH ITEMS THAT HAVE NOUN PROPERTIES
    #Find all items with noun properties
    for value in Rules.keys():
        if value.lower() in location_dict:
            for prop in Rules[value]:
                if prop in NOUNS:
                    values_to_change.append(value.lower())
                    new_values.append(prop.lower())
                    
    #Make a copy of the location dict
    new_location_dict={}
    for key in location_dict.keys():
        new_location_dict[key]=location_dict[key].copy()
        
    updated_location_dict={}
    
    #For items with noun props, change the item name and update their coors in the updated dict
    for new_value,value in zip(new_values,values_to_change):
        for coor in new_location_dict[value]:
            coor1, coor2=coor
            for item in board[coor1][coor2]:
                if item.name==value:
                    if new_value not in updated_location_dict:
                        updated_location_dict[new_value]=[coor]
                    else:
                        updated_location_dict[new_value].append(coor)
                    if coor not in seen:    
                        item.name=new_value
                        seen.add(coor)

                        
    
    #Set location dict to updated dict
    if updated_location_dict!={}:

        for key in location_dict:
            if key not in updated_location_dict:
                updated_location_dict[key]=location_dict[key].copy()
    
                
        game[1]=updated_location_dict
        location_dict=game[1]
    
    
    ###SECTION FOR DETERMINING WIN OR DEFEAT
    you, lose, win=find_characters(Rules)
    you_set=convert_to_set(you)
    lose_set=convert_to_set(lose)
    win_set=convert_to_set(win)


    answer=determine_defeat(board, you_set, lose_set)
    
    #If there is a defeat, remove that element
    if answer[0]:
        del_info=answer[1]
        for item in del_info:
            element, old_coor=item
            board=move_value(board, old_coor, element, True)
            location_dict[element.name].remove(old_coor)
        return False
    
    #Check if there is a win
    else:
        answer=determine_win(board, you_set, win_set)
        return answer

           

def convert_board(board):
    '''
    Helper function to convert my implementation of the board back into
    the canonical version
    '''
    new_board=[]
    for row in board:
        row_list=[]
        for space in row:
            if space==[]:
                row_list.append(space)
                continue
            items_list=[]
            for item in space:
                if isinstance(item, Graph_Object):
                    items_list.append(item.name)
                else:
                    items_list.append(item)
            row_list.append(items_list)
        new_board.append(row_list)
    return new_board


def dump_game(game):
    """
    Given a game representation (as returned from new_game), convert it back
    into a level description that would be a suitable input to new_game.

    This function is used by the GUI and tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """

    board=game[0]  
    answer=convert_board(board)
    return answer
 

