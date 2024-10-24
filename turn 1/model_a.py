import unittest

class Location:
	def __init__(self, name, latitude, longitude):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude

class DataFilter:
	def apply(self, locations):
		pass

class WithinRadiusFilter(DataFilter):
	def __init__(self, center_lat, center_lon, radius):
		self.center_lat = center_lat
		self.center_lon = center_lon
		self.radius = radius

	def apply(self, locations):
		filtered_locations = []
		for location in locations:
			import math
			distance = math.sqrt((location.latitude - self.center_lat)**2 + (location.longitude - self.center_lon)**2)
			if distance <= self.radius:
				filtered_locations.append(location)
		return filtered_locations

class TestLocationFilters(unittest.TestCase):

	def setUp(self):
		self.locations = [
			Location("London", 51.5074, 0.1278),
			Location("New York", 40.7128, -74.0060),
			Location("Paris", 48.8566, 2.3522),
			Location("Sydney", -33.8688, 151.2093),
			Location("San Francisco", 37.7747, -122.4182),
		]

	def test_within_radius_filter(self):
		center_lat = 37.7747  # Center of San Francisco
		center_lon = -122.4182
		radius = 100  # Radius in kilometers

		filter = WithinRadiusFilter(center_lat, center_lon, radius)
		filtered_locations = filter.apply(self.locations)

		self.assertEqual(len(filtered_locations), 2)
		self.assertIn(Location("San Francisco", 37.7747, -122.4182), filtered_locations)
		self.assertIn(Location("Oakland", 37.8044, -122.2711), filtered_locations)

if __name__ == '__main__':
	unittest.main()
