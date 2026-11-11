import sqlite3
import os

# ei toimi INSERT INTO auth_user (password, username, is_superuser, is_staff, is_active) VALUES ('heippa', 'jorma', 0, 0, 1);

db_command = \
"""
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Notes;
CREATE TABLE Notes (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id varchar(200), 
	note varchar(200)
);

INSERT INTO Notes (user_id, note) VALUES('bob','This is an important and secret note for me only');
INSERT INTO Notes (user_id, note) VALUES('alice','I have a note and nobody else will find it');


COMMIT;
"""
db_path = 'db.sqlite3'

if not os.path.exists(db_path):
	print('you have to create database with django. [insert instructions]')
else:
	conn = sqlite3.connect(db_path)
	conn.cursor().executescript(db_command)
	conn.commit()
