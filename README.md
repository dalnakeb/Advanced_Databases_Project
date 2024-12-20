# graphite:

The commands specified in this part are to be made in the base of the repository.
Also, as this benchmarking was made using the docker version you need to already have docker installed on your computer.

### Installing Graphite:

use this command to install graphite on docker on your computer:
docker run -d \
 --name graphite \
 --restart=always \
 -p 80:80 \
 -p 2003-2004:2003-2004 \
 -p 2023-2024:2023-2024 \
 -p 8125:8125/udp \
 -p 8126:8126 \
 graphiteapp/graphite-statsd

 then, ensure it is working correctly with :
 docker ps
 this line should show the graphite docker running

 If your graphite host and ports are not the default ones, they should be corrected at the start of send_to_graphite.py and api_queries.py

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
