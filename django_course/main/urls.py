from django.urls import path
from . import views


app_name = "main"  #Имя через которое можно обращаться к юрлам
urlpatterns = [
    path("", views.title, name="title"),
    path("news/", views.index, name="news"),
    path("contact/",views.contact,name="contact"),
    path("detail/<int:pk>/", views.detail, name="main_detail"),  #int:pk это id. Будет выводить юрл по типо блог/1, блог/2...
    path("create/", views.create_main, name="create_main"),
    path("update/<int:pk>/", views.update_main, name="update_main"),
    path("delete/<int:pk>/",views.delete_blog,name="delete_main")
]
