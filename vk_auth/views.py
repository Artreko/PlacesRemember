from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.conf import settings
import requests
from .models import VkUser


def logout_view(request):
    logout(request)
    return redirect('index')


def auth_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    params = {'client_id': settings.VK_AUTH_CLIENT_ID,
              'display': 'page',
              'redirect_uri': settings.VK_AUTH_CODE_REDIRECT_URI,
              'response_type': 'code',
              'v': settings.VK_AUTH_VERSION}
    redirect_url = f'https://oauth.vk.com/authorize?' + \
        '&'.join([f'{key}={params[key]}' for key in params])
    return redirect(redirect_url)


def auth_code_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    code = request.GET.get('code')
    params = {'client_id': settings.VK_AUTH_CLIENT_ID,
              'redirect_uri': settings.VK_AUTH_CODE_REDIRECT_URI,
              'client_secret': settings.VK_AUTH_SECRET_KEY,
              'code': code}
    access_request = f'https://oauth.vk.com/access_token?' + \
        '&'.join([f'{key}={params[key]}' for key in params])
    access_response = requests.get(access_request).json()
    access_token = access_response.get('access_token')
    access_error = access_response.get('error')
    if access_error:
        HttpResponse(f'Ошибка: {access_error} \
                     Описание: {access_response.get("error_description")}')
    user_info = requests.post(
        'https://api.vk.com/method/account.getProfileInfo',
        data={
            'access_token': access_token,
            'v': settings.VK_AUTH_VERSION
        }
    ).json()
    user_info = user_info.get('response')
    user_id = user_info.get('id')
    profile_image = user_info.get('photo_200')
    first_name = user_info.get('first_name')
    last_name = user_info.get('last_name')
    user, created = VkUser.objects.get_or_create(
        vk_id=user_id,
        defaults={
            'profile_image': profile_image,
            'first_name': first_name,
            'last_name': last_name
        })
    if not created:
        if user.first_name != first_name:
            user.first_name = first_name
        if user.last_name != last_name:
            user.last_name = last_name
        if user.profile_image != profile_image:
            user.profile_image = profile_image
        user.save()
    login(request, user)
    return redirect('index')
