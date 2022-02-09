from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt


from .models import User
from .serializers import UserSerializer
from .utils import Util
# Create your views here.


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = serializer.data
            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink + \
                "?token="+str(refresh.access_token)
                
            body = f"""
                Hi {user.username}
                Click the below link to verify your email.
                {absurl}
            """

            email_data = {
                'to': user.email,
                'subject': 'Verify your email address',
                'body': body
            }

            Util.send_email(self, email_data)

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class EmailVerifyView(generics.GenericAPIView):

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])

            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response("Successful Verify Email", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as error:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as error:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class LogoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.data["refresh"]
            token = RefreshToken(token)
            token.blacklist()

            return Response("Successful Logout", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
