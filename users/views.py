from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm 




# Create your views here.
def register(request):
      form = UserCreationForm(request.POST or None)
        
      if request.method == "POST":
          if form.is_valid():
            form.save()
          return redirect("/login")
      context = {
        "form" : form
      }
      return render(request, "user/register.html", context)
          



def login(request):
      if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
          user = form.get_user()
          auth_login(request, user)
          return redirect("dashboard")

      else:
        form = AuthenticationForm()

      context = {
       "form" : form,
      }
      return render (request,"user/login.html", context)


def logout(request):
    if request.method == "POST":
      auth_logout(request)
      return redirect('/login/')
    return render(request, "user/logout.hmtl")
