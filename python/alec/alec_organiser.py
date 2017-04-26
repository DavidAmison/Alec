"""
Created on Fri Mar  3 19:17:27 2017

@author: David
"""
#import ast #For safely evaluating strings to literals


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger 
from datetime import datetime
from natural_time import natural_time

from pathlib import Path
import os

#from . import alec
#from . import date_time_parser

class AL_organise():
    #Class for creating and organising reminders and events.
    
    def __init__(self,alec_i):
        '''On initialisation Alec goes through the database and re-activates all events and reminders'''
        self.AL = alec_i
        #Database for storing reminders
        self._reminders = Path(os.path.dirname(__file__)) / 'Organise' / 'reminders.txt'
        self._events = Path(os.path.dirname(__file__)) / 'Organise' / 'events.txt'
        '''
        Reminders Format: ID #### Name ... Date ##/##/## Time ##:## Msg ...
        Events Format: ID #### Name ... Date_st ##/##/## Time_st ##:## Date_fin ##/##/## Time_fin ##:## Location ... Msg ...
        '''
        #Dictionaries for constructing the reminders
        self._rmd = {'ID':None,'Name':None,'DateTime':None,'Msg':None}
        self._ev = {'ID':None,'Name':None,'Date_st':None,'Time_st':None,'Date_fin':None,'Time_fin':None,'Location':None,'Msg':None}
        self._datetime = None
        self.next_id = 1
        
        self.scheduler = AsyncIOScheduler() #The scheduler for Alec to place reminders
        self.scheduler.start()
        
    async def interpret(self, msg):
        return str(natural_time(msg))
    
    async def triggered(self,msg=''):
        #Extract the message
        await self.AL.chat_handler.reply(msg)
        
    
    async def remind_me(self,msg='',args=[]):
        '''Starts the process of Alec making a new reminder'''
        #Fist make sure dictionaries are empty
        self.reset_event(self._rmd)
        self.reset_event(self._ev)
        self._rmd['ID'] = str(self.next_id)
        self.next_id += 1
        #Request the event name and set the next step
        self.AL.next_task = [self.AL.organiser.event_name]
        return 'What do you want to call the event?'
        
    async def event_name(self,msg='',args=[]):
        '''Extracts the event name from the user message'''
        self._rmd['Name'] = msg
        self.AL.next_task = [self.AL.organiser.event_date]
        return 'When do you want me to send you a reminder?'
        
    async def event_date(self,msg='',args=[]):
        '''extraxts the event date from the user message'''
        self._datetime = natural_time(msg)
        if self._datetime == []:
            return "Sorry, that date didn't make sense. When is the event?"
        self._rmd['DateTime'] = str(self._datetime)
        self.AL.next_task = [self.AL.organiser.event_msg]
        return 'Reminder will be set for {}. What do you want me to say?'.format(str(self._datetime))
        
    async def event_msg(self,msg='',args=[]):
        '''Extraxts the message for the reminder/event'''
        self._rmd['Msg'] = msg
        self.AL.next_task = ''
        #Add the event to the file
        f = open(str(self._reminders),'a')
        f.write(str(self._rmd)+'\n')
        f.close()   
        #Add the event to the scheduler
        self.scheduler.add_job(self.triggered,trigger=DateTrigger(self._datetime),id=self._rmd['ID'],args=[msg])
        return 'Reminder set {}'.format(str(self._rmd))        
        
    async def reset_event(self,d):
        '''Set all values in d to none'''
        for key in d:
            d[key] = None
            
        
        
    
    
    
    
    