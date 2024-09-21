from django.urls import path
from .views import SignupView, CustomTokenObtainPairView 

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair')
]
