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

'''  Not sure whether this belongs in this file or not

from sqlalchemy.orm import sessionmaker
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def check_in(puppy, shelter):
    if shelter.current_occupancy < shelter.maximum_capacity:
        shelter.current_occupancy += 1
        puppy.shelter_id = shelter.id
        checked_in = True
        session.add(puppy)
        session.add(shelter)
        session.commit()
    else:
        shelters = session.query(Shelter).order_by(current_occupancy)
        checked_in = False
        for shelter in shelters:
            if shelter.current_occupancy < shelter.maximum_capacity:
                shelter.current_occupancy += 1
                puppy.shelter_id = shelter.id
                checked_in = True
                session.add(puppy)
                session.add(shelter)
                session.commit()
        if not checked_in:
            raise ValueError("All shelters are full, \
                time to open a new one!")


def adopt_puppy(puppy, family):
    shelter = session.query(Shelter).filter_by(id = puppy.shelter.id).one()
    shelter.current_occupancy -= 1
    session.add(shelter)
    puppy.shelter_id = None
    for person in family:
        puppy.adopters.append(person.id)
    session.add(puppy)
    session.commit()
'''

