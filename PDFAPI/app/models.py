from django.db import models

# Create your models here.

class Registration(models.Model):
    name=models.CharField(max_length=50)
    contact=models.IntegerField()
    email=models.EmailField(max_length=254)
    address=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

class User_files(models.Model):
    userid=models.IntegerField()
    profile_photo=models.ImageField(upload_to='profile_photos')
    aadhar_card=models.ImageField(upload_to='aadhar_photos')
    pan_card=models.ImageField(upload_to='pan_card_photos')
    voter_id=models.ImageField(upload_to='voter_id_photos')
    marksheet=models.ImageField(upload_to='marksheet_photos')