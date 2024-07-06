from .sfrequest import get

class BaiduMapAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.map.baidu.com"

    def geocode(self, address):
        url = f"{self.base_url}/geocoding/v3/"
        params = {
            "address": address,
            "output": "json",
            "ak": self.api_key
        }
        print(params)
        response = get(url, params=params)
        return response.json()

    def reverse_geocode(self, lat, lng):
        url = f"{self.base_url}/reverse_geocoding/v3/"
        params = {
            "location": f"{lat},{lng}",
            "output": "json",
            "ak": self.api_key
        }
        response = get(url, params=params)
        return response.json()
