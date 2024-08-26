from .models import CustomUser
from . import serializers
from rest_framework import viewsets,filters,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.http import Http404
class UserForUser(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        customuser_id = request.query_params.get("user_id")
        if customuser_id:
            return queryset.filter(id=customuser_id)
        return queryset  
class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [UserForUser]
class CustomDetail(APIView):
    def get_object(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = serializers.UserSerializer(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://workio-ypph.onrender.comaccount/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        CustomUser.objects.create(user=user, bio='')
        return redirect('http://127.0.0.1:5500/logIn.html')
    else:
        return redirect('http://127.0.0.1:5500/singIn.html')
    

class UserLoginApiView(APIView):
    def post(self, request):
        serializer =  serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
              
                user = User.objects.get(username=username)
                if not user.is_active:
                    return Response({'error': "Email not confirmed"}, status=400)

                # Authenticate the user
                user = authenticate(username=username, password=password)
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    login(request, user)
                    try:
                        customuser = CustomUser.objects.get(user=user)
                        customuser_id = customuser.id
                    except CustomUser.DoesNotExist:
                        customuser_id = None
                    return Response({'token': token.key, 'user_id': user.id, 'customuser_id': customuser_id })
                else:

                    return Response({'error': "Password does not match"}, status=400)

            except User.DoesNotExist:

                return Response({'error': "Username does not exist"}, status=400)
        
        # Invalid data (e.g., missing fields)
        return Response(serializer.errors, status=400)
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')

