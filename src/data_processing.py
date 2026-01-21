# bitcoin_project/src/data_processing.py

import os
import pandas as pd
from . import config

def find_tsv_files(folder_path):
    """
    지정된 폴더에서 .tsv 확장자를 가진 모든 파일의 전체 경로 리스트를 반환합니다.

    Args:
        folder_path (str): .tsv 파일을 찾을 폴더의 경로입니다.

    Returns:
        list: .tsv 파일들의 전체 경로가 담긴 리스트입니다.
    """
    try:
        tsv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.tsv')]
        if not tsv_files:
            print(f"경고: '{folder_path}' 폴더에 TSV 파일이 없습니다.")
        return tsv_files
    except FileNotFoundError:
        print(f"오류: '{folder_path}' 폴더를 찾을 수 없습니다.")
        return []

def process_and_append_tsv(tsv_file_path, output_csv_path):
    """
    하나의 TSV 파일을 읽어 처리하고, 결과를 지정된 CSV 파일에 추가합니다.

    - 10 BTC 이상인 트랜잭션만 필터링합니다.
    - 'hash'와 'time' 열만 선택합니다.
    - 처리된 데이터를 CSV 파일에 추가합니다.

    Args:
        tsv_file_path (str): 처리할 TSV 파일의 경로입니다.
        output_csv_path (str): 결과를 저장할 CSV 파일의 경로입니다.
    """
    try:
        df = pd.read_csv(tsv_file_path, sep='\t')

        if 'input_total' not in df.columns:
            print(f"파일에 'input_total' 컬럼이 없어 건너뜁니다: {os.path.basename(tsv_file_path)}")
            return

        # Satoshis 단위를 BTC로 변환합니다. (1 BTC = 10^8 Satoshis)
        df['input_total'] = pd.to_numeric(df['input_total'], errors='coerce') / 1e8

        # 10 BTC 이상인 트랜잭션만 필터링합니다.
        df_filtered = df[df['input_total'] >= 10].copy()

        # 필요한 'hash', 'time' 컬럼만 선택합니다.
        if 'hash' in df_filtered.columns and 'time' in df_filtered.columns:
            df_final = df_filtered[['hash', 'time']]
        else:
            print(f"파일에 'hash' 또는 'time' 컬럼이 없어 건너뜁니다: {os.path.basename(tsv_file_path)}")
            return

        # CSV 파일에 데이터를 추가합니다. 파일이 없으면 새로 만들고, 있으면 이어서 씁니다.
        if not os.path.exists(output_csv_path):
            df_final.to_csv(output_csv_path, index=False, mode='w', encoding='utf-8')
        else:
            df_final.to_csv(output_csv_path, index=False, mode='a', header=False, encoding='utf-8')
            
        print(f"처리 완료 및 추가: {os.path.basename(tsv_file_path)}")

    except Exception as e:
        print(f"'{os.path.basename(tsv_file_path)}' 파일 처리 중 오류 발생: {e}")
