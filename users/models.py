from email.policy import default
from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel): 
    name         = models.CharField(max_length=50)
    contact      = models.CharField(max_length=50, unique=True)
    is_blacklist = models.BooleanField(default=0)

    class Meta: 
        db_table = 'users'