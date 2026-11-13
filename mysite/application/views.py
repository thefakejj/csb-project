from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import File
import sqlite3
import os

from django.http import HttpResponse

db_path = 'mysite/db.sqlite3'

@login_required
def deleteView(request):
	f = File.objects.get(pk=request.POST.get('id'))
	print(f)
	print(f.owner)
	print(f.data)
	print(request.POST.get('id'))
	if f.owner != request.user:
		return redirect('/')

	f.delete()
	return redirect('/')
	

@login_required
def downloadView(request, fileid):
	f = File.objects.get(pk=fileid)
	# the commented code prevents unauthorized access (to uploaded files)
	# if f.owner != request.user:
	# 	return redirect('/')

	filename = f.data.name.split('/')[-1]
	response = HttpResponse(f.data, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=%s' % filename

	return response


@login_required
def addView(request):
	data = request.FILES.get('file')
	f = File(owner=request.user, data=data)
	f.save()
	return redirect('/')

@login_required
def homePageView(request):
	notes = getNotes(request.user.username)
	uploads = getUploads(request)
	return render(request, 'index.html', {'notes': notes, 'uploads': uploads})

def getUploads(request):
	files = File.objects.filter(owner=request.user)
	uploads = [{'id': f.id, 'name': f.data.name.split('/')[-1]} for f in files]
	return uploads

def getNotes(user_id):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	query = 'SELECT note FROM Notes where user_id = :user LIMIT 10;'
	args = (user_id,)
	result = cursor.execute(query, args)
	notes = []
	for row in result.fetchall():
		notes.append(row[0])
	return notes

def searchNoteView(request):
	if request.method == 'POST':
		search = request.POST.get('search', '').strip()
		conn = sqlite3.connect(db_path)
		cursor = conn.cursor()
		user_id = request.user.username
		"""
		SQL injection can be done with these queries
		' OR 1=1; --
		DOESNOTEXIST' UNION SELECT note FROM Notes WHERE user_id = 'admin'; --
		DOESNOTEXIST' UNION SELECT password FROM auth_user WHERE username = 'admin'; --
		"""
		
		query = f"SELECT note FROM Notes WHERE note LIKE '%{search}%' AND user_id = '{user_id}';"
		result = cursor.execute(query)

		# using these lines, the sql injection cant be performed
		# query = "SELECT note FROM Notes WHERE note LIKE :search AND user_id = :user_id;"
		# final_search = f"%{search}%"
		# args = (final_search, user_id)
		# result = cursor.execute(query, args)
		notes = []
		for row in result.fetchall():
			notes.append(row[0])
		return render(request, 'index.html', {'notes': notes, 'uploads': getUploads(request)})

@login_required
def addNoteView(request):

	if request.method == 'POST':
		note = request.POST.get('note', '').strip()
		conn = sqlite3.connect(db_path)
		cursor = conn.cursor()
		user_id = request.user.username

		query = "INSERT INTO Notes (user_id, note) VALUES (:user_id, :note);"
		args = (user_id, note)
		cursor.execute(query, args)

		conn.commit()
		
	return redirect('/')
	# I tried sql injection for this function
	# but it was hard to get anything out of it since execute only ran one command at a time.

	# SQL injection didnt work here
	# note = "moi'); INSERT INTO Notes (user_id, note) VALUES ('bob', 'uus note btw'); --" #trying to create a statement that does something with this injection is tough	
	# query = f"INSERT INTO Notes (user_id, note) VALUES ('bob', '{note}');"
	# query = f"INSERT INTO Notes (user_id, note) VALUES ('{user_id}', '{note}');"
	# print(query)
	# cursor.execute(query) # comment this line too when fixing sql injection
