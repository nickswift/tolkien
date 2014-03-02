from django.core.context_processors import csrf
from django.http import HttpResponse
from django.core import serializers
from auth.models import TUser, TUserMeta

# This depends on bcrypt. Install it with pip
import bcrypt, json

# Get CSRF Token
def get_csrf(request):
    c = {}
    c.update(csrf(request))
    # Set cookie
    response = HttpResponse(c['csrf_token'])
    response.set_cookie('csrftoken', unicode(c['csrf_token']))
    return response


# List users
def list_users(request):
    users = TUser.objects.all().values('pk', 'username')

    data = [
        {
            'pk': user['pk'],
            'name': user['username']
        } for user in users
    ]

    return HttpResponse(json.dumps(data))


# Create a user
def create_user(request):
    # only allow POST

    # if request.method != 'POST':
    #    return HttpResponse(405, '')

    rqdata = json.loads(request.read())

    # Ensure the username isn't taken
    if len(TUser.objects.filter(username=rqdata['username'])) > 0:
        return HttpResponse(status=403)

    # Run password through bcrypt
    password = bytes(rqdata['password'])
    salt = bcrypt.gensalt(12)
    pw_digest = bcrypt.hashpw(password, salt)

    # Create a metadata fingerprint
    user_meta = TUserMeta.objects.create()

    # Create a user
    user = TUser.objects.create(
        username=rqdata['username'],
        passwd_digest=pw_digest,
        metadata=user_meta
    )

    retdata = {
        'user': serializers.serialize('json', user),
        'meta': serializers.serialize('json', user_meta)
    }

    return HttpResponse(json.dumps(retdata))


# Authenticate a user
def auth_user(request):
    return HttpResponse('authenticate user')