# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 20:55:16 2021

@author: joyse
"""

# def boolean_builtins(function, list1):
#     first_index=0
#     second_index=1
#     while second_index<len(list1):
#         if not function(list1[first_index],list1[second_index]):
#             return '#f'
#         first_index+=1
#         second_index+=1
#     return '#t' 
    
# def equal_operation(element1, element2):
#     if element1==element2:
#         return True

# def decreasing_operation(element1, element2):
#     if element1>element2:
#         return True
    
# def non_increasing(element1, element2):
#     if element1>=element2:
#         return True

# def increasing(element1, element2):
#     if element1<element2:
#         return True
    
# def non_decreasing(element1, element2):
#     if element1<=element2:
#         return True
    


# print(boolean_builtins(decreasing_operation, [3,3,3]))


def range(start, stop, step):
    if start>=stop:
        return []
    else:
        initial=[start]
        start=start+step
        return initial+range(start, stop, step)
    

def poly_val(coeffs, x):
    if len(coeffs)==1:
        return coeffs[0]
    else:
        return coeffs[0]+ (x * poly_val(coeffs[1:], x))
    
print(poly_val([-8, 7, 0, 4], 1))











