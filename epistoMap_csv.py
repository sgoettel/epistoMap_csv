import folium
import pandas as pd
from folium.plugins import FastMarkerCluster
import random

# your filename here
input_filename = "epistoMap_input.csv"

# Constants which you can adjust here
OFFSET = 0.002
"""float: The maximum distance, in degrees of latitude and longitude, 
to randomly offset the location of a marker on the map. This is used to
prevent multiple markers from overlapping if they are located at
the same coordinates"""

POLYLINE_WEIGHT_MULTIPLIER = 1.5
"""float: The multiplier used to determine the weight/thickness 
of a polyline on the map. The weight is proportional to the number 
of letters exchanged between two people, and is calculated by multiplying 
the number of letters by this constant."""

def add_offset(lat, lng, offset):
    new_lat = lat + random.uniform(-offset, offset)
    new_lng = lng + random.uniform(-offset, offset)
    return new_lat, new_lng

def create_sender_marker(location, name):
    return folium.Marker(location=location, popup=name, icon=folium.Icon(icon="arrow-up"))

def create_receiver_marker(location, name):
    return folium.Marker(location=location, popup=name, icon=folium.Icon(icon="arrow-down"))

def populate_location_pairs(letters):
    location_pairs = {}
    for index, row in letters.iterrows():
        if pd.isnull(row["sender_place_lat"]) or pd.isnull(row["sender_place_long"]) or pd.isnull(row["receiver_place_lat"]) or pd.isnull(row["receiver_place_long"]):
            continue

        key = (row["sender_id"], row["sender_place_lat"], row["sender_place_long"], row["receiver_id"], row["receiver_place_lat"], row["receiver_place_long"])
        if key not in location_pairs:
            location_pairs[key] = {
                "count": 1,
                "sender_name": row["sender_name"],
                "receiver_name": row["receiver_name"],
                "dates": [row["date_sent"]],
                "sender_coords": (row["sender_place_lat"], row["sender_place_long"]),
                "receiver_coords": (row["receiver_place_lat"], row["receiver_place_long"]),
            }

        else:
            location_pairs[key]["count"] += 1
            location_pairs[key]["dates"].append(row["date_sent"])
    return location_pairs

# input data
letters = pd.read_csv(input_filename)

# Initialize
world_map = folium.Map(location=[50.0, 10.0], tiles="cartodb positron", zoom_start=5) # change the map tile, center and initial zoom here
marker_cluster_senders = FastMarkerCluster(data=[], name="Senders")
marker_cluster_receivers = FastMarkerCluster(data=[], name="Receivers")
location_pairs = populate_location_pairs(letters)
sender_markers = {}
receiver_markers = {}

# Loop over the location_pairs dictionary and create markers and polylines
for (sender_id, sender_lat, sender_long, receiver_id, receiver_lat, receiver_long), data in location_pairs.items():
    offset_sender_lat, offset_sender_long = add_offset(sender_lat, sender_long, OFFSET)
    offset_receiver_lat, offset_receiver_long = add_offset(receiver_lat, receiver_long, OFFSET)

    sender_key = (sender_id, sender_lat, sender_long)
    if sender_key not in sender_markers:
        sender_marker = create_sender_marker(location=[offset_sender_lat, offset_sender_long], name=data["sender_name"])
        sender_markers[sender_key] = sender_marker
        marker_cluster_senders.add_child(sender_marker)

    receiver_key = (receiver_id, receiver_lat, receiver_long)
    if receiver_key not in receiver_markers:
        receiver_marker = create_receiver_marker(location=[offset_receiver_lat, offset_receiver_long], name=data["receiver_name"])
        receiver_markers[receiver_key] = receiver_marker
        marker_cluster_receivers.add_child(receiver_marker)

    polyline_weight = POLYLINE_WEIGHT_MULTIPLIER * data["count"]
    polyline_popup = f"{data['sender_name']} to {data['receiver_name']} on " + " and ".join([f"{date}" for date in data["dates"]])

    folium.PolyLine(
        locations=[
            (offset_sender_lat, offset_sender_long),
            (offset_receiver_lat, offset_receiver_long),
        ],
        color="black",
        weight=polyline_weight,
        popup=folium.Popup(polyline_popup, max_width=300),
    ).add_to(world_map)

# Add marker clusters to map and create layer control

world_map.add_child(marker_cluster_senders)
world_map.add_child(marker_cluster_receivers)
folium.LayerControl().add_to(world_map)

# output data here
world_map.save("epistoMap_output_csv.html")