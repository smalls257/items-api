"""Tests for the FastAPI project skeleton (issue #12).

Covers:
- The `app` object is importable and is a proper FastAPI instance.
- The app can serve HTTP requests (TestClient works end-to-end).
- Undefined routes return 404 (no phantom routes registered at startup).
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def client() -> TestClient:
    """Return a synchronous TestClient wrapping the FastAPI app."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# App-instance tests (no HTTP needed)
# ---------------------------------------------------------------------------


def test_app_instance_is_fastapi():
    """Happy path: app is a FastAPI instance and can be imported."""
    # Arrange / Act — import already happened at module level
    # Assert
    assert isinstance(app, FastAPI)


def test_app_instance_is_not_none():
    """Edge case / sanity: the module-level `app` object must not be None."""
    assert app is not None


# ---------------------------------------------------------------------------
# HTTP-level tests
# ---------------------------------------------------------------------------


def test_app_serves_requests_happy_path(client: TestClient):
    """Happy path: the TestClient can connect to the app without errors.

    Requesting the OpenAPI schema endpoint is a reliable built-in probe —
    FastAPI always registers /openapi.json unless explicitly disabled.
    """
    # Arrange — client fixture provides a live test client

    # Act
    response = client.get("/openapi.json")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "openapi" in payload  # must be a valid OpenAPI document


def test_app_unknown_route_returns_404(client: TestClient):
    """Edge case: an undefined route must return 404, not 500 or anything else.

    This guards against accidental catch-all routes being registered at init.
    """
    # Arrange
    undefined_path = "/this-route-does-not-exist"

    # Act
    response = client.get(undefined_path)

    # Assert
    assert response.status_code == 404


def test_app_docs_endpoint_accessible(client: TestClient):
    """Happy path: the built-in /docs (Swagger UI) endpoint is reachable."""
    # Act
    response = client.get("/docs")

    # Assert
    assert response.status_code == 200


def test_app_has_no_custom_routes_registered():
    """Edge case: the skeleton should have zero application-defined routes.

    FastAPI always adds a few internal routes (/openapi.json, /docs, /redoc).
    We verify that no *additional* routes beyond those built-ins exist yet,
    confirming the skeleton is truly bare.
    """
    # Arrange
    builtin_paths = {"/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect"}

    # Act — collect all route paths from the app's router
    registered_paths = {
        route.path
        for route in app.routes
        if hasattr(route, "path")
    }

    custom_paths = registered_paths - builtin_paths

    # Assert
    assert custom_paths == set(), (
        f"Expected no custom routes, but found: {custom_paths}"
    )
