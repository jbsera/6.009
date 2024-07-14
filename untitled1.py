# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 23:43:24 2021

@author: joyse
"""

[[("Bob_kitchen", False), ("Bob_basement", False)], [("Bob_kitchen", False), ("Bob_penthouse", False)], [("Bob_penthouse", False), ("Bob_basement", False)], [("Dana_kitchen", False), ("Dana_basement", False)], [("Dana_kitchen", False), ("Dana_penthouse", False)], [("Dana_penthouse", False), ("Dana_basement", False)], [("Alice_kitchen", False), ("Alice_basement", False)], [("Alice_kitchen", False), ("Alice_penthouse", False)], [("Alice_penthouse", False), ("Alice_basement", False)], [("Charles_kitchen", False), ("Charles_basement", False)], [("Charles_kitchen", False), ("Charles_penthouse", False)], [("Charles_penthouse", False), ("Charles_basement", False)]]


[("Dana_kitchen", False), ("Dana_basement", False)], [("Dana_kitchen", False), ("Dana_penthouse", False)], [("Dana_penthouse", False), ("Dana_basement", False)]

[("Alice_kitchen", False), ("Alice_basement", False)], [("Alice_kitchen", False), ("Alice_penthouse", False)], [("Alice_penthouse", False), ("Alice_basement", False)]

[("Charles_kitchen", False), ("Charles_basement", False)], [("Charles_kitchen", False), ("Charles_penthouse", False)], [("Charles_penthouse", False), ("Charles_basement", False)]



[[("Bob_kitchen", False), ("Dana_kitchen", False), ("Charles_kitchen", False)], [("Bob_kitchen", False), ("Dana_kitchen", False), ("Alice_kitchen", False)], [("Alice_kitchen", False), ("Dana_kitchen", False), ("Charles_kitchen", False)], [("Bob_kitchen", False), ("Alice_kitchen", False), ("Charles_kitchen", False)], [("Bob_basement", False), ("Dana_basement", False)], [("Bob_basement", False), ("Charles_basement", False)], [("Bob_basement", False), ("Alice_basement", False)], [("Alice_basement", False), ("Charles_basement", False)], [("Alice_basement", False), ("Dana_basement", False)], [("Charles_basement", False), ("Dana_basement", False)]]



Kitchen
Bob, Dana, Charles
Bob, Dana, Alice
Dana, Alice, Charles
Charles, Alice, Bob

[("Bob_basement", False), ("Dana_basement", False)], [("Bob_basement", False), ("Charles_basement", False)], [("Bob_basement", False), ("Alice_basement", False)], [("Alice_basement", False), ("Charles_basement", False)], [("Alice_basement", False), ("Dana_basement", False)], [("Charles_basement", False), ("Dana_basement", False)]
Basement
Bob, Dana
Bob, Charles
Bob, Alice
Alice, Charles
Alice, Dana
Charles, Dana