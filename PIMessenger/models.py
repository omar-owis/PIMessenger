from PIMessenger import db
from PIMessenger.enums import *


class Events(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.Enum(EventType))
    message = db.Column(db. String(300))
    execute_time = db.Column(db.String(100))
    random_delay_sec = db.Column(db.Integer)
    reply_username = db.Column(db.String(75))
    reply_trigger_message = db.Column(db.String(300))
    reply_limit_daily = db.Column(db.Boolean)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.messenger_ID'))
    
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.message = kwargs['message']
        self.execute_time = kwargs['execute_time']
        self.reply_username = kwargs['reply_username']
        self.reply_trigger_message = kwargs['reply_trigger_message']
        self.reply_limit_daily = Bool(kwargs['reply_limit_daily'])
        self.chat_id = int(kwargs['chat_id'])
        self.type = EventType(kwargs['type'])
        self.random_delay_sec = int(kwargs['random_delay_sec'])
    
    def __setattr__(self, name, value):    
        if name == 'type':
            value = EventType(value)
        elif name == 'random_delay_sec' or name == 'chat_id':
            value = int(value)
        elif name == 'reply_limit_daily':
            value = Bool(value)
            
        super().__setattr__(name, value)
        
    
class Accounts(db.Model):
    username = db.Column(db.String(75), primary_key=True)
    password = db.Column(db.String(75))
    chats = db.relationship('Chats', backref='account')
  
class Chats(db.Model):
    messenger_ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    owner_account = db.Column(db.String(75), db.ForeignKey('accounts.username'))
    type = db.Column(db.Enum(ChatType))
    events = db.relationship('Events', backref='chat')
    
    def __init__(self, **kwargs):
        self.messenger_ID = int(kwargs['messenger_ID'])
        self.name = kwargs['name']
        self.owner_account = kwargs['account']
        self.type = ChatType(kwargs['type'])
        

    def __setattr__(self, name, value):
        if name == 'type':
            value = ChatType(value)
        elif name == 'messenger_ID':
            value = int(value)
        elif name == 'account':
            name = 'owner_account'
        
        super().__setattr__(name, value)