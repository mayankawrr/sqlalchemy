from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///mydatabase.db', echo=True)
#engine is an object which connects to DB, echo = for debugging, sqlite:/// = connection string

conn=engine.connect()
conn.execute(text("CREATE TABLE IF NOT EXISTS people (name str, age int)"))
#we wrap SQL queries into a function called text so it can be safely executed by the engine, we can do it without using SQL queries also using metadata and functions and in ORM we use objects, classes
conn.commit()

#When we work with SQLALCHEMY CORE, we work with Connections, in ORM we work with Sessions
from sqlalchemy.orm import Session 
#sqlalchemy and sqlalchemy.orm are modules and submodules, sqlalchemy is the base package
session= Session (engine)
#created a new session object using the database engine, session object connects ORM features to our database allowing us to work with python oop instead of SQL
#engine helps us know, which database to interact with, as there can be diff engines for diff DBs by creating separate engine objects
session.execute(text('INSERT INTO PEOPLE (name, age) VALUES ("Mike2", 30);'))
session.commit()


'''
This is not the best way to run SQLALCHEMY, we are running sql code directly
Use
SQL CORE- use functions (use metadata to create everything in db easily)
ORM- wrap python classes to db tables
'''