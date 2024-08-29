from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import *
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required

from apps.accounts.validators import * 
from apps.parametrization.utils import *

#------------------- LOGIN

def redirect_view(request):
    response = redirect('accounts/login/')
    return response

def login(request):
    if request.method == 'POST':
        validator = FormLoginValidator(request.POST)
        if validator.is_valid():
            auth.login(request, validator.access)  
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('users:profile_list'))
            else:
                return HttpResponseRedirect(reverse('users:profile_list'))
                #return HttpResponseRedirect(reverse('normal_user_view'))
        else:
            return render(request, 'accounts/login.html', {'error': validator.getMessage() })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:profile_list'))
        else:
            return render(request, 'accounts/login.html')


#------------------- LOGOUT

@login_required(login_url='accounts:login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

