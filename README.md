# graphite:

The commands specified in this part are to be made in the base of the repository.

### making the data file

To make the data file in a format readable by graphite, execute the command:

python3 src/graphite/convert_to_graphite.py

### loading the data into graphite

To load the data into graphite and benchmark on the data ingestion speed:

python3 src/graphite/send_to_graphite.py    

### Benchmarking on requests:

To make requests to the API, we are using the api_queries.py script placed in src/graphite.
this python script needs an argument and returns a graph on the time of execution for various data points

To test the select queries:
python3 src/graphite/api_queries.py 'select'

To test the aggregated queries:
python3 src/graphite/api_queries.py 'aggregated'

To test the graph queries:
python3 src/graphite/api_queries.py 'graph'
