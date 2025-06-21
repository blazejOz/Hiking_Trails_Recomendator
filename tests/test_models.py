import pytest
from src.models.route import Route
from src.models.user_preference import UserPreference

def test_route_constructor_valid():
    route = Route(
        id=1,
        name="Test Route",
        region="Test Region",
        start_lat=50.0,
        start_lon=20.0,
        end_lat=51.0,
        end_lon=21.0,
        length_km=10.5,
        elevation_gain=200,
        difficulty=2,
        terrain_type="forest",
        tags=["easy", "family"]
    )
    assert route.name == "Test Route"
    assert route.region == "Test Region"
    assert route.length_km == 10.5
    assert route.elevation_gain == 200
    assert route.difficulty == 2
    assert route.terrain_type == "forest"
    assert "easy" in route.tags

def test_route_constructor_negative_length():
    with pytest.raises(ValueError):
        Route(
            id=2,
            name="Bad Route",
            region="Nowhere",
            start_lat=0,
            start_lon=0,
            end_lat=0,
            end_lon=0,
            length_km=-5,
            elevation_gain=100,
            difficulty=1,
            terrain_type="urban",
            tags=[]
        )

def test_user_preference_constructor_valid():
    pref = UserPreference(
        id=1,
        user_name="tester",
        preferred_temp_min=5.0,
        preferred_temp_max=25.0,
        max_precipitation=8.0,
        max_difficulty=2,
        max_length_km=15.0,
        forecast_date="2025-06-21"
    )
    assert pref._name == "tester"
    assert pref._preferred_temp_min == 5.0
    assert pref._max_length_km == 15.0

def test_user_preference_negative_length():
    with pytest.raises(ValueError):
        UserPreference(
            id=2,
            user_name="bad",
            preferred_temp_min=0,
            preferred_temp_max=20,
            max_precipitation=5,
            max_difficulty=2,
            max_length_km=-10,
            forecast_date="2025-06-21"
        )