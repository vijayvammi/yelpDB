from __future__ import division
import urllib3
import os, re, json, cPickle

key_to_code = {         'B01003_001E' : 'total_population',
'B01001_002E' : 'male_population',         'B01001_026E' :
'female_population',         'B02001_002E' : 'white',
'B02001_003E' : 'black',         'B02001_004E' : 'alaskan',
'B02001_005E' : 'asian',         'B02001_006E' : 'hawain',
'B02001_007E' : 'other',         'B01001_007E' : 'male_18_19',
'B01001_031E' : 'female_18_19',         'B01001_008E' : 'male_20',
'B01001_032E' : 'female_20',         'B01001_009E' : 'male_21',
'B01001_033E' : 'female_21',         'B01001_010E' : 'male_22_24',
'B01001_034E' : 'female_22_24',         'B01001_011E' : 'male_25_29',
'B01001_035E' : 'female_25_29',         'B01001_012E' : 'male_30_35',
'B01001_036E' : 'female_30_35',         'B01001_013E' : 'male_35_39',
'B01001_037E' : 'female_35_39',         'B01001_014E' : 'male_40_45',
'B01001_038E' : 'female_40_45',         'B01001_015E' : 'male_45_49',
'B01001_039E' : 'female_45_49',         'B01001_016E' : 'male_50_54',
'B01001_040E' : 'female_50_54',         'B01001_017E' : 'male_55_59',
'B01001_041E' : 'female_55_59',         'B19001_002E' : '10K',
'B19001_003E' : '10_15K',         'B19001_004E' : '15_20K',
'B19001_005E' : '20_25K',         'B19001_006E' : '25_30K',
'B19001_007E' : '30_35K',         'B19001_008E' : '35_40K',
'B19001_009E' : '40_45K',         'B19001_010E' : '45_50K',
'B19001_011E' : '50_60K',         'B19001_012E' : '60_75K',
'B19001_013E' : '75_100K',         'B19001_014E' : '100_125K'
}


# reverse mappting
code_to_key = {}
for key in key_to_code:
	code_to_key[key_to_code[key]] = key

http = urllib3.PoolManager()
# find the zip codes from yelp
# Basically an SQL query to get the zip codes in the database
# I have saved the unique zip codes in a list and retrieved the 
# demographic information for them and saved them as a dictionary
# for later retrieval. 
class Place():
	def __init__(self):
		self.zipcode = 0
		self.total_population = 0
		self.white = 0
		self.black = 0
		self.asian = 0
		self.alaskan = 0
		self.hawain = 0
		self.other = 0
		self.age18_20 = 0
		self.age20_25 = 0
		self.age25_30 = 0
		self.age30_35 = 0
		self.age35_40 = 0
		self.age40_45 = 0
		self.age45_50 = 0
		self.age50_60 = 0
		self.salary10 = 0
		self.salary10_20 = 0
		self.salary20_30 = 0
		self.salary30_40 = 0
		self.salary40_50 = 0
		self.salary50_60 = 0
		self.salary60_75 = 0
		self.salary75_100 = 0
		self.salary100_125 = 0

# Given a list of Zip codes, find the demographic information
def get_places(zipcodes):
	base_url = 'http://api.census.gov/data/2012/acs5?key=<intentionally_Removed'&&get='+','.join(key_to_code.keys())+'&for=zip+code+tabulation+area:' 
	places = {}
	for zipcode in zipcodes:
		r = http.request('GET', base_url + str(zipcode))
		if not r.status == 200:
			continue
		[codestring, valuestring] = re.compile('\n').split(r.data)
		codes = re.compile('\"*\"').split(codestring)
		values = re.compile('\"*\"').split(valuestring)
		mapping = {}
		for i in range(len(codes)):
			#print codes[i] + '    ' + values[i]
			if codes[i] in key_to_code:
				mapping[key_to_code[codes[i]]] = int(values[i])
		total_population = mapping['total_population']
		if total_population == 0:
			continue
		place = Place()
		place.zipcode = zipcode
		place.total_population =  total_population
		place.white = mapping['white']/total_population
		place.black = mapping['black']/total_population
		place.asian = mapping['asian']/total_population
		place.alaskan = mapping['alaskan']/total_population
		place.hawain = mapping['hawain']/total_population
		place.other = mapping['other']/total_population
		place.age18_20 = (mapping['male_18_19'] + mapping['female_18_19'] \
						  +	mapping['male_20'] + mapping['female_20'])/total_population
		place.age20_25 = (mapping['male_22_24'] + mapping['female_22_24'] \
						 +	mapping['male_21'] + mapping['female_21'])/total_population
		place.age25_30 = (mapping['male_25_29'] + mapping['female_25_29'] )/total_population
		place.age30_35 = (mapping['male_30_35'] + mapping['female_30_35'] )/total_population
		place.age35_40 = (mapping['male_35_39'] + mapping['female_35_39'] )/total_population
		place.age40_45 = (mapping['male_40_45'] + mapping['female_40_45'] )/total_population
		place.age45_50 = (mapping['male_45_49'] + mapping['female_45_49'] )/total_population
		place.age50_60 = (mapping['male_50_54'] + mapping['female_50_54'] \
						 + mapping['male_55_59'] + mapping['female_55_59']			)/total_population	
		place.salary10 = mapping['10K']/total_population
		place.salary10_20 = (mapping['10_15K'] + mapping['15_20K'])/total_population
		place.salary20_30 = (mapping['20_25K'] + mapping['25_30K'])/total_population
		place.salary30_40 = (mapping['30_35K'] + mapping['35_40K'])/total_population
		place.salary40_50 = (mapping['40_45K'] + mapping['45_50K'])/total_population
		place.salary50_60 = mapping['50_60K']/total_population
		place.salary60_75 = mapping['60_75K']/total_population
		place.salary75_100 = mapping['75_100K']/total_population
		place.salary100_125 = mapping['100_125K']/total_population
		json_place = json.dumps(place.__dict__)
		#print json_place
		#with open(str(zipcode)+ '.place', 'w') as f:
		#	f.write(json_place)
		places[zipcode] = place	
	return places

# For all the zipcodes in Yelp database, retrieve the demographic
# information. This code is not shown here. 
