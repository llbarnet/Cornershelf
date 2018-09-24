import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base) :
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(50), nullable=False)
    cookbook_name = Column(String(150))



class Cookbook(Base) :
    __tablename__ = 'cookbook'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), ForeignKey('user.cookbook_name'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """return object data in serializable format"""
        return {
            'id' : self.id,
            'name' : self.name,
            }

class Recipes(Base) :
     __tablename__ = 'recipes'
     id = Column(Integer, primary_key=True)
     name = Column(String(80), nullable = False)
     ingredients = Column(String(300), nullable = False)
     directions = Column(String(800), nullable = False)
     type = Column(String(50))
     cookbook_id = Column(Integer, ForeignKey('cookbook.id'))
     cookbook = relationship(Cookbook)
     user_id = Column(Integer, ForeignKey('user.id'))
     user = relationship(User)

     @property
     def serialize(self):
         """return object data in serializable format"""
         return {
             'id' : self.id,
             'name' : self.name,
             'ingredients' : self.ingredients,
             'directions' : self.directions,
             'type' : self.type,
             }

engine = create_engine('sqlite:///cornershelf.db')

Base.metadata.create_all(engine)
