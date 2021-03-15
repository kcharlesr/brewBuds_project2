# brewBuds_project2
 
Data Sources:
Brewery CSV:https://data.world/datafiniti/breweries-brew-pubs-in-the-usa
Starbucks CSV: https://gist.github.com/dankohn/09e5446feb4a8faea24
Census/IRS Data:https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-2018-zip-code-data-soi
State-ZipCode GeoJSON: 
https://github.com/OpenDataDE/State-zip-code-GeoJSON
https://github.com/OpenDataDE/State-zip-code-GeoJSON

Inspiration:
We are marketing analysts for the “Holy Ale Brewery” we are trying to convince the leaders of this organization that in the next 5 cities we should open our new breweries. Using the data above we will create a dashboard that explains which cities would be an investment opportunity based on population and median household income.


Methods 

1). Data CSV were cleaned using python/pandas to remove null values, unusable columns, and rename columns. 

3). Used pandas to create a sqlite engine and read the csv files into a database with each csv becoming its own table. 
![image](https://user-images.githubusercontent.com/73393825/111224040-50bb6d00-85b4-11eb-8302-82ecec1f9b05.png)

5). SQL Alchemy was used to read in the and query from the sqlite database this enabled our group to create queries of the data that we could use to create the ranking system, brew flask, and html page. 

![image](https://user-images.githubusercontent.com/73393825/111224498-ebb44700-85b4-11eb-8841-f534b1161afc.png)


![image](https://user-images.githubusercontent.com/73393825/111224388-c6bfd400-85b4-11eb-82ec-2baf791d3ad9.png)


7). The purpose of this project was identified key locations that our potential clients would be interested in. In order to identify these, we created a ranking system:

How The Ranking System was Assigned: 
Logic: We have 4 Variables if a zipcode is ideal 
	Median Income
	Population per brewery
	Key demo 20 -34 
	Population per starbucks 

If no breweries/no Starbucks assigned a numerical 1 this was to ensure that there was still a result for the per population and this did not significantly alter the ranking system 
Combined all the data and then 4 columns for each data set that ranked individually. And then aggregated the ranks and then scored the overall zip code based on the aggregate ranks. This then determined the zip code selection. Ranked 1 being the highest desirable 100 being the lowest desirable.

![image](https://user-images.githubusercontent.com/73393825/111224733-3cc43b00-85b5-11eb-9a88-774c0ff094b2.png)


5). The html page created for the data analysis and presentation to our clients visualizes our key points for our presentation:
	1). GeoJson mapping
	2). Leaflet markers (Breweries and Starbucks)
	3). Scatter plot showing percentage of our key demographic, population per brewery, and Median income.

![image](https://user-images.githubusercontent.com/73393825/111224574-05ee2500-85b5-11eb-847a-f7566e4b1b12.png)

![image](https://user-images.githubusercontent.com/73393825/111224618-156d6e00-85b5-11eb-8b4d-6fd7f45e2d35.png)



6). The new json library we used slick enhanced the webpage for the clients by providing photograoh visuals that can be scrolled through in the html page.

![image](https://user-images.githubusercontent.com/73393825/111223081-0eddf700-85b3-11eb-8564-c1149d97c3f5.png)


