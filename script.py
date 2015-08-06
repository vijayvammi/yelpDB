#Load the json files that we already know the demographics
places = get_defined_places()#get_places(zipcodes)

# This function exists in the get_places.py
new_place_zip = 50014 #Ames	
new_place = get_places([new_place_zip])

features = ['white','black','asian','alaskan','hawain','other',
			'age18_20', 'age20_25', 'age25_30', 'age30_35', 'age35_40',
			'age40_45', 'age45_50', 'age50_60',
			'salary10', 'salary20_30', 'salary30_40', 'salary40_50',
			'salary50_60', 'salary60_75', 'salary75_100', 'salary100_125']
to_match = np.zeros((len(places),len(features)))
order = places.keys()
for i, place in enumerate(order):
	for j, feature in enumerate(features):
		to_match[i,j] = getattr(places[place], feature)

match = np.zeros((1,len(features)))
for j, feature in enumerate(features):
	match[0,j] = getattr(new_place[new_place_zip], feature)

rmsd = np.sqrt(((match - to_match)**2).mean(axis=1))
sort_indexs = np.argsort(rmsd)
matched = order[sort_indexs[0]]
age_features = 	['age18_20', 'age20_25', 'age25_30', 'age30_35', 'age35_40',
			'age40_45', 'age45_50', 'age50_60']
race_features = ['white','black','asian','alaskan','hawain','other']
income_features = [	'salary10', 'salary20_30', 'salary30_40', 'salary40_50',
			'salary50_60', 'salary60_75', 'salary75_100', 'salary100_125']	

import matplotlib.pyplot as plt
#age features
plt.close()
sizes = [getattr(places[matched],feature) for feature in age_features]
total_size = sum(sizes)
sizes = [size/total_size*100 for size in sizes]
plt.pie(sizes, labels=age_features, 
        autopct='%1.1f%%', shadow=True, startangle=90)

plt.axis('equal')
plt.tight_layout()
plt.savefig('age_matched.png', dpi =300)

plt.close()
nsizes = [getattr(new_place[new_place_zip],feature) for feature in age_features]
total_size = sum(nsizes)
nsizes = [nsize/total_size*100 for nsize in nsizes]
print nsizes
plt.pie(nsizes, labels=age_features, 
        autopct='%1.1f%%', shadow=True, startangle=90)

plt.axis('equal')
plt.savefig('age_ames.png', dpi = 300)
