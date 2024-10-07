from django.shortcuts import render
from django.http import JsonResponse
from .models import Blog
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import BlogSerializer, UserSerializer
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.forms import model_to_dict
from .tokens import get_token_for_user

# Create your views here.

# blogs = [
#     {'id': 1, 'title': 'Blog 1', 'content': 'This is blog 1 content'},
#     {'id': 2, 'title': 'Blog 2', 'content': 'This is blog 2 content'},
#     {'id': 3, 'title': 'Blog 3', 'content': 'This is blog 3 content'}
# ]

# def list_blogs(request, *args, **kwargs):
#     body = request.body
#     blogs = Blog.objects.all()
#     data =  []
#     try:
#         if blogs:
#             for blog in blogs:
#                 data.append({'id': blog.id, 'title': blog.title, 'content': blog.content})
#             return JsonResponse({'data': data}, status=200)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'data': 'welcome'})

# def get_blog(request):
    # blog_id = request.GET.get('id')
    # data = {}
    # try:
    #     if blog_id is None:
    #         return JsonResponse({'error': 'Blog id is required'}, status=400)
    #     blog = Blog.objects.get(id=blog_id)
    #     data = {'id': blog.id, 'title': blog.title, 'content': blog.content}    
    #     return JsonResponse({'data': data}, status=200)
    # except Exception as e:
    #     return JsonResponse({'error': str(e)}, status=500)
    
    
@api_view(['POST'])
def signup(request):
    serialiser = UserSerializer(data=request.data)
    if serialiser.is_valid():
        serialiser.save()
        user = User.objects.get(username= request.data['username'])
        # hash the password
        user.set_password(request.data['password'])
        user.save()
        # token = Token.objects.create(user=user)
        return Response({"message": "User created successfully", }, status=201)
    return Response({"error": serialiser.errors}, status=400)

@api_view(['POST'])
def login(request):
    # check if user exist
    user = get_object_or_404(User, username=request.data.get('username'))
    # check the user password
    # if  user does not exist or passwod is incorrect send an error message
    if not user.check_password(request.data.get('password')):
        return Response({"error": "Invalid username or password"}, status=401)
    # if user exist and password is correct create a token for the user and return user data
    else:
        # token = Token.objects.get_or_create(user=user)[0]
        # return Response({"user": UserSerializer(user).data, "token": token.key }, status=200)
        token = get_token_for_user(user)
        user_data = model_to_dict(user)
        delete_items = ['password', 'date_joined', "user_permissions"]
        for item in delete_items:
            del user_data[item]
        # del user['user_permissions']
        # del user['password']
        # del user['date_joined']
        return Response({"token": token, "user": user_data}, status=200)
    # 
    # else create a token fr the user and return user data

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def blogs(request):
    try:
        if request.method == 'GET':
            blogs = Blog.objects.all()
            
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            print(request)
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user) # this will attache the blog to the current authenticated user
                return Response({"message": "blog post created successfully"}, status=201)
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(["GET"])
def get_blog_post(request):
    id = request.GET.get('id')
    try:
        if id == None:
            return Response({"error": "Blog id is required"}, status=400)
        blog = Blog.objects.get(id=id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    except:
        return Response({"error": "Blog not found"}, status=404)