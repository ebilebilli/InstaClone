from posts.models import User
from direct_messages.models import DirectMessage
from posts.models import User, Post, Story


class DirectMessageRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'direct_messages':
            return 'mongo'  
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'direct_messages':
            return 'mongo'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if isinstance(obj1, User) and isinstance(obj2, DirectMessage):
            return True
        if isinstance(obj1, DirectMessage) and isinstance(obj2, User):
            return True
        if isinstance(obj1, Post) and isinstance(obj2, DirectMessage):
            return True
        if isinstance(obj1, DirectMessage) and isinstance(obj2, Post):
            return True
        if isinstance(obj1, Story) and isinstance(obj2, DirectMessage):
            return True
        if isinstance(obj1, DirectMessage) and isinstance(obj2, Story):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'direct_messages':
            return db == 'mongo'
        return db == 'default'
