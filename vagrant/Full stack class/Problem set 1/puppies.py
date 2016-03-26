from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()


puppies_and_adopters = Table('adopted_by', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppy.id')),
    Column('adopter_id', Integer, ForeignKey('adopter.id')))


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer)
    current_occupancy = Column(Integer)

    
class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))
    
    profile = relationship("Puppy_Profile",
        uselist = False,
        back_populates = "puppy")

    adopters = relationship("Adopter",
        secondary = puppies_and_adopters,
        back_populates = "puppies")


class Puppy_Profile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key = True)
    pic_url = Column(String(250))
    description = Column(String(250))
    needs = Column(String(250))

    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", back_populates = "profile")


class Adopter(Base):
    __tablename__ = "adopter"

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    puppies = relationship("Puppy",
        secondary = puppies_and_adopters,
        back_populates = "adopters")





engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)