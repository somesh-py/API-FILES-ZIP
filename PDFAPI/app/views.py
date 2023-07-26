from django.shortcuts import render
from .serilizers import RegistrationSerializers
from django.views.generic import View
from rest_framework.views import APIView
import json
from django.contrib.auth.hashers import make_password,check_password
from .models import Registration,User_files
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