from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.station import create_random_station


def test_create_station(
        client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": "Station Number One"}
    response = client.post(
        f"{settings.API_V1_STR}/stations", headers=superuser_token_headers,
        json=data
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content
    assert "owner_id" in content


def test_read_station(
        client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    station = create_random_station(db)
    response = client.get(
        f"{settings.API_V1_STR}/stations/{station.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    print(content)
    print(station)
    assert content["id"] == str(station.id)
    assert content["name"] == station.name
    assert content["owner_id"] == str(station.owner_id)
