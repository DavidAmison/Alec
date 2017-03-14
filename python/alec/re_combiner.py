"""
Created on Wed Feb 22 15:22:24 2017

For generating regex strings from lists

@author: David
"""

from pathlib import Path


def combine_or(items):
    #Combines a list of items into an or regex expression
    re = '('
    for item in items[:-1]:
        re = re + item + '|'
    re = re + items[-1] + ')'
    return re

def combine_or_file(path):
    #Combines a list of space seperaed words in a file (one row) e.g (abc|def)
    f = open(str(path),'r')
    re = '('
    words = f.readline().split()
    for w in words[:-1]:
        re = re + w + '|'
    re = re + words[-1] + ')'
    return re

    
