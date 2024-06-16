#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Function to calculate haversine distance between two points given their latitude and longitude
def main(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    # Radius of Earth in kilometers (use 6371.0 for kilometers)
    r = 6371.0

    # Calculate the distance
    distance = r * c
    return distance


if __name__ == "__main__":

    # Test the function with sample coordinates
    lat1, lon1 = 52.5200, 13.4050  # Berlin, Germany
    lat2, lon2 = 48.8566, 2.3522  # Paris, France
    distance = main(lat1, lon1, lat2, lon2)
    print("Distance between Berlin and Paris:", distance, "km")
