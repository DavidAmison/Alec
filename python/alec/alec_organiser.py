"""
Created on Fri Mar  3 19:17:27 2017

@author: David
"""
#import ast #For safely evaluating strings to literals

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from pathlib import Path
import os

from . import alec

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
        self._rmd = {'ID':None,'Name':None,'Date':None,'Time':None,'Msg':None}
        self._ev = {'ID':None,'Name':None,'Date_st':None,'Time_st':None,'Date_fin':None,'Time_fin':None,'Location':None,'Msg':None}
        self.next_id = 1
        
        self.scheduler = AsyncIOScheduler() #The scheduler for Alec to place reminders
        
    
    async def remind_me(self,msg='',args=[]):
        '''Starts the process of Alec making a new reminder'''
        #Fist make sure dictionaries are empty
        self.reset_event(self._rmd)
        self.reset_event(self._ev)
        self._rmd['ID'] = self.next_id
        self.next_id += 1
        #Request the event name and set the next step
        self.AL.next_task = [self.event_name]
        return 'What do you want to call the event?'
        
    async def event_name(self,msg='',args=[]):
        '''Extracts the event name from the user message'''
        self._rmd['Name'] = msg
        self.AL.next_task = [self.event_date]
        return 'What date do you want me to send you a reminder?'
        
    async def event_date(self,msg='',args=[]):
        '''extraxts the event date from the user message'''
        self._rmd['Date'] = msg
        self.AL.next_task = [self.event_time]
        return 'What time do you want me to remind you?'
        
    
    async def event_time(self,msg='',args=[]):
        '''Extracts the time from the user message'''
        self._rmd['Time'] = msg
        self.AL.next_task = [self.event_msg]
        return 'What do you want me to say?'
        
    async def event_msg(self,msg='',args=[]):
        '''Extraxts the message for the reminder/event'''
        self._rmd['Msg'] = msg
        self.AL.next_task = ''
        #Add the event to the file
        f = open(str(self._reminders),'a')
        f.write(str(self._rmd)+'\n')
        f.close()       
        return 'Reminder set {}'.format(str(self._rmd))        
        
    async def reset_event(self,d):
        '''Set all values in d to none'''
        for key in d:
            d[key] = None
            
        
        
    
    
    
    
    