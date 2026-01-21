# bitcoin_project/src/analysis.py

import os
import pandas as pd
from . import config
from .rpc_client import BitcoinRPC

def analyze_whale_transactions():
    """
    처리된 '고래' 트랜잭션 목록을 읽고, 각 트랜잭션의 상세 정보를
    RPC 클라이언트(시뮬레이션 또는 실제)를 통해 가져와 분석합니다.
    """
    print("="*50)
    print("Starting Whale Transaction Analysis...")
    print("="*50)

    # 1. 처리된 데이터 파일을 읽습니다.
    try:
        processed_data_path = os.path.join(config.OUTPUT_DATA_PATH, config.PROCESSED_DATA_FILENAME)
        df_transactions = pd.read_csv(processed_data_path)
        print(f"Loaded {len(df_transactions)} transactions from '{config.PROCESSED_DATA_FILENAME}'.")
    except FileNotFoundError:
        print(f"Error: Processed data file not found at '{processed_data_path}'")
        print("Please run 'python -m src.main' first to generate the data.")
        return

    # 2. RPC 클라이언트를 초기화합니다.
    rpc = BitcoinRPC()

    # 3. 각 트랜잭션을 순회하며 분석합니다.
    # 샘플 분석을 위해 상위 5개의 트랜잭션만 처리합니다.
    for index, row in df_transactions.head(5).iterrows():
        txid = row['hash']
        print(f"\n--- Analyzing Transaction: {txid[:15]}... ---")

        # 4. RPC를 통해 트랜잭션 상세 정보를 가져옵니다.
        tx_data = rpc.get_raw_transaction(txid)

        if not tx_data:
            print("Could not retrieve transaction data.")
            continue

        # 5. 간단한 분석을 수행하고 결과를 출력합니다.
        # (향후 이 부분에 더 복잡한 '고래 지갑 분류' 로직 추가 가능)
        total_output_value = sum(vout.get('value', 0) for vout in tx_data.get('vout', []))
        num_outputs = len(tx_data.get('vout', []))
        
        print(f"  - Total Output Value: {total_output_value:.4f} BTC")
        print(f"  - Number of Outputs: {num_outputs}")
        print("  - Output Details:")
        for vout in tx_data.get('vout', []):
            address = vout.get('scriptPubKey', {}).get('addresses', ['N/A'])[0]
            value = vout.get('value', 'N/A')
            print(f"    -> Address: {address}, Value: {value}")
    
    print("\n" + "="*50)
    print("Whale Transaction Analysis Finished.")
    print("="*50)


if __name__ == '__main__':
    analyze_whale_transactions()
