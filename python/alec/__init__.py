from skybeard.beards import BeardChatHandler
from skybeard.predicates import Filters

from . import alec

class AlecChat(BeardChatHandler):

    __commands__ = [
        (Filters.text_no_cmd, 'start',
         'Does stuff'),
        ('teach','teach',
         'Teach Alec to recognise certain input'),
        ('talk','talk',
         'Puts Alec into conversation mode'),
        ('organise','organise',
         'Organises a reminder or an event'),
    ]
    
    __userhelp__ = """Personal Assistant: Start by typing Hi Alec."""
    
    _timeout = 90
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.AL = alec.Alec(self)
        self.msg_text = ''
        self.msg_username = ''
    
    #greetings = ['Hi','Hey','Hello']


    async def start(self, msg):
        #Deconstruct the message to try and find out what is wanted
        print('Message Recieved')
        #Extract Data and put in correct format for Alec
        #TODO AL_msg = {'chat_id':'','user_id':'','msg':msg['text'],'user_name':msg['from']['first_name']}
        self.msg_text = msg['text']
        self.msg_username = msg['from']['first_name']
        #Check whether AL is waiting for a reply
        if self.AL.wait_for_reply:
            print('Waiting for Reply')
            self.AL.reply(self.msg_text, self.msg_username)
        else:                    
            await self.AL.message(self.msg_text, self.msg_username)
            
    async def teach(self,msg):
        print('Command Recieved: Teach')
        self.msg_text = msg['text']
        self.msg_username = msg['from']['first_name']        
        await self.AL.teach(self.msg_text, self.msg_username)

    async def organise(self,msg):
        print('Command Recieved: Organise')
        self.msg_text = msg['text']
        self.msg_username = msg['from']['first_name']
        await self.AL.organise(self.msg_text,self.msg_username)
        
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