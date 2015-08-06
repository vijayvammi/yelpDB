#Create the YELP DB
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from address import AddressParser, Address

import json
import re
engine = create_engine('postgresql://santhosh:roomno123@localhost/yelp')

Base = declarative_base()
def proceed(dicti):
	categories = [str(x).lower() for x in dicti['categories']]
	lookingfor = ['food','restaurant']
	for l in lookingfor:
		for categ in categories:
			if l in categ:
				return True  

class Business(Base):
	__tablename__ = 'business'
	__table_args__ = {'schema': 'yelp'}
	business_id = Column(String, primary_key=True)
	type =Column(String)
	name = Column(String)
	full_address = Column(String)
	zipcode = Column(Integer)
	city = Column(String)
	state = Column(String)
	latitude = Column(Float)
	longitude = Column(Float)
	stars = Column(Float)
	review_count = Column(Integer)
	photo_url = Column(String)
	categories = Column(String)

Base.metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = Session()
json_file = 'business'+'.json'
ap = AddressParser()
not_found = []
with open(json_file) as f:
	for line in f:
		json_object = json.loads(line)
		if not proceed(json_object):
			continue
		json_object['categories'] = 'food'
		try:
			address = ap.parse_address(json_object['full_address'].replace('\n',','))
		except:
			continue	
		json_object['zipcode'] = address.zip
		new_object = Business()
		for key in json_object.keys():
			skey = key.lower()
			if hasattr(new_object, skey):
				setattr(new_object, skey, json_object[key])
			else:
				not_found.append(key)
		session.add(new_object)

not_found = set(not_found)
print ', '.join(not_found)
session.commit()
