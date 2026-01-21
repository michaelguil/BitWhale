# bitcoin_project/src/rpc_client.py

import os
import pandas as pd
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from . import config

class BitcoinRPC:
    """
    Bitcoin Core RPC와 통신하기 위한 클라이언트 클래스입니다.
    시뮬레이션 모드를 지원하여, 실제 노드 없이도 개발 및 테스트가 가능합니다.
    """
    def __init__(self):
        self.simulation_mode = config.SIMULATION_MODE
        if not self.simulation_mode:
            try:
                # 실제 모드: RPC 서버에 연결
                self.rpc_connection = self._get_rpc_connection()
                # 연결 테스트
                self.rpc_connection.getblockchaininfo()
                print("Successfully connected to Bitcoin Core RPC.")
            except Exception as e:
                print(f"Error connecting to Bitcoin Core RPC: {e}")
                print("Switching to simulation mode.")
                self.simulation_mode = True
        
        if self.simulation_mode:
            print("Running in SIMULATION MODE. No real RPC calls will be made.")

    def _get_rpc_connection(self):
        """RPC 연결 객체를 생성하고 반환합니다."""
        rpc_url = f"http://{config.RPC_USER}:{config.RPC_PASSWORD}@{config.RPC_HOST}:{config.RPC_PORT}"
        return AuthServiceProxy(rpc_url)

    def get_raw_transaction(self, txid, verbose=True):
        """
        주어진 트랜잭션 ID(txid)에 대한 상세 정보를 반환합니다.
        시뮬레이션 모드에서는 가상의 데이터를 반환합니다.
        """
        if self.simulation_mode:
            # 시뮬레이션 모드: 가상의 트랜잭션 데이터 반환
            print(f"SIMULATION: Fetching data for txid: {txid[:10]}...")
            return self._get_mock_transaction_data(txid)
        else:
            # 실제 모드: 실제 RPC 호출
            try:
                return self.rpc_connection.getrawtransaction(txid, verbose)
            except JSONRPCException as e:
                print(f"Error fetching transaction {txid}: {e}")
                return None

    def _get_mock_transaction_data(self, txid):
        """
        시뮬레이션 모드에서 사용할 가상의 트랜잭션 데이터를 생성합니다.
        실제 RPC 응답과 유사한 구조를 가집니다.
        """
        # 간단한 해시 함수를 사용하여 txid에 따라 약간 다른 값을 반환
        value_seed = int(txid[:5], 16) % 1000
        
        return {
            "txid": txid,
            "hash": txid,
            "version": 1,
            "size": 250,
            "vsize": 250,
            "weight": 1000,
            "locktime": 0,
            "vin": [
                {
                    "txid": "a1" * 32,
                    "vout": 0,
                    "scriptSig": {"asm": "...", "hex": "..."},
                    "sequence": 4294967295
                }
            ],
            "vout": [
                {
                    "value": 10.0 + (value_seed / 100.0),
                    "n": 0,
                    "scriptPubKey": {
                        "asm": "OP_DUP OP_HASH160 ... OP_EQUALVERIFY OP_CHECKSIG",
                        "hex": "...",
                        "reqSigs": 1,
                        "type": "pubkeyhash",
                        "addresses": ["1MockAddress1_xxxxxxxxxxxxxxxxx"]
                    }
                },
                {
                    "value": 5.0 - (value_seed / 200.0),
                    "n": 1,
                    "scriptPubKey": {
                        "asm": "OP_DUP OP_HASH160 ... OP_EQUALVERIFY OP_CHECKSIG",
                        "hex": "...",
                        "reqSigs": 1,
                        "type": "pubkeyhash",
                        "addresses": ["1MockAddress2_yyyyyyyyyyyyyyyyy"]
                    }
                }
            ],
            "hex": "...",
            "blockhash": "0000000000000000000aaaaabbbbbbcccccddddddeeeeee",
            "confirmations": 123,
            "time": 1672531200,
            "blocktime": 1672531200
        }

if __name__ == '__main__':
    # 이 파일이 직접 실행될 때 간단한 테스트를 수행합니다.
    rpc = BitcoinRPC()
    
    # 처리된 데이터 파일에서 샘플 txid를 읽어옵니다.
    try:
        processed_data_path = os.path.join(config.OUTPUT_DATA_PATH, config.PROCESSED_DATA_FILENAME)
        df = pd.read_csv(processed_data_path)
        sample_txid = df['hash'].iloc[0]
        
        print(f"\n--- Testing with sample txid: {sample_txid} ---")
        transaction_data = rpc.get_raw_transaction(sample_txid)
        
        if transaction_data:
            print("\n--- Received Transaction Data ---")
            print(f"Transaction ID: {transaction_data.get('txid')}")
            print(f"Confirmations: {transaction_data.get('confirmations')}")
            print("Outputs (vout):")
            for vout in transaction_data.get('vout', []):
                print(f"  - Address: {vout.get('scriptPubKey', {}).get('addresses', ['N/A'])[0]}, Value: {vout.get('value')}")
            print("---------------------------------")

    except (FileNotFoundError, IndexError) as e:
        print(f"\nCould not read sample txid from processed data file: {e}")
        print("Testing with a dummy txid instead.")
        
        sample_txid = "f" * 64
        print(f"\n--- Testing with dummy txid: {sample_txid} ---")
        transaction_data = rpc.get_raw_transaction(sample_txid)
        if transaction_data:
            print("\n--- Received Transaction Data ---")
            print(f"Transaction ID: {transaction_data.get('txid')}")
            print("---------------------------------")
