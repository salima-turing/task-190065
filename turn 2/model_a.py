import unittest
import requests
import math

# Base DataFilter class
class DataFilter:
	def filter_data(self, data):
		raise NotImplementedError

# Concrete DataFilter class for filtering by distance using Haversine formula
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
		R = 6371  # Earth radius in kilometers
		dlat = math.radians(lat1 - self.center_lat)
		dlon = math.radians(lon1 - self.center_lon)
		a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(self.center_lat)) * math.cos(
			math.radians(lat1)
		) * math.sin(dlon / 2) * math.sin(dlon / 2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		return R * c


# New class to handle real-time geospatial data filtering
class RealTimeGeospatialFilter(DataFilter):
	def __init__(self, api_key, max_distance):
		self.api_key = api_key
		self.max_distance = max_distance
		self.base_url = "http://api.open-notify.org/iss-now.json"

	def filter_data_by_iss_location(self, data):
		filtered_data = []

		# Fetch current ISS position
		iss_position = self.fetch_iss_position()

		if iss_position:
			iss_lat = iss_position['latitude']
			iss_lon = iss_position['longitude']

			for entry in data:
				lat = entry["location"]["lat"]
				lon = entry["location"]["lon"]
				distance = self.calculate_distance(lat, lon, iss_lat, iss_lon)
				if distance <= self.max_distance:
					filtered_data.append(entry)

		return filtered_data

	def fetch_iss_position(self):
		response = requests.get(self.base_url)
		if response.status_code == 200:
			data = response.json()
			return data['iss_position']
		else:
			print(f"Failed to fetch ISS position. Status code: {response.status_code}")
			return None

	def calculate_distance(self, lat1, lon1, lat2, lon2):
		from math import radians, cos, sin, asin, sqrt

		"""
		Calculate distance between two points 
		on the earth (specified in decimal degrees)
		"""
		# convert decimal degrees to radians
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

		# haversine formula
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a))
		# Radius of earth in kilometers is 6371
		return c * 6371


# Unit test class to validate the framework's extensibility
class TestDataFilterExtensibility(unittest.TestCase):
	def setUp(self):
		self.data = [
			{"name": "Alice", "location": {"lat": 32.6514, "lon": -161.4333}},
			{"name": "Bob", "location": {"lat": 37.7747, "lon": -122.4182}},
			{"name": "Charlie", "location": {"lat": -33.8688, "lon": 151.2093}},
		]
		self.api_key = "YOUR_OPEN_NOTIFY_API_KEY"

	def test_distance_filter(self):
		# Test DistanceFilter as before
		pass

	def test_real_time_geospatial_filter(self):
		max_distance = 10000
		filter = RealTimeGeospatialFilter(self.api_key, max_distance)
		filtered_data = filter.filter_data_by_iss_location(self.data)
		self.assertIsNotNone(filtered_data)
		# Add more assertions based on expected results or data characteristics

if __name__ == "__main__":
	unittest.main()
