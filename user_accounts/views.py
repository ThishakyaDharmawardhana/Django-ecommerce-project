from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm





# Create your views here.
def user_info(request):
    return render(request, 'user_accounts/userinfo.html', {})

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You have been Logged in..."))
            return redirect ('storehome')
        else:
            messages.success(request, ("Username or Password incorrect...Please try again"))
            return redirect ('login_user')
    else:
        return render( request, 'user_accounts/login.html', {'title': 'Sign in'})
    

    
def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out...Thank you!'))
    return redirect('storehome')

def register_user(request):
    form = SignUpForm()
    if not request.method == "POST":
        return render(request,'user_accounts/register.html', {'form': form, 'title': 'Join with us'})


    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data["username"]
            password= form.cleaned_data["password1"]
            #log in user
            user =authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have registered! Welcome !!!"))
            return redirect('welcome')
        else:
            messages.error(request, ("Threre is a problem registering, try agaian"))
            return redirect('register_user')




