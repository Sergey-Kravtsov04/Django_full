from django.urls import path
from .import views

app_name="users"
urlpatterns=[
    path("login/",  views.Login.as_view() , name="login"),
    path("logout/",views.Logout.as_view(), name="logout"),
    path("register/",views.Register, name="register"),
    path("profile/", views.Profile, name="profile"),
    path("profile_update/", views.profile_update, name="profile_update")
]