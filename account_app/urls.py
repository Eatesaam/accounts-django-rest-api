from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import UserRegisterView, UserListView, UserDetailView, LogoutView, EmailVerifyView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email_verify/', EmailVerifyView.as_view(), name='email-verify'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),


    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
