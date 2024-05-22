from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login, logout
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

class RegistrationViewSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html',{'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            return Response("Check Your Email to Verify Account")
        return Response(serializer.errors)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class LoginViewSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username= username, password=password)
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request,user )
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        
        return Response(serializer.errors)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return JsonResponse({"message": "Successfully logged out.", "status": 200})
    except Token.DoesNotExist:
        return JsonResponse({"error": "Token not found.", "status": 400})


class UserProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
