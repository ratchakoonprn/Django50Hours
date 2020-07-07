# models.py
from django.db import models

class Allproduct(models.Model):
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True)
	imageurl = models.CharField(max_length=200, null=True, blank=True)
	instock = models.BooleanField(default=True)
	quantity = models.IntegerField(default=1)
	unit = models.CharField(max_length=200, default='-')

	image = models.ImageField(upload_to="products", null=True, blank=True)

	def __str__(self):
		return self.name
	