from django.shortcuts import render
from .serilizers import RegistrationSerializers
from django.views.generic import View
from rest_framework.views import APIView
import json
from django.contrib.auth.hashers import make_password,check_password
from .models import Registration,User_files
import zipfile
from django.http import HttpResponse
import os
from django.shortcuts import get_object_or_404
# Create your views here.


def registrationpg(request):
    return render(request,'registration.html')

class RegistrationApi(APIView):

    def post(self,request,*args,**kwargs):
        data=request.data
        name=data.get('name')
        contact=data.get('contact')
        email=data.get('email')
        address=data.get('address')
        password=data.get('password')
        hashed_password=make_password(password)

        if Registration.objects.filter(email=email).exists():
            return render(request,'registration.html',{'msg':'email already exists'})
        else:
            Registration.objects.create(name=name,contact=contact,email=email,address=address,password=hashed_password)
            return render(request,'login.html')

def login(request):
    return render(request,'login.html')

class LoginAPi(APIView):
    def post(self,request):
        data=request.data
        email=data.get('email')
        password=data.get('password')

        if Registration.objects.filter(email=email).exists():
            user=Registration.objects.get(email=email)
            dbpassword=user.password
            if check_password(password,dbpassword):
                return render(request,'uploadfile.html',{'id':user})
            else:
                return render(request,'login.html',{'msg':'password was incorrect'})

def upload_files(request):
    return render(request,'uploadfile.html')

def upload_files_data(request):
    if request.method=='POST':
        user_id=request.POST['id']
        profile_photo=request.FILES.get('profile_photo')
        aadhar_card=request.FILES.get('aadhar_card')
        pan_card=request.FILES.get('pan_card')
        voter_id=request.FILES.get('voter_id')
        marksheet=request.FILES.get('marksheet')

        if User_files.objects.filter(userid=user_id).exists():
            data = User_files.objects.get(userid=user_id)
            print(data)
            return render(request,'uploadfile.html',{'msg':'document already uploaded','id':data})
        
        else:
            user=User_files.objects.create(userid=user_id,profile_photo=profile_photo,aadhar_card=aadhar_card,
                                  pan_card=pan_card,voter_id=voter_id,marksheet=marksheet)
    

            if User_files.objects.filter(userid=user_id).exists():
                data=User_files.objects.get(userid=user_id)
                print('user data',data)
                return render(request,'downloadpg.html',{'user':data})
            
def download(request,id):
    data=User_files.objects.get(userid=id)
    return render(request,'downloadpg.html',{'user':data})


def download_files_as_zip(request, user_id):
    if request.method == 'GET':
        # Check if the user exists and matches the authenticated user

        user = User_files.objects.get(userid=user_id)



        # Assuming you have a user model with file fields
        files_to_download = [
            user.profile_photo,  # Replace with the file fields in your model (e.g., user.aadhar_card, user.pan_card, etc.)
            # Add other files here
        ]

        # Create a ZIP archive in memory
        memory_file = zipfile.ZipFile('files.zip', 'w')
        for file_to_download in files_to_download:
            if file_to_download:
                memory_file.write(file_to_download.path, file_to_download.name)

        # Close the in-memory ZIP file
        memory_file.close()

        # Create a response with the ZIP content
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{user}_files.zip"'

        # Open the created ZIP file and write its content to the response
        with open('files.zip', 'rb') as f:
            response.write(f.read())

        # Clean up temporary files
        memory_file.close()
        os.remove('files.zip')

        return response