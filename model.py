# Create the sqlite database and map python objects
# Configuration: import all modules needed
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuration: Create instance of declarative base (class code will inherit this)
Base = declarative_base()


# Class: Representation of table as a python class, extends the Base class
class Artist(Base):
    __tablename__ = 'artist'  # Table in the database

    # Mapper: Maps python objects to columns in the database
    id = Column(Integer, primary_key=True)  # auto incremented
    name = Column(String(80), nullable=False)
    # genre = Column(String(20), nullable=False)


class Album(Base):
    __tablename__ = 'album'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)  # auto incremented
    # artist_id = Column(String(50),nullable=False)
    date = Column(Integer, nullable=False)

    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship(Artist)
