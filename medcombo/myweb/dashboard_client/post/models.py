from django.db import models
from datetime import datetime
from medcombo.configuration.usercustom.models import User, Company
from medcombo.crm.dashboard_admin.models import LanguageCampaign

# Create your models here.
def content_file_post_image(instance, filename):
  return 'post/{1}'.format(instance, filename)


class Post(models.Model):
	title = models.CharField(max_length=50)
	description= models.TextField()
	date = models.DateField(default=datetime.now, blank=True)
	image = models.ImageField(upload_to=content_file_post_image, blank=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	company = models.ForeignKey(Company, null=True, blank=True, related_name='post_relationship', on_delete=models.SET_NULL)
	language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
