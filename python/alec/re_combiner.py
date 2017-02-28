# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:22:24 2017

For generating regex strings from lists

@author: David
"""

def combine_or(items):
    #Combines a list of items into an or regex expression
    re = '('
    for item in items[:-1]:
        re = re + item + '|'
    re = re + items[-1] + ')'
    return re
