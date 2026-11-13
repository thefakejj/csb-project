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

# # logging (to identify brute force attacks?)
# class Log(models.Model):
#       action = models.CharField(max_length=64)
#       username = models.CharField(max_length=64, null=True)
#       ip = models.GenericIPAddressField(null=True)
#       time = models.CharField(max_length=256, null=True) # saves the time of the log in this form: "Sun Jun 20 23:21:05 1993" (python docs)
# # https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django

# @receiver(user_logged_in)
# def user_logged_in_callback(request, user, **kwargs):  
#     ip = request.META.get('REMOTE_ADDR')
#     Log.objects.create(action='user_logged_in', ip=ip, username=user.username, time=asctime(gmtime()))


# @receiver(user_logged_out)
# def user_logged_out_callback(request, user, **kwargs):  
#     ip = request.META.get('REMOTE_ADDR')
#     Log.objects.create(action='user_logged_out', ip=ip, username=user.username, time=asctime(gmtime()))


# @receiver(user_login_failed)
# def user_login_failed_callback(credentials, **kwargs):
#     Log.objects.create(action='user_login_failed', username=credentials.get('username', None), time=asctime(gmtime()))
