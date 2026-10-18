def test_health_example(api_client):
    """Example contract: GET /health returns 200; adapt to the project contract."""
    resp = api_client.request("GET", "/health")
    assert resp.status_code == 200
