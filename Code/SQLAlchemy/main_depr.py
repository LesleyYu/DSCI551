# https://www.youtube.com/watch?v=AKQ3XEDI9Mw

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
  # orm: object relational mapping
  # declarative_base is the base class that we're going to extend so that we can call it using sessionmaker
  # sessionmaker will start a session then we can start the session and we can do stuff in the database


Base = declarative_base()
# class Base(DeclarativeBase):
#   pass

class Person(Base):
  __tablename__ = "people"    # this will be the table name inside of the dabatase

  ssn = Column("ssn", Integer, primary_key=True)
  firstname = Column("firstname", String)
  lastname = Column("lastname", String)
  gender = Column("gender", CHAR)
  age = Column("age", Integer)

  def __init__(self, ssn, firstname, lastname, gender, age):
    self.ssn = ssn
    self.firstname = firstname
    self.lastname = lastname
    self.gender = gender
    self.age = age
  # # The above lines are deprecated methods.
  # # in the doc, there's also another way to write it using 
  # # sqlalchemy.orm.Mapped and mapped_column
    
  # for debugging:
  def __repr__(self):
    return f"({self.ssn}) {self.firstname} {self.lastname} {self.gender} {self.age}"
  
class Thing(Base):
  __tablename__ = "things"

  tid = Column("tid", Integer, primary_key=True)
  description = Column("description", String)
  owner = Column(Integer, ForeignKey("people.ssn"))

  def __init__(self, tid, description, owner):
    self.tid = tid
    self.description = description
    self.owner = owner

  def __repr__(self):
    return f"({self.tid}) {self.description} owned by {self.owner}"

engine = create_engine("sqlite:///mydb.db", echo=True)   # this create a sqlite database. This create a file and work with it.
Base.metadata.create_all(bind=engine)   # connect to the engine and create all the tables linked to Base

Session = sessionmaker(bind=engine)     # sessionmaker. This is a class
session = Session()                     # an instance of Session

person = Person(12312, "Mike", "Smith", 'm', 35)
session.add(person)
session.commit()

p1 = Person(52662, "Anna", "Blue", 'f', 40)
p2 = Person(38672, "Bob", "Blue", 'm', 35)
p3 = Person(53967, "Angela", "SmiColdth", 'f', 22)
session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

t1 = Thing(1, "Car", p1.ssn)
t2 = Thing(2, "Laptop", p1.ssn)
t3 = Thing(3, "PS5", p2.ssn)
t4 = Thing(4, "Tool", p3.ssn)
t5 = Thing(5, "Book", p3.ssn)
session.add(t1)
session.add(t2)
session.add(t3)
session.add(t4)
session.add(t5)
session.commit()


# # query
# results1 = session.query(Person).all()
# print(results1)

# results2 = session.query(Person).filter(Person.lastname == 'Blue')
# for r in results2:
#   print(r)

# results3 = session.query(Person).filter(Person.firstname.like("%An%"))
# for r in results3:
#   print(r)

# results4 = session.query(Person).filter(Person.firstname.in_(["Anna", "Mike"]))
# for r in results4:
#   print(r)

res1 = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Anna")
for r in res1:
  print(r)