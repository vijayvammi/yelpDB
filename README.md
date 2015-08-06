# yelpDB
#Find correlations between Yelp database and local demographics

The idea was to use Yelp database to understand correlations between local demographics and types of restaurants that flourish in such setting. Yelp has given the data for 6 cities over US. My mini-project was focussed on finding a closely matching demographic in the yelp dataset to a new location that we are interested in and listing out the restaurants that succeed in those locations. 

create_yelp.py: Yelp has  open dataset of businesses in 6 major cities in one huge json file. This script creates a db of these businesses, especially restaurants. I used sqlalchemy ORM to do the DB creation and a local Postgressql server was the DB. 

create_census.py: The second goal was to retrieve census information about all the zipcodes that are present in the Yelp database using census API. I have written a SQL query to get all the unique zipcodes from the yelp database and looped over it to get my census information. A class was used to hold the information which was later jsonfied to prevent calls to API. 

script.py: This uses the DB and the demographic information JSON files to find the best matching zipcode and plots the distribution of different demographic features that are considered to match two locations. 


