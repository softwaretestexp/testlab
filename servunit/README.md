# Baidu Maps API Unit Testing Project

This project is designed to test the functionality of the Baidu Maps Web Service API, including geocoding and reverse geocoding operations. It uses the `pytest` framework for unit testing.

## Features

- **Geocoding**: Convert addresses into geographical coordinates.
- **Reverse Geocoding**: Convert geographical coordinates into readable addresses.
- **API Key Validation**: Test the validity of the provided API key.
- **Parameter Handling**: Ensure that the API responds correctly to missing parameters.

## Technologies

- **Python**: The primary programming language used for the project.
- **pytest**: A testing framework for Python.
- **Baidu Maps API**: The web service API used for geocoding and reverse geocoding.

## Project Structure

- `test_mapserv.py`: Contains the unit tests for the Baidu Maps API functionalities.
- `mapserv.py`: Contains the `BaiduMapAPI` class, which interfaces with the Baidu Maps Web Service API.

## How to Run

1. Ensure you have `pytest` installed:
    ```bash
    pip install pytest
    ```
2. Run the tests:
    ```bash
    pytest -v test_mapserv.py
    ```

## Files

### test_mapserv.py

This file includes the unit tests for the BaiduMapAPI class. The tests cover various scenarios, including successful requests, invalid API keys, and missing parameters.

### mapserv

This file contains the `BaiduMapAPI` class, which provides methods for geocoding and reverse geocoding using the Baidu Maps Web Service API.

## Testing

The tests included in this project are:

- **test_geocode_success**: Tests successful geocoding of an address.
- **test_reverse_geocode_success**: Tests successful reverse geocoding of coordinates.
- **test_invalid_api_key**: Tests the response when using an invalid API key.
- **test_invalid_address**: Tests the response when providing an invalid address.
- **test_geocode_missing_params**: Tests the response when required parameters are missing in a geocode request.
- **test_reverse_geocode_missing_params**: Tests the response when required parameters are missing in a reverse geocode request.
