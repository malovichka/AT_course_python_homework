import requests as r

HEADERS = {"Content-Type": "application/json"}
BASE_URL = "https://api.punkapi.com/v2/beers/"
BEER_ID = 1
BEER_NAME = "Buzz"
BEER_ABV = 4.5
RANDOM_ENDPOINT = "random"
PAYLOAD = [
    {
        "name": "Pivo",
        "tagline": "str",
        "first_brewed": "str",
        "description": "str",
        "image_url": "https://images.punkapi.com/v2/192.png",
        "abv": 6.0,
        "ibu": 60.0,
        "target_fg": 1010.0,
        "target_og": 1056.0,
        "ebc": 17.0,
        "srm": 8.5,
        "ph": 4.4,
        "attenuation_level": 82.14,
        "volume": {"value": 20, "unit": "liters"},
        "boil_volume": {"value": 25, "unit": "liters"},
        "method": {
            "mash_temp": [{"temp": {"value": 65, "unit": "celsius"}, "duration": 75}],
            "fermentation": {"temp": {"value": 19.0, "unit": "celsius"}},
        },
        "ingredients": {
            "malt": [
                {"name": "Extra Pale", "amount": {"value": 5.3, "unit": "kilograms"}}
            ],
            "yeast": "str",
        },
        "food_pairing": ["str"],
        "brewers_tips": "str",
        "contributed_by": "str",
    }
]
NOT_FOUND_BASE = "No endpoint found that matches '/v2/beers/'"
NOT_FOUND_ID = f"No endpoint found that matches '/v2/beers/{BEER_ID}'"


def test_get_single_beer():
    """Test verifies sending GET /id is successfull and returns valid data"""
    get_beer_data = r.get(BASE_URL + str(BEER_ID))
    assert (
        get_beer_data.status_code == 200
    ), f"GET beer data returned {get_beer_data.status_code}, expected - 200"
    assert (
        get_beer_data.json()[0]["name"] == BEER_NAME
    ), f'Received beer name {get_beer_data.json()[0]["name"]}, expected - {BEER_NAME}'
    assert (
        get_beer_data.json()[0]["abv"] == BEER_ABV
    ), f'Received beer name {get_beer_data.json()[0]["abv"]}, expected - {BEER_ABV}'


def test_get_random_beer():
    """Test verifies that sending GET /random is successfull and returns data"""
    get_random_beer = r.get(BASE_URL + RANDOM_ENDPOINT)
    assert (
        get_random_beer.status_code == 200
    ), f"GET random beer returned {get_random_beer.status_code}, expected - 200"
    assert get_random_beer.json() != None, f"Get random beer returned no content"


def test_post_method_not_found():
    """Test verifies that POST method is not supported"""
    create_beer = r.post(BASE_URL, json=PAYLOAD, headers=HEADERS)
    assert (
        create_beer.status_code == 404
    ), f"POST request ended with {create_beer.status_code}, expected - 404"
    assert (
        create_beer.json()["message"] == NOT_FOUND_BASE
    ), f'POST request message is {create_beer.json()["message"]}, expected {NOT_FOUND_BASE}'


def test_delete_method_not_found():
    """Test verifies that DELETE method is not supported"""
    delete_beer = r.delete(BASE_URL + str(BEER_ID))
    assert (
        delete_beer.status_code == 404
    ), f"POST request ended with {delete_beer.status_code}, expected - 404"
    assert (
        delete_beer.json()["message"] == NOT_FOUND_ID
    ), f'POST request message is {delete_beer.json()["message"]}, expected {NOT_FOUND_ID}'
