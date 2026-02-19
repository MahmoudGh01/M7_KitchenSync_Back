"""
Integration tests for API endpoints.
"""

import pytest


@pytest.mark.integration
class TestAuthEndpoints:
    """Test authentication API endpoints."""

    def test_register_success(self, client, sample_kitchen):
        """Test successful user registration."""
        response = client.post(
            "/auth/register",
            json={
                "display_name": "NewUser",
                "kitchen_code": sample_kitchen.code,
                "password": "Strong#123",
            },
        )
        assert response.status_code == 201
        data = response.get_json()
        assert "user" in data
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["display_name"] == "NewUser"

    def test_register_missing_fields(self, client):
        """Test registration with missing fields."""
        response = client.post(
            "/auth/register",
            json={"display_name": "Test"},
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data["code"] == "missing_fields"

    def test_register_weak_password(self, client, sample_kitchen):
        """Test registration with weak password."""
        response = client.post(
            "/auth/register",
            json={
                "display_name": "Test",
                "kitchen_code": sample_kitchen.code,
                "password": "weak",
            },
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data["code"] == "validation_error"

    def test_login_success(self, client, sample_user, sample_kitchen):
        """Test successful login."""
        response = client.post(
            "/auth/login",
            json={
                "display_name": sample_user.display_name,
                "kitchen_code": sample_kitchen.code,
                "password": "Test#123",
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "user" in data
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_wrong_password(self, client, sample_user, sample_kitchen):
        """Test login with wrong password."""
        response = client.post(
            "/auth/login",
            json={
                "display_name": sample_user.display_name,
                "kitchen_code": sample_kitchen.code,
                "password": "WrongPassword",
            },
        )
        assert response.status_code == 401

    def test_me_endpoint(self, client, auth_headers):
        """Test getting current user."""
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "user" in data

    def test_me_endpoint_unauthorized(self, client):
        """Test getting current user without auth."""
        response = client.get("/auth/me")
        assert response.status_code == 401


@pytest.mark.integration
class TestKitchenEndpoints:
    """Test kitchen API endpoints."""

    def test_create_kitchen(self, client):
        """Test creating a kitchen."""
        response = client.post("/kitchens", json={"name": "New Kitchen"})
        assert response.status_code == 201
        data = response.get_json()
        assert "kitchen" in data
        assert data["kitchen"]["name"] == "New Kitchen"
        assert len(data["kitchen"]["code"]) == 6

    def test_get_all_kitchens(self, client, sample_kitchen):
        """Test getting all kitchens."""
        response = client.get("/kitchens")
        assert response.status_code == 200
        data = response.get_json()
        assert "kitchens" in data
        assert len(data["kitchens"]) >= 1

    def test_get_kitchen_by_id(self, client, sample_kitchen):
        """Test getting kitchen by ID."""
        response = client.get(f"/kitchens/{sample_kitchen.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["kitchen"]["id"] == sample_kitchen.id

    def test_get_kitchen_by_code(self, client, sample_kitchen):
        """Test getting kitchen by code."""
        response = client.get(f"/kitchens/code/{sample_kitchen.code}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["kitchen"]["code"] == sample_kitchen.code


@pytest.mark.integration
class TestItemEndpoints:
    """Test item API endpoints."""

    def test_create_item(self, client, auth_headers, sample_kitchen):
        """Test creating an item."""
        response = client.post(
            "/items",
            headers=auth_headers,
            json={
                "name": "Test Item",
                "kitchen_id": sample_kitchen.id,
                "category": "Food",
            },
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["item"]["name"] == "Test Item"

    def test_create_item_unauthorized(self, client, sample_kitchen):
        """Test creating item without auth."""
        response = client.post(
            "/items",
            json={"name": "Test", "kitchen_id": sample_kitchen.id},
        )
        assert response.status_code == 401

    def test_get_items_by_kitchen(self, client, auth_headers, sample_kitchen):
        """Test getting items by kitchen."""
        response = client.get(
            f"/items?kitchen_id={sample_kitchen.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "items" in data

    def test_update_item_quantity(self, client, auth_headers, sample_item):
        """Test updating item quantity."""
        response = client.patch(
            f"/items/{sample_item.id}/quantity",
            headers=auth_headers,
            json={"quantity_percent": 50.0},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["item"]["quantity_percent"] == 50.0


@pytest.mark.integration
class TestRestockLogEndpoints:
    """Test restock log API endpoints."""

    def test_create_restock_log(self, client, auth_headers, sample_item):
        """Test creating a restock log."""
        response = client.post(
            "/restocks",
            headers=auth_headers,
            json={"item_id": sample_item.id},
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["log"]["item_id"] == sample_item.id

    def test_get_restock_logs_by_item(self, client, auth_headers, sample_item):
        """Test getting restock logs by item."""
        response = client.get(
            f"/restocks?item_id={sample_item.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "logs" in data


@pytest.mark.integration
class TestConsumptionLogEndpoints:
    """Test consumption log API endpoints."""

    def test_create_consumption_log(self, client, auth_headers, sample_item):
        """Test creating a consumption log."""
        response = client.post(
            "/consumptions",
            headers=auth_headers,
            json={"item_id": sample_item.id, "percent_used": 25.0},
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["log"]["percent_used"] == 25.0

    def test_create_consumption_log_invalid_percent(self, client, auth_headers, sample_item):
        """Test creating consumption log with invalid percent."""
        response = client.post(
            "/consumptions",
            headers=auth_headers,
            json={"item_id": sample_item.id, "percent_used": 150.0},
        )
        assert response.status_code == 400

    def test_get_consumption_logs_by_kitchen(self, client, auth_headers, sample_kitchen):
        """Test getting consumption logs by kitchen."""
        response = client.get(
            f"/consumptions?kitchen_id={sample_kitchen.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "logs" in data
