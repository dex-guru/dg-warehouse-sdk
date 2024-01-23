# Example of using of warehouse SDK to query Query results,
# Here we are quering: https://warehouse.dex.guru/queries/56 (Networks Supported)

from warehouse_sdk.query_service import QueryService


def query_service():
    # Setup QueryService
    service = QueryService(warehouse_url="https://api.dev.dex.guru/wh",
                           warehouse_api_key="3aRnEoATe5VSgakGxlZUggO2vZnnhvXUJJplHzy3")
    return service


if __name__ == "__main__":
    query_name = 'networks_supported'
    parameters = {}
    response = query_service().execute_query("networks_supported",
                                            parameters)

    print(f"Response for {query_name} with {query_name}")
    for key, value in response:
        print(f"{key}: {value}")
