# bitcoin_project/src/config.py

import os

# 프로젝트의 루트 디렉토리 경로를 설정합니다.
# 이 파일 (config.py)의 상위 디렉토리(src)의 상위 디렉토리(bitcoin_project) 입니다.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 데이터 입출력 경로를 설정합니다.
# 입력 데이터는 'bitcoin_project/data' 폴더에 있다고 가정합니다.
# 출력 데이터는 'bitcoin_project/data/output' 폴더에 저장됩니다.
INPUT_DATA_PATH = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'output')

# 처리된 데이터를 저장할 CSV 파일의 이름을 정의합니다.
PROCESSED_DATA_FILENAME = "processed_transactions.csv"

# 출력 폴더가 존재하지 않으면 생성합니다.
os.makedirs(OUTPUT_DATA_PATH, exist_ok=True)

# RPC 연결 설정
# SIMULATION_MODE가 True이면 실제 RPC 서버에 연결하지 않고 가상 데이터를 반환합니다.
SIMULATION_MODE = True
RPC_HOST = "127.0.0.1"
RPC_PORT = 8332
RPC_USER = "your_rpc_user"  # 실제 운영 시 이 값을 변경하세요.
RPC_PASSWORD = "your_rpc_password" # 실제 운영 시 이 값을 변경하세요.