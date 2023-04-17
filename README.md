# epistoMap

This script is designed to create an interactive map visualization of letters sent between people from different locations. It reads input data from a CSV file, processes it, and generates an HTML file containing the map with sender and receiver markers and polylines connecting them.

To run the script, simply execute it in your terminal or command prompt with Python:

`$ python3 epistoMap.py` 

Make sure the input CSV file is in the same directory as the script. After the script finishes running, you'll find the generated HTML file (`epistoMap_output.html`) in the same directory.

## Prerequisites

To run this script, you need Python 3.x installed on your system along with Folium and Pandas libraries.-   

You can install these packages using pip:

`$ pip install folium pandas` 

## Input

The input data should be a CSV file with the following columns:
-   sender_id
-   sender_name
-   sender_place_lat (latitude)
-   sender_place_long (longitude)
-   date_sent
-   receiver_id
-   receiver_name
-   receiver_place_lat
-   receiver_place_long

Each row in the CSV file should be a letter sent from a sender to a receiver. The latitude and longitude values should be numerical and correspond to the geographic locations of the sender and receiver.
If you don't have the coordinates yet, you can use `geonames_coordinates.py` for GeoNames IDs, or `gnd_id_coordinates.py` for GND IDs from [this repo](https://github.com/sgoettel/teihdr2csv).



## Processing

The script reads the input data using pandas and processes it to extract unique sender-receiver pairs. It groups the letters based on sender and receiver IDs, ensuring that a sender or receiver is only displayed once when they are at the exact same location.

The script employs the folium library to create an interactive map with two marker clusters: one for senders and another for receivers. It uses a custom `add_offset` function to slightly offset the markers to prevent overlapping when multiple individuals are at the same location.

## Output

The output is an interactive HTML map with some features.  Senders and receivers are represented by distinct markers (arrow-up for senders, arrow-down for receivers) with polyline connections between sender and receiver locations. You easily can change the map tiles, adjust the offset value in the `add_offset` function to control the marker separation or alter the polyline color, weight, and popup content etc.
