from django.contrib import admin
from .models import Registration,User_files
# Register your models here.

@admin.register((Registration))
class RegistrationModelAdmin(admin.ModelAdmin):
    list_display=['id','name','contact','email','address','password']

@admin.register((User_files))
class User_filesModelAdmin(admin.ModelAdmin):
    list_display=['id','userid','profile_photo','aadhar_card','pan_card','voter_id','marksheet']