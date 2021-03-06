from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('postgresql://postgres:password1234.@catalogapp.cjqlyhntilau.us-west-2.rds.amazonaws.com:5432/catalogapp')
#engine = create_engine('sqlite:///catalogApp.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Drop all tables if exists and recreate them
Item.__table__.drop(engine, checkfirst=True)
User.__table__.drop(engine, checkfirst=True)
Category.__table__.drop(engine, checkfirst=True)

Base.metadata.create_all(engine)

# Create Items
user1 = User(name="Konrad Schieban", email="konrad.schieban@gmail.com")
session.add(user1)
session.commit()


cat1 = Category(name="Soccer")
session.add(cat1)
session.commit()

cat2 = Category(name="Basketball")
session.add(cat2)
session.commit()

cat3 = Category(name="Golf")
session.add(cat3)
session.commit()

item1 = Item(name="Ball", user=user1, category=cat1, description="Some description here...", price="$99.99")
session.add(item1)
session.commit()

item2 = Item(name="Shoes", user=user1, category=cat1, description="Some other description here...", price="$29.99")
session.add(item2)
session.commit()

item3 = Item(name="Ball", user=user1, category=cat2, description="Some description here...", price="$39.99")
session.add(item3)
session.commit()

item4 = Item(name="Clubs", user=user1, category=cat3, description="Some description here...", price="$999.99")
session.add(item4)
session.commit()
