from app import app

client = app.test_client()


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200


def test_bookings_page():
    response = client.get("/bookings")
    assert response.status_code == 200