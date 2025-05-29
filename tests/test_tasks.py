import pytest


@pytest.mark.asyncio
async def test_healthcheck(async_client):
    response = await async_client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_task(async_client):
    response = await async_client.post(
        "/tasks", json={"title": "Test Task", "description": "Testing", "priority": 2}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"


@pytest.mark.asyncio
async def test_get_task(async_client):
    response = await async_client.post(
        "/tasks",
        json={"title": "Task to Fetch", "description": "Details", "priority": 1},
    )
    task_id = response.json()["id"]
    get_response = await async_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_update_task(async_client):
    response = await async_client.post(
        "/tasks", json={"title": "To Update", "description": "Status", "priority": 3}
    )
    task_id = response.json()["id"]
    update_response = await async_client.put(f"/tasks/{task_id}?status=completed")
    assert update_response.status_code == 204
    status_check = await async_client.get(f"/tasks/{task_id}")
    assert status_check.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_task(async_client):
    response = await async_client.post(
        "/tasks", json={"title": "Delete Me", "description": "Gone", "priority": 1}
    )
    task_id = response.json()["id"]
    del_response = await async_client.delete(f"/tasks/{task_id}")
    assert del_response.status_code == 204
    confirm = await async_client.get(f"/tasks/{task_id}")
    assert confirm.status_code == 404


@pytest.mark.asyncio
async def test_process_task(async_client):
    response = await async_client.post(
        "/tasks",
        json={"title": "To Process", "description": "Background", "priority": 2},
    )
    task_id = response.json()["id"]
    process_response = await async_client.post(f"/tasks/{task_id}/process")
    assert process_response.status_code == 202
    assert "processing started" in process_response.json()["message"]
