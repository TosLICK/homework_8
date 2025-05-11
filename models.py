from bson import json_util
from mongoengine import Document, StringField, ReferenceField, ListField, BooleanField, CASCADE


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {'collection': 'authors'}

class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {'collection': 'quotes'}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data['author'] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
    
class Contact(Document):
    fullname = StringField(max_length=50)
    email = StringField(max_length=50)
    phone = StringField(max_length=50)
    prefered_channel = StringField(max_length=10, choices=['email', 'sms'])
    sent_message = BooleanField(default=False)
    meta = {'collection': 'contacts'}
