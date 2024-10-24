import requests


class MapboxGeocoder:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

    def geocode(self, address):
        url = f"{self.base_url}{address}.json?access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Geocoding failed with status code: {response.status_code}")


class MapboxDataFilter(DataFilter):
    def __init__(self, max_distance, access_token):
        self.max_distance = max_distance
        self.geocoder = MapboxGeocoder(access_token)

    def filter_data(self, data, center_address):
        # Geocode the center address to get its coordinates
        center_coordinates = self.geocode_address(center_address)

        # Initialize a DistanceFilter with the center coordinates
        distance_filter = DistanceFilter(*center_coordinates, self.max_distance)
        return distance_filter.filter_data(data)

    def geocode_address(self, address):
        geocode_result = self.geocoder.geocode(address)
        features = geocode_result.get("features")
        if not features:
            raise Exception("Geocoding failed to return any results.")

        first_feature = features[0]
        center = first_feature.get("center")
        if not center:
            raise Exception("Geocoded feature did not contain center coordinates.")

        return center
