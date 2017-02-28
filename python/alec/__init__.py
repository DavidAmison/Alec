from skybeard.beards import BeardChatHandler
from skybeard.predicates import Filters
import asyncio

import re
from textblob import TextBlob
from textblob import Word

import random

from . import alec

class AlecChat(BeardChatHandler):

    __commands__ = [
        (Filters.text_no_cmd, 'start',
         'Repeats back what is given'),
        ('teach','teach',
         'Teach Alec to recognise certain input'),
        ('talk','talk',
         'Puts Alec into conversation mode'),
    ]
    
    user_name = ''
    
    __userhelp__ = """Personal Assistant: Start by typing Hi Alec."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.AL = alec.Alec(self)
        self.msg_text = ''
        self.msg_username = ''
    
    #greetings = ['Hi','Hey','Hello']


    async def start(self, msg):
        #Deconstruct the message to try and find out what is wanted
        print('Message Recieved')
        #Extract Data
        self.msg_text = msg['text']
        self.msg_username = msg['from']['first_name']    
        
        #Check whether AL is waiting for a reply
        if self.AL.wait_for_reply:
            print('Waiting for Reply')
            self.AL.wait_for_reply = False
        else:                    
            await self.AL.message(self.msg_text, self.msg_username)
            
    async def teach(self,msg):
        print('Command Recieved: Teach')
        self.msg_text = msg['text']
        self.msg_username = msg['from']['first_name']
        await self.AL.teach(self.msg_text, self.msg_username)

            
    async def talk(self,msg):
        print('Command Recieved: Talk')
        self.AL.talk()
        await self.sender.sendMessage("I'm ready to talk")
        
    
    async def input(self):
        '''Waits for the user to send input'''
        reply = await self.listener.wait()
        print(reply)
        self.msg_text = reply['text']
        self.msg_username = reply['from']['first_name']    
        return self.msg_text, self.user_name
    
    async def reply(self, msg):
        await self.sender.sendMessage(msg)