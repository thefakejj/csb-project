import sqlite3
import os

db_command = \
"""
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Notes;
CREATE TABLE Notes (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id varchar(200), 
	note varchar(200)
);

COMMIT;
"""
db_path = 'mysite/db.sqlite3'


if not os.path.exists(db_path):
	print('Follow steps 2 and 3 in the guide before running this command')
else:
	conn = sqlite3.connect(db_path)
	conn.cursor().executescript(db_command)
	conn.commit()
