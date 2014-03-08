from django.core.context_processors import csrf
from django.middleware.csrf import rotate_token
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core import serializers
from auth.models import AuthUser, UserMeta, UserSession
from datetime import datetime as dt 
from datetime import timedelta
from utils import sanitize_passwd_meta

# This depends on bcrypt. Install it with pip
import bcrypt, json, random, string

'''
Note: input doesn't need to be sanitized on this level, because Django's 
model implementation provides input sanitization as part of its core 
functionality
'''

# A request to /auth/csrf should reset the csrf token, and then return that 
# token. Ideally, this should all be happening over SSL
def get_csrf(request):
    if request.method != 'GET':
        return HttpResponse(status=405)

    rotate_token(request)
    c = {}
    c.update(csrf(request))
    # Set cookie
    response = HttpResponse(c['csrf_token'])
    response.set_cookie('csrftoken', unicode(c['csrf_token']))
    return response


# List users
def list_users(request):
    if request.method != 'GET':
        return HttpResponse(status=405)

    data = [
        {
            'pk': user['pk'],
            'name': user['username']
        } for user in AuthUser.objects.all().values('pk', 'username')
    ]
    return HttpResponse(json.dumps(data))


# Create a user
def create_user(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    rqdata = json.loads(request.read())

    atmpt_username = rqdata['username']
    atmpt_password = rqdata['password']

    try:
        existing = AuthUser.objects.get(username=atmpt_username)
        return HttpResponse(status=403)
    except ObjectDoesNotExist:
        # Run password through bcrypt
        password = bytes(rqdata['password'])
        salt = bcrypt.gensalt(12)
        pw_digest = bcrypt.hashpw(password, salt)

        # Create a user
        user = AuthUser.objects.create(
            username=rqdata['username'],
            passwd_digest=pw_digest
        )
        retdata = {
            'user': {
                'pk'   : user.pk,
                'name' : user.username
            }
        }
        return HttpResponse(json.dumps(retdata))


# Authenticate a user
def auth_user(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    rqdata = json.loads(request.read())

    atmpt_username = rqdata['username']
    atmpt_password = rqdata['password']

    # Get login data
    try:
        user = AuthUser.objects.get(username=atmpt_username)
    except ObjectDoesNotExist:
        # Couldn't find user
        return HttpResponse(status=404)

    # Check for existing session
    try:
        session = UserSession.objects.get(ticket_holder=user)

        # Check session expiry -- sessions should expire after a couple hours
        # after the user stops contacting the server
        now = dt.now()
        if session.expiry <= now:
            # Delete this session, and raise exception to
            # get out of this try clause
            session.delete()
            raise ObjectDoesNotExist
        return HttpResponse(status=403)

    except ObjectDoesNotExist:
        # Hash the given password and test it against our user's
        passdg = user.passwd_digest
        if bcrypt.hashpw(atmpt_password, passdg) != passdg:
            # This is where we can log the origin of the request, and screen 
            # it out if it's trying to login too frequently
            return HttpResponse(status=403)

        # Last line of defense -- check the user's metedata fingerprint
        fingerprint = sanitize_passwd_meta(rqdata['metadata'])

        if fingerprint is None:
            # User passed in something nasty
            return HttpResponse(status=403)

        # Analyze the fingerprint
        

        # Create session
        token_found = False

        # Note: it's EXTREMELY unlikely that there will be conflicts in token
        # values, but being paranoid pays dividends
        try:
            # try random tokens until we find one that isn't taken
            # then, break out of the try clause
            while True:
                stoken = ''.join(
                    random.choice(string.ascii_uppercase+string.digits)
                    for _ in xrange(32)
                )
                match = UserSession.objects.get(session_token=stoken)
        except ObjectDoesNotExist:
            # Create the session and return the key
            # Session should expire in six hours
            session = UserSession.objects.create(
                ticket_holder=user,
                session_token=stoken,
                expiry=dt.now() + timedelta(hours=3)
            )

            # There should be more to it than this, but there's nothing the
            # user's going to be doing here -- so just keep it in mind that
            # you should be updating the expiration time as the user is 
            # active. This thing should only expire when the user forgets to 
            # log out
            session.save()

            return HttpResponse(json.dumps({
                'stoken': stoken
            }))

def logout(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
        
    rqdata = json.loads(request.read())

    # validate the user's session token before we do anything else
    atmpt_stoken = rqdata['stoken']
    try:
        session = UserSession.objects.get(session_token=atmpt_stoken)

        # Kill the session and rotate the csrf key
        session.delete()
        rotate_token(request)
        return HttpResponse(status=204)
    except ObjectDoesNotExist:
        # Session failure
        return HttpResponse(status=403)