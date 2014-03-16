from django.shortcuts import render
from django.middleware.csrf import rotate_token
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from Crypto.Cipher import AES

from auth.models import UserMeta
from auth.utils import aes_secret_padding, validate_user_metadata

import struct, zlib, json

# Reset the CSRF token
def reset_csrf(request):
	rotate_token(request)
	return HttpResponse('CSRF Token Reset', status=200)

def user_create(request):
	# Search for taken username
	try:
		extant = User.objects.get(username=request.POST['username'])
		return HttpResponse(status=403)
	except ObjectDoesNotExist:
		pass

	# Django's model class sanitizes input automatically
	# I'd double check it, but that's not the focus of this project
	# -- it's used in production environments, so I'm not too worried
	username=request.POST['username']
	password=request.POST['password']

	# Load data into correct format for the first time
	md_list = json.loads(request.POST['metadata'])
	metadata = json.dumps({
		'keystrokes': md_list
		'variance'  : [0 for _ in md_list]
	})

	# Create the user 
	user = User.objects.create(
		username=username, 
		password=password
	)

	# IMPORTANT -- Encrypt the metadata with AES using 
	# the password as a key so that the attacker doesn't get the key length
	md_aes = AES.new(aes_secret_padding(password), AES.MODE_CFB)
	md_cipher = md_aes.encrypt(metadata)
	user_md = UserMeta.objects.create(
		owner=user,
		data=md_cipher
	)
	user.save()
	user_md.save()
	return HttpResponse(status=200)

def user_login(request):
	username=request.POST['username']
	password=request.POST['password']
	metadata=request.POST['metadata']

	# authenticate the user
	user = authenticate(username=username, password=password)

	if user is not None and user.is_active:
		# Authentication worked -- now for the metadata
		try:
			metadata = UserMeta.objects.get(owner=user)
		except ObjectDoesNotExist:
			# This shouldn't happen. fail
			return HttpResponse(status=500)

		md_aes = AES.new(aes_secret_padding(password), AES.MODE_CFB)
		md_ptext = md_aes.decrypt(metadata.data)

		# perform cyclic redundancy check
		# crc should be the first 4 chars of plaintext. slice it off...
		crc, md_ptext = (md_ptext[-4:], md_ptext[:-4])

		if not crc == struct.pack('i', zlib.crc32(md_ptext)):
			# CRC failed. Metadata is bonked
			# TODO: recover from this error without giving the attacker a way
			# to break in.
			return HttpResponse(status=500)

		# Now we can use the metadata to validate the user
		md_new = json.loads(metadata)
		md_extant = json.loads(md_plaintext)
		md_valid = validate_user_metadata(md_new, md_extant)

		if md_valid is not None:
			# Update metadata and reencrypt it
			md_aes = AES.new(aes_secret_padding(password), AES.MODE_CFB)
			metadata.data = md_aes.encrypt(json.dumps({
				'keystrokes': md_valid['ks'],
				'variance'  : md_valid['variance']
			}))
			# persist this data to the DB
			metadata.save()

			# login is seperate from authentication -- it's almost as if the 
			# creators of Django know what they're doing...
			login(request, user)
			return HttpResponse(status=200)
	# VERBOTEN
	return HttpResponse(status=403)

def user_logout(request):
	logout(request)
	return HttpResponse(status=200)