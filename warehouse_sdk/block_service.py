from typing import Optional

from pydantic import BaseModel

from warehouse_sdk import BaseWarehouseService


class BlockModel(BaseModel):
    number: int
    timestamp: int
    hash: Optional[str] = None
    parent_hash: Optional[str] = None
    nonce: Optional[str] = None
    sha3_uncles: Optional[str] = None
    logs_bloom: Optional[str] = None
    transactions_root: Optional[str] = None
    state_root: Optional[str] = None
    receipts_root: Optional[str] = None
    miner: Optional[str] = None
    difficulty: Optional[str] = None
    total_difficulty: Optional[str] = None
    size: Optional[int] = None
    extra_data: Optional[str] = None
    gas_limit: Optional[int] = None
    gas_used: Optional[int] = None
    transaction_count: Optional[int] = None
    base_fee_per_gas: Optional[int] = None


class BlockService(BaseWarehouseService):

    def get_last_indexed_block(self, network: str) -> Optional[list]:
        """
        We are requesting last indexed block from data warehouse
        query:
        https://warehouse.dex.guru/queries/15
        curl -X POST 'https://api.dev.dex.guru/wh/last_block_indexed?api_key=YOUR_API_KEY'
         -H 'Content-Type: application/json' --data '{"parameters": {"network":"canto"}}'
        """
        if network == "eth":
            network = "ethereum"
        return self._make_wh_request('last_block_indexed', {"parameters": {"network": network}})

    def get_indexed_block_by_timestamp(self, network: str, timestamp: int) -> Optional[list]:
        """
        We are requesting block by timestamp from data warehouse
        query
        https://warehouse.dex.guru/queries/167

        curl -X POST 'https://api.dev.dex.guru/wh/block_by_timestamp?api_key=YOUR_API_KEY'
         -H 'Content-Type: application/json' --data '{"parameters": {"timestamp":"1703416371",
         "Network":"ethereum","block_time":"14"}}'

        """
        if network == "eth":
            network = "ethereum"
        return self._make_wh_request('block_by_timestamp', {"parameters": {"timestamp": timestamp,
                                                                           "network": network}})

    def get_block_by_number(self, network: str, block_number: int) -> Optional[list]:
        """
        We are requesting block by number from data warehouse
        query
        https://warehouse.dex.guru/queries/169
        curl -X POST 'https://api.dev.dex.guru/wh/block_by_number?api_key=YOUR_API_KEY'
        -H 'Content-Type: application/json' --data '{"parameters": {"network":"ethereum","number":"1"}}'
        """
        if network == "eth":
            network = "ethereum"
        return self._make_wh_request('block_by_number', {"parameters": {"number": block_number,
                                                                        "network": network}})

    def get_lr_coefficients(self, network: str, training_set_size: int) -> Optional[list]:
        """
        We are requesting linear regression for network from warehouse
        https://warehouse.dex.guru/queries/166

        query curl -X POST 'https://api.dev.dex.guru/wh/block_ts_lr?api_key=YOUR_API_KEY'
        -H 'Content-Type: application/json' --data '{"parameters": {"network":"ethereum","training_set_size":1000000}}'
         -H 'Content-Type: application/json' --data '{"parameters": {"network":"canto"}}'
         we reciewe json like this:
         [{"block_number": 7463340, "block_timestamp": 1703379702, "block_lag": 5}]
        """
        if network == "eth":
            network = "ethereum"
        return self._make_wh_request('block_ts_lr', {"parameters": {"network": network,
                                                                    "training_set_size": training_set_size}})

    def get_block_by_timestamp(self, network: str,
                               timestamp: int) -> Optional[BlockModel]:

        """
        Method either predicts or returns block by timestamp
        :param network:
        :param timestamp:
        :return:
        """
        timestamp = self._transform_timestamp(timestamp)
        last_indexed_block = self.get_last_indexed_block(network)
        if not last_indexed_block:
            return None
        last_indexed_block = last_indexed_block[0]
        if timestamp > last_indexed_block['timestamp']:
            # 10% OF ALL BLOCKS
            training_set_size = round(last_indexed_block['number'] * 0.1)
            lr_coefficients = self.get_lr_coefficients(network, training_set_size)
            if not lr_coefficients:
                return None
            lr_coefficients = lr_coefficients[0]['lr']
            block_number = round((timestamp - lr_coefficients["b"]) // lr_coefficients["k"])
            return BlockModel(number=block_number, timestamp=timestamp)
        else:
            block_by_timestamp = self.get_indexed_block_by_timestamp(network,
                                                                     timestamp)
            if not block_by_timestamp:
                return None
            block_by_timestamp = block_by_timestamp[0]
            return BlockModel(**block_by_timestamp)

    def get_block(self,
                  network: str,
                  block_number: int
                  ) -> Optional[BlockModel]:
        """
        Method either predicts or returns block by number
        :param network:
        :param block_number:
        :return:
        """
        last_indexed_block = self.get_last_indexed_block(network)
        if not last_indexed_block:
            return None
        last_indexed_block = last_indexed_block[0]
        if block_number > last_indexed_block['number']:
            training_set_size = round(last_indexed_block['number'] * 0.1)
            lr_coefficients = self.get_lr_coefficients(network, training_set_size)
            if not lr_coefficients:
                return None
            lr_coefficients = lr_coefficients[0]['lr']
            timestamp = round(lr_coefficients["k"] * block_number + lr_coefficients["b"])
            return BlockModel(number=block_number, timestamp=timestamp)
        else:
            block = self.get_block_by_number(network, block_number)
            if not block:
                return None
            block = block[0]
            return BlockModel(**block)
