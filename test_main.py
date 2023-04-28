"""This module tests the FastAPI's in the main module using Pytest."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_movies():
    """Tests getting all movies."""
    response = client.get("/api/v1/movies")
    assert response.status_code == 200

def test_get_wrong_movie_id_details():
    """Tests getting specific movie with wrong id."""
    response = client.get("/api/v1/movies/kasjdfbksdf")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie with the given id was not found"}

def test_get_right_movie_id_details():
    """Tests getting right movie with the right id."""
    response = client.get("/api/v1/movies/TTGCgiDFiPm1y2ei8QqT")
    assert response.status_code == 200

def test_booking_ticket_with_non_existent_id():
    """Tests booking ticket with wrong id."""
    response = client.post(
        "/api/v1/book",
        json =  {
            "movie_id": "kasjdfbksdf",
            "number_of_tickets": 12
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail" : "Movie with the given id was not found"}

def test_booking_tickets_more_than_avaiable():
    """Tests booking more tickets than available."""
    response = client.post(
        "/api/v1/book",
        json =  {
            "movie_id": "TTGCgiDFiPm1y2ei8QqT",
            "number_of_tickets": 99
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Not enough tickets. Reduce number of tickets to book or Try another movie"
    }

def test_booking_negative_tickets():
    """Tests booking negative number of tickets."""
    response = client.post(
        "/api/v1/book",
        json =  {
            "movie_id": "TTGCgiDFiPm1y2ei8QqT",
            "number_of_tickets": -9
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Bad request. Can't buy zero or negative tickets"}

def test_booking_zero_tickets():
    """Tests booking zero tickets."""
    response = client.post(
        "/api/v1/book",
        json =  {
            "movie_id": "TTGCgiDFiPm1y2ei8QqT",
            "number_of_tickets": 0
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad request. Can't buy zero or negative tickets"
    }
