from django.urls import path
from .views import UserProfilView


urlpatterns = [
    path('users/', UserProfilView.as_view()),
    #path('<int:user_id>/', UserProfilView.as_view()),
]

