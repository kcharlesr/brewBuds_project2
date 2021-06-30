# brewBuds_project2

## Inspiration
<br>
We are marketing analysts for the “Holy Ale Brewery” trying to convince the leaders of this organization in which 5 cities they should open new breweries. Using the data above we will create a dashboard that explains which cities would be an investment opportunity based on population and median household income. 
<br>

## Data Sources
<br>
Brewery CSV:https://data.world/datafiniti/breweries-brew-pubs-in-the-usa
<br>
Starbucks CSV: https://gist.github.com/dankohn/09e5446feb4a8faea24
<br>
Census/IRS Data:https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-2018-zip-code-data-soi
<br>
State-ZipCode GeoJSON: 
https://github.com/OpenDataDE/State-zip-code-GeoJSON
<br>

## Methods 
<br>

1. Data CSV were cleaned using Python/Pandas to remove null values, unusable columns, and rename columns.
<br>

2. Used Pandas to create a SQLite engine and read the CSV files into a database with each CSV becoming its own table. 
   
![image](https://user-images.githubusercontent.com/73393825/111224040-50bb6d00-85b4-11eb-8302-82ecec1f9b05.png)
<br>

3. SQL Alchemy was used to connect to the SQLite database. This enabled our group to create queries of the data that we could use to create the ranking system, brew Flask, and HTML page. 
   
![image](https://user-images.githubusercontent.com/73393825/111224498-ebb44700-85b4-11eb-8841-f534b1161afc.png)


![image](https://user-images.githubusercontent.com/73393825/111224388-c6bfd400-85b4-11eb-82ec-2baf791d3ad9.png)

<br>

4. The purpose of this project was to identify key locations that our potential clients would be interested in. In order to identify these, we created a ranking system.

How The Ranking System was Assigned: 
<br>
Logic: We used 4 variables to determine if a zipcode is ideal 
<br>

* Median Income
* Population per brewery
* Key demo 20 -34 
* Population per starbucks 
<br>

If no breweries/no Starbucks were found in a zipcode, it was assigned a numerical of 1  to ensure that there was still a result for the per population calculation and this did not significantly alter the ranking system.
We combined all of the data including the 4 columns from each data set that ranked the zipcodes individually. We then aggregated the ranks and scored the overall zip code based on the aggregate ranks. This then determined the zip code selection. Rank 1 being the most desirable and 100 being the least desirable.

![image](https://user-images.githubusercontent.com/73393825/111224733-3cc43b00-85b5-11eb-9a88-774c0ff094b2.png)

<br>

5. The HTML page created for the data analysis and presentation to our clients visualizes our key points for our presentation:
	1). GeoJson mapping
	2). Leaflet markers (Breweries and Starbucks)
	3). Scatter plot showing percentage of our key demographic, population per brewery, and median income.

![image](https://user-images.githubusercontent.com/73393825/111224574-05ee2500-85b5-11eb-847a-f7566e4b1b12.png)

![image](https://user-images.githubusercontent.com/73393825/111224618-156d6e00-85b5-11eb-8b4d-6fd7f45e2d35.png)

<br>

6. We also used a new JSON library, Slick, to enhance the webpage for the clients by providing photo visuals that can be scrolled through in the HTML page.

![image](https://user-images.githubusercontent.com/73393825/111223081-0eddf700-85b3-11eb-8564-c1149d97c3f5.png)


