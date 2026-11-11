from django.db import models

 
from django.contrib.auth.models import User

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from time import gmtime, asctime
 
# Create your models here.
 
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)
 
class File(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	data = models.FileField(upload_to=user_directory_path)

# https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django
class Logs(models.Model):
      action = models.CharField(max_length=64)
      username = models.CharField(max_length=64, null=True)
      ip = models.GenericIPAddressField(null=True)
      time = asctime(gmtime) # saves the time of the log in this form: "Sun Jun 20 23:21:05 1993" (python docs)
