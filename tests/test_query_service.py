import pytest
from warehouse_sdk.query_service import QueryService


class TestQueryService:

    @pytest.fixture
    def query_service(self, mocker):
        # Setup QueryService with a mock for _make_wh_request
        service = QueryService(warehouse_url="http://fakeurl.com", warehouse_api_key="fakekey")
        mocker.patch.object(service, '_make_wh_request')
        return service

    def test_execute_query_success(self, query_service):
        # Mocking successful warehouse response
        query_service._make_wh_request.return_value = [{"key1": "value1", "key2": "value2"}]

        response = query_service.execute_query("test_query_id", {"param1": "value1"})

        assert response is not None
        assert response.count == 1
        assert "key1" in response.data[0]
        assert "key2" in response.data[0]

    def test_execute_query_no_result(self, query_service):
        # Mocking no result from warehouse
        query_service._make_wh_request.return_value = None

        response = query_service.execute_query("test_query_id", {"param1": "value1"})

        assert response is None

    def test_execute_query_with_specific_query_result(self, query_service):
        # Mocking successful response for a specific query
        query_service._make_wh_request.return_value = [{"specific_key": "specific_value"}]

        response = query_service.get_specific_query_result(123)

        assert response is not None
        assert response.count == 1
        assert "specific_key" in response.data[0]

    # You can add more tests here for other scenarios and methods
