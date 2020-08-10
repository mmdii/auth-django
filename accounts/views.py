from django.shortcuts import render, redirect

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserRegisterForm

from .admin import UserResource

dataset = UserResource().export()
print(dataset.csv)

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


from django.shortcuts import render
from django.http import HttpResponse
# from .resources import PersonResource
from tablib import Dataset
# from .models import Person
from .admin import UserResource


from django.contrib.auth import (
    authenticate,
    get_user_model

)

user = get_user_model()

def export(request):
    user_resource = UserResource()
    dataset = user_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        user_resource = UserResource()
        dataset = Dataset()
        new_users = request.FILES['myfile']

        imported_data = dataset.load(new_users.read(),format='xlsx')
        #print(imported_data)
        for data in imported_data:
        	print(data[1])
        	value = user(
        		data[0],
        		data[1],
        		 data[2],
        		 data[3],
                 data[4],
                 data[5]
        		)
        	value.save()       
        
    return render(request, 'input.html')