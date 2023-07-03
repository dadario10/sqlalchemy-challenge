# sqlalchemy-challenge

### Project Description
 - This assignment uses SQL Alchemy to look into Honolulu, Hawaii climate before a vacation. 3 files were provided and SQL, Jupyter Notebook, and Python was used to link the files and obtain specific information that was requested.
### Summary of Contents
 - Part 1: Analyze and Explore the Climate Data
     - Basic climate analysis and data exploration of climate database
     - Uses the SQLAlchemy "create_engine()" function to connect to SQLite database
     - Uses the SQLAlchemy "automap_base()" function to reflect tables into classes, and then saves references to the classes named "station" and "measurement".
     - Links Python to the database by creating a SQLAlchemy session.
- Precipitation Analysis
     - Finds the most recent data in the dataset
     - Uses the most recent date to get the previous 12 months of percipitation data by querying the previous 12 months of data
     - Loads the query results into a Pandas DataFrame
     - Sorts teh DataFrame values by "date"
     - Plots the results
     - Uses Pandas to print the summary statistics for the precipitation data
 - Station Alalysis
     - Designs a query to calculate the total number of stations in the dataset
     - Designs a query to find the most active stations
     - Designs a query to calaculate the lowest, highest and average temperatures of the most active station id
     - Designs a query to get the previous 12 months of temperature observation data
     - Closes the session
 - Part 2: Designs a climate app
     - Uses Flask API based on developed queries to create a homepage and list of routes
     - Converts the query results from analysis to a directory
     - Returns a JSON list of stations
     - Queries the dates and temperature observations of the most active station for the previous year of data
     - Returns a JSON list of Minimum, Average and Maximum temperatures for a specified start and start-end range
### Getting Started
 - This assignment uses Jupyter Notebook and Visual Studio to the provided data and obtain the required information
### Acknowledgements
 - API SQLite
 - Jupyter Notebook
 - Visual Studio
