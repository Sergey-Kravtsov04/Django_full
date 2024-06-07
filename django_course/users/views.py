from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AuthUserForm, userRegistraitionForm, UserUpdateForm
from django.contrib.auth import login
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
class Login(LoginView):
    fields =["username","passwors"]
    template_name = 'users/login.html'
    form_class = AuthUserForm
class Logout(LogoutView):
    template_name = "users/logout.html"

def Register(request):
    regform = userRegistraitionForm(request.POST)
    if request.method == "POST":
        if regform.is_valid():
            reg_f=regform.save(commit=False)
            reg_f.is_active = True
            reg_f.is_staff = False
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()

            reg_f.backend ='django.contrib.auth.backends.ModelBackend'
            login(request, reg_f)
            return redirect('main:title')
    else:
        regform =userRegistraitionForm()
    return render(request,'users/registration.html',{"regform":regform})
@login_required
def Profile(request):
    user_blogs = request.user.blogpost_set.all()  #Здесь название модели нужно в lowercase прописать(я на это минут 30 потратил,прикол блин)
    return render(request, 'users/profile.html',{"user_blogs": user_blogs})
@login_required
def profile_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance= request.user)
    return render(request,'users/profile_update.html',{"form":form})