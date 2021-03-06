# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:48:57 2017

Takes messages in the following format:
    {'chat_id':'...','user_id':'...','msg':'...','user_name':'...'}

@author: David
"""
from textblob import TextBlob
import random
import re
import asyncio

import os
from pathlib import Path
from . import re_combiner

class Alec():
    
    def __init__(self, ch):
        print('Alec being created')
        self.chat_handler = ch #Handles input and output requests 
        '''
        Chat handler must have the following funcions:
        input - must wait for input to be recieved
        reply - will be sent a string and should output it        
        '''
        #TODO This is a string telling Alec what to do with the next input he recieves
        self.next_task = ''
        self.wait_for_reply = False
        
        self.said_my_name = re.compile(r'\b(Alec|alec|al|Al)\b')
        
        
        self.language = Path(os.path.dirname(__file__)) / 'language'
        self.memory = Path(os.path.dirname(__file__)) / 'memory'
        
        #Some memory stuff (not yet implemented files)
        self.greetings = ['Hi','Hey','Hello',"G'day"]
        self.names = ['Alec','Al']
        
        #Mode can be 'talk', 'teach'
        self.mode = 'talk'
        
        self.learning = 0
        self.__learning_dict = {1:'Greetings'}
        self.__learningfiles = {1:self.language/'greetings.txt'}
        self.__learning_max = 2
        
        self.msg = ''
        self.user = ''
        
   
    async def message(self,msg,user):
        '''Recieves users message and trues to classify it'''
        #Did the user refer to Alec      
        if (self.said_my_name.search(msg) == None) and (self.wait_for_reply == False):
            #The message wasn't meant for me
            print('Message not for me')
            #A little surprise that will randomly pop up
            if random.randint(0,100) == 0:
                await self.chat_handler.reply('Talk to me!')
            return
        
        #Special case where only alec's name is mentioned
        if re.match(r'^(Alec|alec|al|Al).*$',msg):
            await self.chat_handler.reply(random.choice(['Yes?','What?','David!']))
            
        
        
        #Check for greeting
        exp = re.compile((r'(^' + re_combiner.combine_or(self.greetings) + r' \b' + re_combiner.combine_or(self.names) + r'\b)').lower())
        if exp.match(msg.lower()):
            reply_msg = '{} {}'.format(random.choice(self.greetings),user)
            await self.chat_handler.reply(reply_msg)
      
            
    async def teach(self, msg, user):
        '''Teaches Alec something new (but related to what he already knows)'''
        await self.chat_handler.reply(
                '''What do you want to teach me?
                    1) Greetings
                    2) Nothing''')        
        
        self.wait_for_reply = True
        while self.wait_for_reply:
            self.msg, self.user = await self.chat_handler.input()
            try:
                num = int(re.search(r'(\d+)', self.msg, re.IGNORECASE).group(1))
            except:
                return "Sorry I can't learn that."
            if num < self.__learning_max:
                self.wait_for_reply = False
        
        await self.chat_handler.reply('Enter the word or phrase you want me to learn.')
        self.msg, self.user = await self.chat_handler.input()
        #TODO Need to make this look for the correct variable
        self.greetings.append(self.msg)
        
        reply = "Learned new {}: {}".format(self.__learning_dict[num],self.msg)        
        await self.chat_handler.reply(reply)    
        await self.chat_handler.reply(str(self.greetings))            

        
        async def talk(self):
            self.mode = 'talk' 
            
        async def reply(self, msg, user_id):
            
            return
                
            
            
        
        