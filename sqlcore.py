from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float
from random import randint, choice
import os

engine = create_engine('sqlite:///mydatabase.db', echo=True)

meta = MetaData() #passed as a parameter into Table function and stores all the data of table to create table later on

people= Table(
    "people", #name of table
    meta, #metadata object, keeps track of all info
    Column('id', Integer, primary_key=True), 
    Column('name', String, nullable=False),
    Column('age', Integer)
)

meta.create_all(engine) #this actually creates the table as engine manages connections internally and we do not need to explicitly create connection objects to create tables either


conn=engine.connect()
select_statement = people.select().where(people.c.name == 'Mike')
result = conn.execute(select_statement)
conn.commit() #this makes sure that the change i applied to the db out the the program


print(result.fetchall()) #fetchall writes everything in one line instead of iterating, otherwise result = a list of all rows from the query results which is run by iteration


#Let's model relationships now
things = Table (
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('value', Float),
    Column('owner', Integer, ForeignKey('people.id'))
    
)
#one to many relationship bcoz of foreign key being from people table, for many to many we need another association table

meta.create_all(engine) #takes schema and table relationships automatically internally and can be overwritten, single statement is enough to build multiple tables in a single transaction

#inserting random values into peoples table
names = ['Mike', 'Anna', 'John', 'Sara', 'Tom']
ages = [randint(18, 60) for _ in range(len(names))]

for idx, (name, age) in enumerate(zip(names, ages), start=1):
    insert_stmt = people.insert().values(id=idx, name=name, age=age)
    conn.execute(insert_stmt)

conn.commit() 

#now we fill up things table
descriptions = ['Laptop', 'Phone', 'Book', 'Pen', 'Bag']
for _ in range(5):
    desc = choice(descriptions)
    value = round(randint(10, 1000) + randint(0, 99)/100, 2)
    owner_id = randint(1, len(names))
    insert_stmt = things.insert().values(description=desc, value=value, owner=owner_id)
    conn.execute(insert_stmt)
    
conn.commit()

#inner join, preserves only the rows which have a relationship and doesn't show empty relationships in the rows
join_statement = people.join(things, people.c.id == things.c.owner)
select_statement = people.select().with_only_columns(people.c.name, things.c.description).select_from(join_statement)

result = conn.execute(select_statement)
#result has a cursor, retrieves result after using query and then exhausts itself after the cursor which acts as a pointer
#result = iterator and not a list so it is exhauster after every iteration and we need to re run query, this is useful for memory efficiency
print(result.fetchall())

result = conn.execute(select_statement)
for row in result.fetchall():
    print(row)


result = conn.execute(select_statement)
for row in result:
    print(row)
    
    
#outer join
join_statement = people.outerjoin(things, people.c.id == things.c.owner)
select_statement = people.select().with_only_columns(people.c.name, things.c.description).select_from(join_statement)

result = conn.execute(select_statement)
for row in result:
    print(row)
   

db_path = 'mydatabase.db'
if os.path.exists(db_path):
    os.remove(db_path)