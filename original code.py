# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:15:34 2021

@author: joyse
"""

#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION

def create_list(num_rows, num_cols, bombs, masks=False):
    '''
    Helper function to create the board or mask list
    '''
    new_list=[]
    
    if masks: #if masks is true, proceed with the masks code
        for r in range(num_rows):
            row = []
            for c in range(num_cols):
                row.append(False)
            new_list.append(row)
        return new_list
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            if [r, c] in bombs or (r, c) in bombs:
                row.append('.')
            else:
                row.append(0)
        new_list.append(row)
    return new_list

def find_neighbors(r,c, num_rows, num_cols):
    '''

    Parameters
    ----------
    r : the given row
    c : the given column
    num_rows : total number of rows
    num_cols : total number of columns 

    Returns
    -------
    neighbor_list : a list of tuples of neighbors to the given r,c

    '''
    
    neighbor_list=[]
    max_row=num_rows-1
    max_col=num_cols-1
    
    r_list=[(r-1),(r),(r+1)]
    c_list=[(c-1),(c),(c+1)]
    
    #Finds all the possible rows and columns to visit
    if r==max_row:
        del(r_list[2])
    elif r==0:
        del(r_list[0])
    if c==max_col:
        del(c_list[2])
    if c==0:
        del(c_list[0])
        
    #Finds all possible combinations of possible rows and columns, adds to neighbors
    for row in r_list:
        for col in c_list:
            neighbor_list.append((row,col))
    return neighbor_list
    
    
def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    
    board=create_list(num_rows, num_cols, bombs)
    mask=create_list(num_rows, num_cols, bombs, True)
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0
                neighbors=find_neighbors(r, c, num_rows, num_cols) #find the neighbors
                for neighbor in neighbors:
                    if board[neighbor[0]][neighbor[1]]== '.':
                        neighbor_bombs+=1
                board[r][c] = neighbor_bombs
    return {
        'dimensions': (num_rows, num_cols),
        'board': board,
        'mask': mask,
        'state': 'ongoing'}


def update_state(game):
    '''

    Parameters
    ----------
    game : the game state
    Returns
    -------
    list
        list of the updated number of bombs and covered squares.

    '''
    bombs = 0  # set number of bombs to 0
    covered_squares = 0
    for r in range(game['dimensions'][0]):
        # for each r,
        for c in range(game['dimensions'][1]):
            # for each c,
            if game['board'][r][c] == '.':
                if game['mask'][r][c] == True:
                    # if the game mask is True, and the board is '.', add 1 to
                    # bombs
                    bombs += 1
            elif game['mask'][r][c] == False:
                covered_squares += 1
    return [bombs, covered_squares]


def update_state_nd(all_coordinates, game):
    '''

    Parameters
    ----------
    game : the game state
    Returns
    -------
    list
        list of the updated number of bombs and covered squares.

    '''
    
    bombs=0
    covered_squares=0
    # all_coordinates=get_possible_coordinates(game['dimensions'])
    
    for coor in all_coordinates:
        if get_coordinates(game['board'], coor)=='.':
            if get_coordinates(game['mask'], coor):
                bombs+=1
        elif not get_coordinates(game['mask'], coor):
            covered_squares+=1
    return [bombs, covered_squares]
            


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    if game['state'] == 'defeat' or game['state'] == 'victory':
        game['state'] = game['state']  # keep the state the same
        return 0

    if game['board'][row][col] == '.':
        game['mask'][row][col] = True
        game['state'] = 'defeat'
        return 1

    bombs, covered_squares=update_state(game)
    if bombs != 0:
        # if bombs is not equal to zero, set the game state to defeat and
        # return 0
        game['state'] = 'defeat'
        return 0
    
    if covered_squares == 0:
        game['state'] = 'victory'
        return 0

    if game['mask'][row][col] != True:
        game['mask'][row][col] = True
        revealed = 1
    else:
        return 0

    if game['board'][row][col] == 0:
        num_rows, num_cols = game['dimensions']
        neighbors=find_neighbors(row, col, num_rows, num_cols)
        for neighbor in neighbors:
            if game['board'][neighbor[0]][neighbor[1]] != '.':
                if game['mask'][neighbor[0]][neighbor[1]] == False:
                    revealed += dig_2d(game, neighbor[0], neighbor[1])

    bombs, covered_squares=update_state(game)          
    bad_squares = bombs + covered_squares
    if bad_squares > 0:
        game['state'] = 'ongoing'
        return revealed
    else:
        game['state'] = 'victory'
        return revealed



def board_to_string(game):
    '''
    Parameters
    ----------
    game : Game state

    Returns
    -------
    board_copy : returns copy of the game state board where all values are turned into strings and 0's become ' ''

    '''
    final_board=[]
    board_copy=game['board'].copy()
    
    ##iterate through each value and change to corresponding string
    for index1,row in enumerate(board_copy):
        row_copy=row.copy()
        for index2,value in enumerate(row_copy):
            if value==0:
                row_copy[index2]=' '
            else:
                row_copy[index2]=str(value)
        final_board.append(row_copy)
    return final_board

def board_to_string_nd(array, dimensions):
    '''
    Parameters
    ----------
    game : Game state

    Returns
    -------
    board_copy : returns copy of the game state board where all values are turned into strings and 0's become ' ''

    '''
    
    all_coordinates=get_possible_coordinates(dimensions)
    for coor in all_coordinates:
        if get_coordinates(array, coor)==0:
            array=replace_value(array, coor, ' ')
        else:
            value=get_coordinates(array,coor)
            array=replace_value(array, coor, str(value))
    return array

def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['mask'] indicates which squares should be visible.  If xray
    is True (the default is False), game['mask'] is ignored and all cells are
    shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    board_copy=board_to_string(game).copy() 
    if xray: 
        return board_copy
    
    #Make values invisible if game[mask] is false
    for index1, row in enumerate(game['mask']): 
        for index2, tuple_val in enumerate(row):
            if not tuple_val: 
                board_copy[index1][index2]='_'
                
    return board_copy


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'mask':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    board_string=''
    new_board=render_2d_locations(game, xray)
    number_of_squares=len(new_board[0])
    number_of_rows=len(new_board)
    
    #Creates a string of the board
    for index1, row in enumerate(new_board):
        count=0
        for index2, value in enumerate(row):
            board_string=board_string+new_board[index1][index2]
            count+=1
            #Adds \n if the end of a row
            if count==number_of_squares and index1!=number_of_rows-1:
                board_string=board_string+'\n'
            
            
    return board_string

# N-D IMPLEMENTATION

#HELPER FUNCTIONS


# A function that, given a game, returns the state of that game ('ongoing', 'defeat', or 'victory').


def get_coordinates(array, coordinates):
    '''
    Given an array and a coordinate, returns the specific value at that coordinate
    >>> get_coordinates([[0,1],[2,3],[4,5]], (2,0))
    4
    '''

    value=array.copy()
    for coordinate in coordinates:
        value=value[coordinate]
    return value 

def replace_value(array, coordinates, value):
    '''
    Given an array and a coordinate, change the value at the coordinate to the given value and return the new array
    '''
    
    x=array[coordinates[0]]
    count=0
    for coordinate in coordinates[1:]:
        count+=1
        if count==len(coordinates)-1:
            x[coordinate]=value
        else:
            x=x[coordinate]
    return array

def create_array(dimensions, value):
    '''
    Given dimensions and a value, creates an array of those dimensions with each value in the array 
    '''
    
    if len(dimensions)==1:
        return [value] * dimensions[0]
    
    else:
        answer=[create_array(dimensions[1:], value) for i in range(dimensions[0])]
        return answer


def convert_tuples(tup):
    '''
    Given a nested tuple, returns a single tuple of all the values
    for instance, ((1,2),3) ==> (1,2,3)
    
    '''
    new_list=[]
    for index,i in enumerate(tup):
        if type(i)==tuple:
            for j in i:
                new_list.append(j)
        else:
            new_list.append(i)

    return tuple(new_list)


def get_nd_neighbors(coordinates, dimensions):
    '''
    Given coordinates and dimensions, finds all the neighbors to the given 
    coordinate (including the coordinate itself)

    '''
    
    neighbor_dict={}
    
    #initialize the dictionary with the possible neighbors to each coordinate
    for index,i in enumerate(coordinates):
        if i==0 and i==(dimensions[index]-1):
            neighbor_dict[i]={(i,)}
        elif i==0:
            neighbor_dict[i]={(i,),(i+1,)}
        elif i==(dimensions[index]-1):
            neighbor_dict[i]={(i-1,), (i,)}
        else:
            neighbor_dict[i]={(i-1,), (i,), (i+1,)}
    
    count=0
    #finds neighbors of pairs of coordinates
    while count<len(dimensions)-1:
        count+=1
        for neighbor1 in neighbor_dict[coordinates[0]]:
            for neighbor2 in neighbor_dict[coordinates[1]]:
                
                neighbor=(neighbor1, neighbor2)
                neighbor=convert_tuples(neighbor)
                original_point= (coordinates[0], coordinates[1])
                original_point=convert_tuples(original_point)
                
                #Add the point and all the neighbors of that point to the dictionary
                if original_point not in neighbor_dict.keys():
                    neighbor_dict[original_point]={neighbor}
                else:
                    neighbor_dict[original_point].add(neighbor)

        #Set the new coordinates as the original point: every other coordinate
        coordinates=(original_point, *coordinates[2:])

        
    return list(neighbor_dict[coordinates[0]])


def get_possible_coordinates(dimensions):
    '''
    Given dimensions (tuple) returns a list of all possible coordinate in a game board
    
    '''
    dimension_copy=list(dimensions).copy()
    coordinates_dict={}
    
    #initialize the dictionary with the possible coordinate values in each dimension
    for i in dimensions:
        coordinates_dict[i]=set()
        for j in range(i):
            coordinates_dict[i].add((j,))
          
    count=0
    
    #finds possible coordinates given all dimensions
    while count<len(dimension_copy)-1:
        count+=1
        for coor1 in coordinates_dict[dimensions[0]]:
            for coor2 in coordinates_dict[dimensions[1]]:
                
                coor3=(coor1, coor2)
                coor3=convert_tuples(coor3)
                original_point= (dimensions[0], dimensions[1])
                original_point=convert_tuples(original_point)
                
                #Add the point and all the possible coordinates from that point to the dictionary
                if original_point not in coordinates_dict.keys():
                    coordinates_dict[original_point]={coor3}
                else:
                    coordinates_dict[original_point].add(coor3)

        #Set the new dimensions as the original point: every other point remaining
        dimensions=(original_point, *dimensions[2:])
        
    return list(coordinates_dict[dimensions[0]])


###THE MEAT AND POTATOES
def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    #Create initial variables
    mask=create_array(dimensions, False)
    new_board=create_array(dimensions, 0)
    bombs_set=set(bombs)
    all_coordinates=get_possible_coordinates(dimensions)
    
    #iterate through all coordinates to find their value, append value to board
    for coor in all_coordinates:
        adjacent_bombs=0
        if coor in bombs_set:
            adjacent_bombs='.'
            replace_value(new_board, coor, adjacent_bombs)
        else:
            neighbors=get_nd_neighbors(coor, dimensions)
            for neighbor in neighbors:
                if neighbor in bombs_set:
                    adjacent_bombs+=1
            replace_value(new_board, coor, adjacent_bombs)
    
    game={
    'dimensions': dimensions,
    'board': new_board,
    'mask':mask,
    'state': 'ongoing',
    }
    
    return game


# def find_covered_squares(game):
#     all_coordinates=get_possible_coordinates(game['dimensions'])
#     covered_squares=0
#     for coor in all_coordinates:
#         if get_coordinates(game['board'], coor)!='.':
#             covered_squares+=1
#     return covered_squares


def check_game_state(game):
    '''
    
    returns the state of the game 

    '''
    all_coordinates=get_possible_coordinates(game['dimensions'])
    for coor in all_coordinates:
        if get_coordinates(game['board'], coor)=='.' and get_coordinates(game['mask'], coor):
            return 'defeat'
        if get_coordinates(game['board'], coor)!='.' and not get_coordinates(game['mask'], coor):
            return 'ongoing'
    return 'victory'

def dig_nd(game, coordinates, counter=0):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    
    # bombs, covered_squares=update_state_nd(game)
    # def function(covered_squares, game, coordinates):
    #     covered_squares-=1
    #     if game['state'] == 'defeat' or game['state'] == 'victory':
    #         game['state'] = game['state']  # keep the state the same
    #         return 0
        
    #     game['mask']=replace_value(game['mask'], coordinates, True)
    #     revealed=1
        
    #     if get_coordinates(game['board'], coordinates)=='.':
    #         game['mask']=replace_value(game['mask'], coordinates, True)
    #         game['state']='defeat'
    #         return 1
        
    
    
    #     if get_coordinates(game['board'], coordinates) == 0:
    #         neighbors=get_nd_neighbors(coordinates, game['dimensions'])
    #         for neighbor in neighbors:
    #             if get_coordinates(game['board'], neighbor) != '.':
    #                 if not get_coordinates(game['mask'], neighbor):
    #                     revealed += function(covered_squares, game, neighbor)
    #     bad_squares = bombs + covered_squares   
    #     if bad_squares>0:
    #         game['state']='ongoing'
    #         return revealed
    #     else:
    #         game['state']='victory'
    #         return revealed
    # return function(covered_squares)
        # if counter==0:                
        #     game['state']=check_game_state(game)
        # return revealed
    
    # # if first_call:
    # #     all_coordinates=get_possible_coordinates(game['dimensions'])
    ###WORKING CODE
    if game['state'] == 'defeat' or game['state'] == 'victory':
        game['state'] = game['state']  # keep the state the same
        return 0
    if not get_coordinates(game['mask'], coordinates):
        replace_value(game['mask'], coordinates, True)
        revealed=1
        if get_coordinates(game['board'], coordinates)=='.':
            game['state']='defeat'
            return revealed

    else:
        return 0
    
    # if get_coordinates(game['board'], coordinates)=='.':
    #     game['mask']=replace_value(game['mask'], coordinates, True)
    #     game['state']='defeat'
    #     return 1
    

    if get_coordinates(game['board'], coordinates) == 0:
        neighbors=get_nd_neighbors(coordinates, game['dimensions'])
        for neighbor in neighbors:
            # if get_coordinates(game['board'], neighbor) != '.':
                # if not get_coordinates(game['mask'], neighbor):
                    revealed += dig_nd(game, neighbor, counter+1)
    if counter==0:                
        game['state']=check_game_state(game)
    return revealed
    
    ###OLD SOLUTION

    # bombs, covered_squares=update_state_nd(all_coordinates, game)          
    # bad_squares = bombs + covered_squares
    # if bad_squares > 0:
    #     game['state'] = 'ongoing'
    #     return revealed
    # else:
    #     game['state'] = 'victory'
    #     return revealed
    
    
    # # if first_call:
    # #     game['state']=check_game_state(game)
    # #     #add parameter to check if status is won
    # #     # bombs, covered_squares=update_state_nd(game) 
    # #     #covered_squares=find_covered_squares(game)
    # #     #find_covered_squares(game)
            
    
    # if game['state'] == 'defeat' or game['state'] == 'victory':
    #     game['state'] = game['state']  # keep the state the same
    #     return 0
    # #if mask is true, return 0
    
    # game['mask']=replace_value(game['mask'], coordinates, True)
    # revealed=1

    
    # if get_coordinates(game['board'], coordinates)=='.':
    #     game['state']='defeat'
    #     return 1
    
    # #covered_squares=covered_squares-1

    # # bombs, covered_squares=update_state_nd(game)
    # # if bombs != 0:
    # #     # if bombs is not equal to zero, set the game state to defeat and
    # #     # return 0
    # #     game['state'] = 'defeat'
    # #     return 0
    
    # # if covered_squares == 0:
    # #     game['state'] = 'victory'
    # #     return 0
    
    # if get_coordinates(game['board'], coordinates)==0:
    #     neighbors=get_nd_neighbors(coordinates, game['dimensions'])
    #     for neighbor in neighbors:
    #         if get_coordinates(game['board'], neighbor)!='.':
    #             if not get_coordinates(game['mask'], neighbor):
    #                 game['mask']=replace_value(game['mask'], coordinates, False)
    #                 #print('recursive call', dig_nd(game,neighbor))
    #                 revealed += dig_nd(game, neighbor)
            
    # bombs, covered_squares=update_state_nd(game)    
    # #print('covered_squares', covered_squares)
    # # if covered_squares<revealed:
    # #     game['state']='ongoing'
    # #     return revealed
    # # else:
    # #     game['state']='victory'
    # #     return revealed
    # # return revealed
    # bad_squares = bombs + covered_squares   
    # if bad_squares>0:
    #     game['state']='ongoing'
    #     return revealed
    # else:
    #     game['state']='victory'
    #     return revealed
            




def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    

    new_board=create_array(game['dimensions'], '0')
    all_coordinates=get_possible_coordinates(game['dimensions'])
    
    if xray: 
        return board_to_string_nd(game['board'], game['dimensions'])
    
    for coor in all_coordinates:
        value=get_coordinates(game['board'], coor)
        new_board=replace_value(new_board, coor, value)
        if not get_coordinates(game['mask'], coor):
            new_board=replace_value(new_board, coor, '_')
    
    new_board=board_to_string_nd(new_board, game['dimensions'])      
    return new_board


if __name__ == "__main__":
    #Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags, verbose=True)  # runs ALL doctests
    
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    
     # dump(g)
     
        # g = {'dimensions': (2, 4, 2),
        #      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        #                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        #     'mask': [[[False, False], [False, True], [False, False],
        #                [False, False]],
        #               [[False, False], [False, False], [False, False],
        #               [False, False]]],
        #     'state': 'ongoing'}
        # print(dig_nd(g, (0, 3, 0)))
        
        
#     game={
#        'dimensions': (5,),
#        'board': [1, '.', 1, 0, 0],
#        'mask': [False, False, False, False, False],
#        'state':'ongoing',
#        }
    
#     # result1=lab.dig_nd(game, (0,))
#     expected1=1
#     #result2=lab.dig_nd(game, (4,))
#     expected2=3
#     game= {
    
#     'dimensions': (6, 6),
    
#     'board':
#     [[0, 0, 1, 1, 2, '.'],
#     [0, 0, 2, '.', 3, 1],
#     [1, 1, 2, '.', 2, 0],
#     ['.', 1, 1, 1, 1, 0],
#     [1, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0]],

#     'mask':
#     [[False, False, False, False, False, False],
#     [False, False, False, False, False, False],
#     [False, False, False, False, False, False],
#     [False, False, False, False, False, False],
#     [False, False, False, False, False, False],
#     [False, False, False, False, False, False]],
    
#     'state': 'ongoing',
# }
        
#     # result1=lab.dig_nd(game, (1, 0))
#     expected1=9
#     # result2=lab.dig_nd(game, (5,4))
#     expected2=21
#     # assert result1==expected1
#     # assert result2==expected2
#     #print(dig_nd(game, (0,)))
#     print(dig_nd(game, (5,4)))
    
    #DOCTEST FAILING WEIRDLY, TIMING OUT OF THE TEST CASES, WRITE DOCSTRINGS AND SIMPLIFY