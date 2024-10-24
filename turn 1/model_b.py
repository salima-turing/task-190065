import unittest
import math

# Sample data
data = [
    {"name": "Alice", "location": {"lat": 32.6514, "lon": -161.4333}},
    {"name": "Bob", "location": {"lat": 37.7747, "lon": -122.4182}},
    {"name": "Charlie", "location": {"lat": -33.8688, "lon": 151.2093}},
]


# Base DataFilter class
class DataFilter:
    def filter_data(self, data):
        raise NotImplementedError("Subclasses must implement filter_data method")


# Concrete DataFilter class for filtering by distance
class DistanceFilter(DataFilter):
    def __init__(self, center_lat, center_lon, max_distance):
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.max_distance = max_distance

    def filter_data(self, data):
        import math

        filtered_data = []
        for entry in data:
            lat = entry["location"]["lat"]
            lon = entry["location"]["lon"]
            distance = self.calculate_distance(lat, lon)
            if distance <= self.max_distance:
                filtered_data.append(entry)
        return filtered_data

    def calculate_distance(self, lat1, lon1):
        # Haversine formula to calculate distance between two points
        R = 6371  # Earth radius in kilometers
        dlat = math.radians(lat1 - self.center_lat)
        dlon = math.radians(lon1 - self.center_lon)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(self.center_lat)) * math.cos(
            math.radians(lat1)
        ) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c


# Unit test class for DataFilter
class TestDataFilter(unittest.TestCase):
    def setUp(self):
        self.data = data

    def test_distance_filter(self):
        # Create a DistanceFilter with a center point and max distance
        center_lat = 37.7747
        center_lon = -122.4182
        max_distance = 100  # kilometers
        filter = DistanceFilter(center_lat, center_lon, max_distance)

        # Filter the data using the DistanceFilter
        filtered_data = filter.filter_data(self.data)

        # Assert the expected result
        expected_filtered_data = [
            {"name": "Bob", "location": {"lat": 37.7747, "lon": -122.4182}},
        ]
        self.assertEqual(filtered_data, expected_filtered_data)


if __name__ == "__main__":
    unittest.main()
