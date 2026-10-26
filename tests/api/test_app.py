"""Тести конфігурації застосунку: маршрути, OpenAPI, middleware."""

import re

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from core.middleware import TimingAndLoggingMiddleware
from main import app

EXPECTED_PATHS = {
    "/students/",
    "/students/{student_id}",
    "/teachers/",
    "/teachers/{teacher_id}",
    "/courses/",
    "/courses/{course_id}",
    "/tasks/",
    "/tasks/{task_id}",
    "/schedules/",
    "/schedules/{schedule_id}",
    "/register",
    "/login",
    "/me",
}


def test_all_routers_are_registered():
    paths = set(app.openapi()["paths"])

    assert paths == EXPECTED_PATHS


async def test_openapi_endpoint_responds(client):
    response = await client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "My FastAPI Project"


async def test_timing_middleware_sets_header_and_logs(caplog):
    """Middleware сама по собі працює — перевіряємо окремим застосунком."""

    test_app = FastAPI()
    test_app.add_middleware(TimingAndLoggingMiddleware)

    @test_app.get("/ping")
    async def ping():
        return {"ok": True}

    transport = ASGITransport(app=test_app)
    with caplog.at_level("INFO", logger="app.access"):
        async with AsyncClient(transport=transport, base_url="http://test") as http_client:
            response = await http_client.get("/ping")

    assert response.status_code == 200
    assert re.fullmatch(r"\d+\.\d{4}s", response.headers["X-Process-Time"])
    assert "GET /ping" in caplog.text


async def test_application_adds_process_time_header(client):
    response = await client.get("/students/")

    assert "X-Process-Time" in response.headers


def test_openapi_url_is_versioned():
    assert app.openapi_url == "/api/v1/openapi.json"
