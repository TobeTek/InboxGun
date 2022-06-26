import factory
from django.contrib.auth import get_user_model
from .. import models 

class RandomUserFactory(factory.Factory):
    class Meta:
        model = get_user_model()
    
    username = factory.Faker('first_name')
    password = factory.Faker('password')
    email = factory.LazyAttribute(lambda a: '{}@example.com'.format(a.username).lower())

class RandomPostFactory(factory.Factory):
    class Meta:
        model = models.Post 
    
    title = factory.Faker('sentence')
    author = RandomUserFactory()
    body = factory.Faker('text')
    status = 'draft'

