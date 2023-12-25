from time import sleep
from typing import Optional

import requests


class BaseWarehouseService:
    def __init__(self, warehouse_url: str, warehouse_api_key: str):
        self._warehouse_url = warehouse_url
        self._warehouse_api_key = warehouse_api_key

    def _make_wh_request(self, query: str, parameters: dict, retry: int = 1) -> Optional[dict]:
        url = f'{self._warehouse_url}/{query}?api_key={self._warehouse_api_key}'
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(parameters))
            if response.status_code == 200:
                response_json = response.json()
                if response_json:
                    if response_json[0].get('job'):
                        if retry:
                            # retry as warehouse working on the job, there is no cached.
                            sleep(1)
                            return self._make_wh_request(query=query, parameters=parameters, retry=0)
                        else:
                            return None
                    return response_json
                else:
                    return None
            else:
                return None
        except Exception as e:
            return None

    @staticmethod
    def _transform_timestamp(v: int):
        # Check if timestamp is in milliseconds (assuming it's longer than 10 characters)
        if len(str(v)) > 10:
            v = round(v / 1000)
        return v
