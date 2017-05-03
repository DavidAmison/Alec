# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:48:57 2017

Takes messages in the following format:
    {'chat_id':'...','user_id':'...','msg':'...','user_name':'...'}

@author: David
"""

from textblob import TextBlob
from textblob import Word
import random
import re

from natural_time import natural_time
from .reminderfinder import classifier

    
import os
from pathlib import Path
from . import re_combiner
from .teach_alec import AL_teach
from .alec_organiser import AL_organise

class Alec():
    
    def __init__(self, ch):
        self.chat_handler = ch
        #TODO This is a string telling Alec what to do with the next input he recieves
        self.next_task = []
        self.next_args = {}
        self.wait_for_reply = False
        
        #Important regex strings
        self.said_my_name = re.compile(r'\b(Alec|alec|al|Al)\b')
        
        #Files for storing information
        self.language = Path(os.path.dirname(__file__)) / 'Language'
        self.memory = Path(os.path.dirname(__file__)) / 'Memory'
        
        #Classes for doing stuff        
        self.learn = AL_teach(self)
        self.organiser = AL_organise(self)
        self._trainer_path = Path(os.path.dirname(__file__)) / 'train.txt'
        self._classifier = classifier(self._trainer_path)
        
        #Some memory stuff (not yet implemented files)
        self.greetings = ['Hi','Hey','Hello',"G'day"]
        self.names = ['Alec','Al']
        
        
        #Get rid of these global variables
        self.msg = ''
        self.user = ''
        
   
    async def message(self,msg,user):
        '''Recieves users message and tries to classify it'''
        #Does alec have a specific task to complete?
        try:
            r = await self.next_task[0](msg,self.next_args)            
            await self.chat_handler.reply(r)
            return
        except IndexError:
            pass #do nothing and continue along
                                  
        #Did the user refer to Alec? If not then don't do anything      
        if (self.said_my_name.search(msg) == None) and (self.wait_for_reply == False):
            #The message wasn't meant for me
            print('Message not for me')
            #A little surprise that will randomly pop up
            if random.randint(0,100) == 0:
                await self.chat_handler.reply('Talk to me!')
            return
        
        #Special case where only alec's name is mentioned
        if re.match(r'^(Alec|alec|al|Al).?$',msg):
            await self.chat_handler.reply(random.choice(['Yes?','What?',user]))
                           
        #Special case where a greeting is given. Check for greeting (e.g Hello Alec)
        exp = re.compile((r'(^' + re_combiner.combine_or_file(self.language/'greetings.txt') + 
                             r' \b' + re_combiner.combine_or(self.names) + r'\b)').lower())
        if exp.match(msg.lower()):
            reply_msg = '{} {}'.format(random.choice(self.greetings),user)
            await self.chat_handler.reply(reply_msg)
            
        #Check for a possible reminder using the classifiers
        if self._classifier.classify(msg) == 'pos':
            await self.chat_handler.reply('Do you want me to remind you?')
            self.next_task = [self.organiser.want_reminder]
   
    
    async def teach(self, msg, user):
        '''Teaches Alec something new (but related to what he already knows)'''
        r = await self.learn.init_teaching()
        await self.chat_handler.reply(r)
        
    async def organise(self, msg, user):
        '''Organises an event or reminder'''
        r = await self.organiser.remind_me(msg)
        #r = natural_time(msg)
        await self.chat_handler.reply(r)
        
        
                
            
            
        
        