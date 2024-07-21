import pdb
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.generic import *
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import CustomUser
from apps.properties.models import Membres, MembresMediasSociaux
from apps.users.form import ProfileEditForm, UserEditForm, CustomUserCreationForm
from apps.users.models import Profile
from apps.vars import *
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password

from apps.web.models import Formulaire_contact

def updateProfile(request):
    existing_orders = Profile.objects.exclude(order__isnull=True).values_list('order', flat=True)
    if request.user and request.user.profile.order:
        existing_orders = list(existing_orders)
        existing_orders.remove(request.user.profile.order)

    available_orders = [i for i in range(1, 11) if i not in existing_orders]
    
    user_membre = request.user.profile.membre
    available_membres = Membres.objects.filter(profile__isnull=True)
    membres = available_membres | Membres.objects.filter(pk=user_membre.pk) if user_membre else available_membres

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)  
            if 'image' in request.FILES:  
                profile.image = request.FILES['image']  
            profile.save()  
            messages.success(request, 'Perfil actualizado', 'succesful')
            return redirect('users:profile_list')  
        else:
            messages.error(request, 'Error al actualizar el perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'users/profile.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'cantidad_usuarios':available_orders,
        'membres': membres,
    })

def updateProfileUsers(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    existing_orders = Profile.objects.exclude(order__isnull=True).values_list('order', flat=True)
    if user and user.profile.order:
        existing_orders = list(existing_orders)
        existing_orders.remove(user.profile.order)

    available_orders = [i for i in range(1, 11) if i not in existing_orders]
    
    user_membre = user.profile.membre
    available_membres = Membres.objects.filter(profile__isnull=True)
    membres = available_membres | Membres.objects.filter(pk=user_membre.pk) if user_membre else available_membres
    if request.method == 'POST':
        user_form = UserEditForm(instance=user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)  
            if 'image' in request.FILES:  
                profile.image = request.FILES['image'] 
            if 'image_over' in request.FILES:  
                profile.image_over = request.FILES['image_over'] 
            profile.save()  
            messages.success(request, 'Perfil actualizado', 'succesful')
            return redirect('users:profile_list')  
        else:
            messages.error(request, 'Error al actualizar el perfil')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=user.profile)
    return render(request, 'users/profile.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'cantidad_usuarios':available_orders,
        'membres': membres,
    })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            auth_logout(request) 
            messages.success(request, '¡Su contraseña fue modificada con éxito!')
            return redirect('users:password_change_done')
        else:
            messages.error(request, 'Por favor corriga los errores listados')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {
        'form': form
    })

def password_change_done(request):
    return render(request, 'users/password_change_done.html')

def change_password_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Contraseña modificada con éxito!')
            return redirect('users:profile_list')
        else:
            messages.error(request, 'Por favor corriga los errores listados')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change_user.html', {
        'form': form,
        'user':user
    })

def profile_list(request):
    usuarios = CustomUser.objects.all().order_by('first_name')
    return render(request, 'users/list_users.html',{'usuarios':usuarios})

def create_user(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileEditForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.email  
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.order = CustomUser.objects.count()
            profile.save()
            messages.success(request, '¡Usuario creado Correctamente!')
            return redirect('users:profile_list')
        else:
            messages.error(request, 'Por favor corriga los errores listados')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileEditForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

#
def user_verification():
    try:
        membres = Membres.objects.all()
        order = 0
        for membre in membres:
            if not CustomUser.objects.filter(email=membre.courriel).exists():
                user = CustomUser.objects.create_user(
                    email=membre.courriel,
                    username=membre.courriel,
                    first_name = membre.prenom,
                    last_name = membre.nom,
                    password=make_password("Operaciones123")
                )
            else:
                user = CustomUser.objects.get(email=membre.courriel)
            order += 1
            if not Profile.objects.filter(user=user).exists():
                profile = Profile.objects.create(
                    user=user,
                    image='static/media/default.png',
                    membre = membre,
                    order= order,
                    type_user="operador",
                )
            else:
                profile = Profile.objects.get(user=user)

    except Exception as e:
        mensaje = f'Error processing files: {str(e)}'
        return mensaje

    return "Usuarios y perfiles verificados y/o creados correctamente"

def list_messages(request):
    messages_list = Formulaire_contact.objects.all()
    return render(request, 'users/list_messages.html',{'messages_list':messages_list})

def detail_message(request, id):
    message_detail = get_object_or_404(Formulaire_contact, id=id)
    if request.method == 'POST':
        message = get_object_or_404(Formulaire_contact, id=id)
        message.read = True
        message.save()
        return redirect('users:list_messages')

    return render(request, 'users/detail_message.html',{'message_detail':message_detail})