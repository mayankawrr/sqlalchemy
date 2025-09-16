from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///mydatabaseorm.db', echo=True)

base=declarative_base()

class Person(base):
    __tablename__='people'
    id = Column(Integer, primary_key=True)
    name= Column(String, nullable=False)
    age= Column(Integer)
    
    things = relationship('Thing', back_populates='person')
    

class Thing(base):
    __tablename__='things'
    id= Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    owner = Column(Integer, ForeignKey('people.id'))
    
    person=relationship('Person', back_populates='things')
    
    
base.metadata.create_all(engine)

Session= sessionmaker(bind=engine)
session=Session()

new_person= Person(name='Charlie', age=70)
session.add(new_person)
session.flush() #temporarily add the person but doesnt write that into database, we can get the id for the next Things table command

new_thing=Thing(description='Camera', value=500, owner=new_person.id)
session.add(new_thing)
session.commit()

print(list(new_person.things))  # This will print a list of Thing objects related to new_person
print([thing.description for thing in new_person.things])  # Prints descriptions of things owned by new_person

print(new_thing.person)  # This will print the Person object related to new_thing
print([new_thing.person.name])  # Prints the name of the person who owns new_thing

#Basically we can directly use python objects to print relationship values from the table instead of using any joins and SQL or mannual databse stuff. Just need to define objects as classes beforehand to use in relationships later



#Querying, Updating, Inserting and Deleting is pretty similar compare to previous time, just need to use different function names this time


result=session.query(Person.name, Person.age).all() #all() is an alternative to fetchall
result2=session.query(Person).all() #python objects we get which are not readable
#print([p.name for p in result])
print(result2)

#Alternative for where here is filter

result3=session.query(Person).filter(Person.age>40).all()
#print([p.name for p in result3])





 