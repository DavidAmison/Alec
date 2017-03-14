"""
Created on Sat Mar  4 20:42:14 2017

Extract a date and or time from a string in a variety of formats

@author: David
"""

"""
Possible formats for date:
    Dates:
    25/04/94,25/04/1994, 25/04, 25th Apr, Apr 25th, April 25th
    The 25th of this month, The 25th of next month, 1 month today, 2 months today, in two weeks
    a week on saturday, tomorrow, yesterday, in two days, on Friday ...
    
    How to approach this problem?
    1) Parse the text, splitting into sections seperated by wither spaces or symboles
    2) Run through the text systematically analysing each 'word' and it's significance
    3) Return the best possible understanding
"""
from datetime import datetime, timedelta
import calendar
from dateutil import rrule

import num_parse

from textblob import TextBlob, Word
import re

#A dictionary of words that can be understood for mapping words of the same meaning and grouping
_date_words = {
        'second':['time','sec'],
        'seconds':['time','sec'],
        'sec':['time','sec'],
        'secs':['time','sec'],
        'minute':['time','min'],
        'minutes':['time','min'],
        'min':['time','min'],
        'mins':['time','min'],
        'hour':['time','hr'],
        'hours':['time','hr'],
        'hr':['time','hr'],
        'hrs':['time','hr'],
        'day':['time','day'],
        'days':['time','day'],
        'week':['time','wk'],
        'weeks':['time','wk'],
        'wk':['time','wk'],
        'month':['time','mth'],
        'months':['time','mth'],
        'mth':['time','mth'],
        'mths':['time','mth'],
        'year':['time','yr'],
        'yr':['time','yr'],
        'years':['time','yr'],
        'yrs':['time','yr'],
        'morning':['time','am'],
        'afternoon':['time','pm'],
        'evening':['time','pm'],
        'night':['time','am'],
        'am':['time','am'],
        'pm':['time','pm'],
        'monday':['day',0],
        'mon':['day',0],
        'tuesday':['day',1],
        'tue':['day',1],
        'wednesday':['day',2],
        'wed':['day',2],
        'thursday':['day',3],
        'thur':['day',3],
        'thu':['day',3],
        'friday':['day',4],
        'fri':['day',4],
        'saturday':['day',5],
        'sat':['day',5],
        'sunday':['day',6],
        'sun':['day',6],
        'weekend':['day','wk_end'],
        'weekends':['day','wk_end'],
        'january':['mth',1],
        'jan':['mth',1],
        'february':['mth',2],
        'feb':['mth',2],
        'march':['mth',3],
        'mar':['mth',3],
        'april':['mth',4],
        'apr':['mth',4],
        'apl':['mth',4],
        'may':['mth',5],
        'june':['mth',6],
        'jun':['mth',6],
        'july':['mth',7],
        'jul':['mth',7],
        'august':['mth',8],
        'aug':['mth',8],
        'september':['mth',9],
        'sept':['mth',9],
        'sep':['mth',9],
        'october':['mth',10],
        'oct':['mth',10],
        'november':['mth',11],
        'nov':['mth',11],
        'december':['mth',12],
        'dec':['mth',12],
        'yesterday':['rel','yest'],
        'today':['rel','td'],
        'tomorrow':['rel','tmrw'],
        'in':['rel','in'],
        'last':['rel','last'],
        'first':['rel','first'],
        'this':['rel','this'],
        'next':['rel','nxt'],
        'every':['rel','evy'],
        'at':['at','at'],
        'on':['on','on'],
        'for':['len','for'],
        'untill':['len','to'],
        'till':['len','to'],
        'to':['len','to']
        }

class Date_Parser():
    
    def __init__(self):
        #Variables for storing the date
        self.now = datetime.now()
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        #Perameters for that will be passed to rrule
        self.freq = rrule.MINUTELY          #Frequency can be either rrule.YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY or SECONDLY
        self.dtstart = datetime.now()       #Start from today
        self.interval = 1
        self.wkstart = None
        self.count = 1                      #Returns only one instance as default
        self.until = None
        self.bysetpos = None
        self.bymonth = None
        self.bymonthday = None
        self.byyearday = None
        self.byweekno = None
        self.byweekday = None #0 = Monday ... 6 = Sunday
        self.byhour = None
        self.byminute = None
        self.bysecond = 0 #Default to 0 seconds (who needs to be that accurate anyway??)
        #Dictionary for mapping functions
        #Dictionary mapping tags to specific functions
        self._tag_func = {
                'time':self.time_tag,
                'day':self.day_tag,
                'mth':self.mth_tag,
                'rel':self.rel_tag,
                'at':self.at_tag,
                'on':self.on_tag,
                'len':self.len_tag,
                'num':self.on_tag,
                }  
           
        
    def parse_string(self,s):
        #First make the string all lower case, then split up all the words
        s = s.lower()
        #convert all numerical text to numbers (one => 1, second => 2nd etc
        s = num_parse.convert_num(s)
        tb = TextBlob(s)
        words = tb.words
        #map and group the words using _date_words 
        date_mapped = [(_date_words[w] if w in _date_words else w) for w in words]
        #remove all non-important words and tag numbers
        date_tagged = []
        for item in date_mapped:
            if self.contains_digit(item):
                date_tagged.append(['num',item])
            elif len(item) == 2:
                date_tagged.append(item)        
        #Cycle through everything and try to interpret the meaning of all the numbers
        self.interpret_num(date_tagged)
        print(date_tagged)
        #Now the numbers are turned to proper numbers and the words are tagged try to understand
        #self.interpret_tags(date_tagged)
        #Are there any 'rel' tags in the words. e.g every, tomorrow, next
        '''
        date = list(rrule.rrule(self.freq, self.dtstart, self.interval, self.wkstart, self.count, self.until,
                                self.bysetpos, self.bymonth, self.bymonthday, self.byyearday, self.byweekno,
                                self.byweekday, self.byhour, self.byminute, self.bysecond)
        '''
       
    def contains_digit(self,st):
        try:
            return any(c.isdigit() for c in st)
        except Exception:
            return False 
    
    def interpret_num(self,st_tagged):
        '''
        Seeks to understand the meening of each item tagged with the 'num' tag.
        Is it a day? Month? Time? Date? etc
        '''
        i = 0
        for item in st_tagged:            
            if item[0] != 'num':
                i += 1
                continue
            #Check if the number is some form of time or date.
            time = self.is_time(item[1])
            date = self.is_date(item[1])
            #Interpret the time or date
            if time != None:
                st_tagged[i] = time
            elif date != None:
                st_tagged[i] = date
            i += 1
            
     
    def is_time(self,st):
        '''
        Recognized formats: 7am, 7:00:00 7:00am (given 'time' tag)
        7hr, 7s/sec, 7min (given 'rel_t' tag)        
        '''
        morning = None
        hour = 0
        minute = 0
        second = 0
        
        #Check for s, sec, min or hr at end of word
        matches = re.search(r'(\d+(?=(s|sec|secs)\b))',st)
        if matches:
            second = int(matches.group(1))
        matches = re.search(r'(\d+(?=(min|mins)\b))',st)
        if matches:
            minute = int(matches.group(1))
        matches = re.search(r'(\d+(?=(hr|hrs)\b))',st)
        if matches:
            hour = int(matches.group(1))
        
        if hour+minute+second > 0:
            return ['rel_t',[hour,minute,second]]

        #Check for am or pm at the end of the word
        am_pm = re.search(r'(am|pm)$',st)
        try:
            if am_pm.group(1) == 'am':
                morning = True
            else:
                morning = False
        except AttributeError:
            pass    
        #Check for ##:## format
        if ':' in st:
            time = re.findall(r'(\d{1,2})',st)
            if time:
                try:
                    hour = int(time[0])
                    minute = int(time[1])
                    second = int(time[2])
                except IndexError:
                    pass
            else:
                return None
        else:
            return None
        
        if morning == False and hour < 12:
            hour += 12
        
        return ['tm',[hour,minute,second]]
    
    def is_date(self,st):
        '''
        Purpose of this function is to interpret numbers as they relate do dates
        returns ['date',[d,m,y]] where any of these items can be None
        Recognized formats: 
        25/04/1994, 25/04, 3rd, 25-04-1994, 25.04.1994
        Note: will asuume date is of the order day-month-year unless it is explicilty
        obvious e.g 04/25 is obviously mm/dd
        '''
        day = None
        month = None
        year = None
        #First check for the st, th, nd, rd endings
        matches = re.match(r'\d+(?=(st|th|nd|rd)\b)',st)
        if matches:
            #Assumption is that a month day is referred to
            day = matches.group(0)
            return ['date',[day,month,year]]
            
        #Now check for the seperated values format (seperated by . or / or -)
        if any(c in st for c in ['.','-','/','\\']):
            matches = re.findall(r'(\d{1,4})',st)
            #How many matches are there
            n = len(matches)
            if n == 2:
                if int(matches[1]) > 12:
                    month = int(matches[0])
                    day = int(matches[1])
                else:
                    month =int(matches[1])
                    day = int(matches[0])
                return ['date',[day,month,year]]
            elif n == 3:
                if int(matches[1]) > 12:
                    year = int(matches[2])
                    month = int(matches[0])
                    day = int(matches[1])
                else:
                    year = int(matches[2])
                    month = int(matches[1])
                    day = int(matches[0])
                #Check if the year was a 2 digit or 4 digit number
                if year < 1000:
                    year += 2000 #We are probably going to be in the 21st century...
                return ['date',[day,month,year]]
            else:
                return None
        else:
            return None
            
        
        
                
    
    def interpret_tags(self,st_tagged):
        '''
        Tries to understand the meaning of a the phrase in relation to dates and time.           
        '''
        #Work through each word, analysing the tag and meaning.
        i = 0
        for w in st_tagged:
            #Note that once anything has been interpreted (even if by another function) it is not looked at again
            self._tag_func[w[0]](st_tagged,i)  
            i += 1
        print(self.freq)
        print(self.dtstart)
        print(self.byweekday)
        print(self.byhour)
        print(self.byminute)
        print(self.bymonth)
        print(self.bymonthday)
            
        
    def time_tag(self,st_tagged,i):
        return
    
    def day_tag(self,st_tagged,i):
        return
    
    def mth_tag(self,st_tagged,i):
        return
    
    def rel_tag(self,st_tagged,i):
        '''
        Interprets items with the relative (rel) tag
        Words included in this tag are: yesterday (yest), today (td), tomorrow (tmrw)
        last (last), this (this), next (nxt), every (evy)
        '''
        #TODO case where word is first
        #First find out which instance of the tag we are looking at
        word = st_tagged[i][1]
        if word == 'yest':
            pass
        elif word == 'td':
            #Set start date to today
            date = self.now
            self.byyear = date.year
            self.bymonth = date.month
            self.byday = self.day           
        elif word == 'tmrw':
            #Set start date to tomorrow at 00:00
            date = self.now + timedelta(days=1)
            date.replace(hour = 0, minute = 0, second = 0)
            self.byyear = date.year
            self.bymonth = date.month
            self.byday = self.day
        elif word == 'last':
            try:
                last_what = st_tagged[i+1] #should be tagged as [time,day] or [day,(day)]
                if last_what[0] == 'day':
                    self.byweekday = last_what[1]
                    self.bymonthday = -1
                    del st_tagged[i+1]
                elif last_what[1] == 'day':
                    self.bymonthday = -1
                    del st_tagged[i+1]
                else:
                    print('Unexpected format: last')
            except IndexError:
                print('Unexpected format: last')
                           
            #Done analysis, now remove
            del st_tagged[i]
        elif word == 'nxt' or word == 'this':
            #Next word should be one of: year, month, week, [month], [day]
            try:
                next_what = st_tagged[i+1]
                if next_what[0] == 'day':
                    date = (self.now + timedelta(days=7)).replace(hour=23,minute=59,second=59)                
                    self.count = None
                    self.until = date
                    self.byweekday = next_what[1]
                    del st_tagged[i+1]
                elif next_what[0] == 'mth':
                    date = (self.now + timedelta(days=366 if calendar.isleap(self.now.year) else 365))
                    max_day = calendar.monthrange(date.year,date.month)[1]
                    date = date.replace(day=max_day,hour=23,minute=59,second=59)
                    self.count = None
                    self.until = date
                    self.bymonth = next_what[1]
                    del st_tagged[i+1]
                elif next_what[1] == 'yr':
                    self.byyear = self.now.year + 1
                    del st_tagged[i+1]
                elif next_what[1] == 'mth':
                    month_days = calendar.monthrange(self.now.year,self.now.month)[1]
                    self.bymonth = (self.now + timedelta(days=month_days)).month
                    del st_tagged[i+1]
                elif next_what[1] == 'wk':
                    date = self.now + timedelta(days=7)
                    self.byyear = date.isocalendar()[0]
                    self.byweek = (self.now + timedelta(days=7)).isocalendar()[1]
                    del st_tagged[i+1]
                elif next_what[1] == 'day':
                    date = self.now + timedelta(day=1)
                    self.byyear = date.year
                    self.bymonth = self.month
                    self.byday = date.weekday()
                    del st_tagged[i+1]
                else:
                    print('Unexpected format: next/this')
            except IndexError:
                print('Unexpected format: next/this')
            
            del st_tagged[i] 
        elif word == 'evy':
            
            del st_tagged[i]
        return
    
    def at_tag(self,st_tagged,i):
        return
    
    def on_tag(self,st_tagged,i):
        return
    
    def len_tag(self,st_tagged,i):
        '''
        Interprets items with the 'len' tag which includes the words 'for'
        and 'to'
        '''
        word = st_tagged[i][1]
        if word == 'for':
            #TODO (sort out later)
            del st_tagged[i]
            if st_tagged[i+1][0] == 'num': del st_tagged[i+1]
        elif word == 'to':
            #TODO add functionality to consider number before and after
            del st_tagged[i]
            if st_tagged[i+1][0] == 'num': del st_tagged[i+1]
            pass
        
        
        pass
        