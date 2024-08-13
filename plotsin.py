# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:19:05 2024

@author: bangk
"""

import math

step = 0.25
x = 0.0

while True:
    y= math.sin(x)
    n_spaces = math.floor((y+1)*50)
    
    print(''*n_spaces + 'x')
    x+= step