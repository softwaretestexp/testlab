import sys
import pytest

sys.path.append("../")
from utils.mapserv import BaiduMapAPI
from utils.sfrequest import get

@pytest.fixture
def api_key():
    return "wdzFSF98TRzTYrHOnro9rUYZY2NTiNTK"

@pytest.fixture
def baidu_map(api_key):
    return BaiduMapAPI(api_key)

def test_geocode_success(baidu_map):
    address = "北京市海淀区上地十街10号"
    response = baidu_map.geocode(address)
    assert response["status"] == 0
    assert "result" in response
    assert "location" in response["result"]

def test_reverse_geocode_success(baidu_map):
    lat, lng = 39.983424, 116.322987
    response = baidu_map.reverse_geocode(lat, lng)
    assert response["status"] == 0
    assert "result" in response
    assert "formatted_address" in response["result"]

def test_invalid_api_key():
    baidu_map = BaiduMapAPI("invalid_key")
    address = "北京市海淀区上地十街10号"
    response = baidu_map.geocode(address)
    assert response["status"] != 0

def test_invalid_address(baidu_map):
    address = "4398483948"
    response = baidu_map.geocode(address)
    assert response["status"] == 1

def test_geocode_missing_params(baidu_map):
    response = get(f"{baidu_map.base_url}/geocoding/v3/", params={"ak": baidu_map.api_key})
    assert response.status_code == 200

def test_reverse_geocode_missing_params(baidu_map):
    response = get(f"{baidu_map.base_url}/reverse_geocoding/v3/", params={"ak": baidu_map.api_key})
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main(["-v", "test_mapserv.py"])
