from django.db import models

class sample(models.Model):
	package = models.TextField(null= True)
	md5hash = models.CharField(max_length=50)
	upload_location = models.TextField(null= True)
	static_location = models.TextField(null= True)
	dynamic_location = models.TextField(null= True)
	download_location = models.TextField(null= True)
	upload_time = models.DateTimeField(null= True)
	static_time = models.DateTimeField(null= True)
	dynamic_time = models.DateTimeField(null= True)
	static_status = models.IntegerField(null= True)
	dynamic_status = models.IntegerField(null= True)
	manual_status = models.IntegerField(null= True)
	manual_location = models.TextField(null= True)
	manual_time = models.DateTimeField(null= True)

	def __unicode__(self):
		return self.md5hash