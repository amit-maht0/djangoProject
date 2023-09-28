from django.shortcuts import render
from .models import UserModel, PostModel
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate , login
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# Create your views here.

'''
Login Code to login user if user is registered, and then redirect to post page.
Sending token to url to get userId for creating post
'''
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
   
        user_obj = UserModel.objects.filter(email = email).values('email','id', 'password','is_active').first()  
        #print(user_obj)
        if user_obj is not None:
            match_password = check_password(password,user_obj['password'])
           
            if user_obj['email'] == email and match_password == True:
                user_data = UserModel(**user_obj)
                refresh = RefreshToken.for_user(user_data)
                
                token = str(refresh.access_token)
            
                return redirect(f'/post/?token={token}')
               
            else:
                messages.warning(request, "UserModel not found!")
                return HttpResponseRedirect(request.path_info)

    return render(request,'login.html')


'''
Registeration Code to register user and then redirect to login page
'''

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        followers = request.POST.get('followers')
        following = request.POST.get('following')
        password = request.POST.get('password')
        hashed_password = make_password(password)
        is_verified = True
        user_obj = UserModel.objects.filter(email = email)
        if(user_obj.exists()):
            messages.warning(request,"Email already exist!")
            return HttpResponseRedirect(request.path_info)
        user_obj = UserModel.objects.create(name = name, email = email, followers = followers, following = following,password=hashed_password, is_verified = is_verified)
        user_obj.save()
        messages.success(request,"Successfully Registered!")

        return redirect('login')
    return render(request,'register.html')

'''
Post Code to create post by user, sending user id in url to create post according to user
'''
def post(request):
    if request.method == 'POST':
        
        userId = request.POST.get('userId')
        print(userId)

        post = request.POST.get('posts')
        print(post)
        post_obj = PostModel.objects.create(user_id_id = userId, post = post)
        post_obj.save()
        messages.success(request,"Successfully Created Post!")

        return redirect(f'/details/?userId={userId}')
    return render(request,'post.html')

'''
Code to get user details and post
'''

def details(request):
    userId = request.GET.get('userId')
    print(userId)
    user = UserModel.objects.filter(id=userId).values('email','id','name','is_active', 'followers', 'following').first()
    print(user)
    get_post = PostModel.objects.filter(user_id=userId).values('post','user_id')
   
    posts = list(get_post.values())
    print(posts)
    return render(request,'details.html',{'user':user,'posts':posts})

def home(request):
    return render(request,'home.html')

