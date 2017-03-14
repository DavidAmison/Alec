"""
Created on Fri Mar  3 15:02:52 2017

Subclass of Alec used to teach him new things

@author: David
"""
import os
from pathlib import Path

import re

from . import alec

class AL_teach():  
    
    def __init__(self, alec_i):
        self.language = Path(os.path.dirname(__file__)) / 'Language'
        #General directories of various stuff alec can learn
        self._learning_dict = {1:'Greetings'}
        self._learningfiles = {1:self.language/'greetings.txt'}
        self._learning_max = 2
        self.AL = alec_i
        
    async def init_teaching(self,msg='',args=[]):
        #initiate teaching of alec
        print('entering teaching mode')
        self.AL.next_task = [self.AL.learn.learn_what]
        return '''What do you want to teach me?
                    1) Greetings
                    2) Nothing'''
    
    async def learn_what(self,msg='',args=[]):
        print('extracting what I need to learn')
        #Extract the number from the message.
        try:
            value = int(re.match(r'\d+',msg).group())
            #Add to the arguments for the next instruction
            self.AL.next_args.clear()
            self.AL.next_args['value'] = value
        except Exception as e:
            print(e)
            return 'Sorry, please enter a valid number'
        self.AL.next_task = [self.AL.learn.learn]
        return 'Okay, what phrase do you want me to learn?'
        
    async def learn(self,msg='',args=[]):
        print('learning')
        #Open the required file in append mode and add the new phrase
        p = self._learningfiles[args['value']]
        f = open(str(p),'a')
        f.write(' '+msg)
        f.close()
        self.AL.next_task = []
        return 'Thankyou for teaching me that!'
        
        
        
        
        
        
        
        
    