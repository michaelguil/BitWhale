# Bitcoin 고래 트랜잭션 분석 (Bitcoin Whale Transaction Analysis)

## 1. 프로젝트 개요 (Overview)

이 프로젝트는 대규모 비트코인 트랜잭션(일명 '고래')을 식별하고, 해당 트랜잭션의 상세 정보를 분석하여 시장의 움직임을 파악하는 것을 목표로 합니다.

현재 버전(v1.0)은 로컬 데이터를 처리하고 Bitcoin Core RPC와의 통신을 시뮬레이션하여 전체 분석 파이프라인의 개념을 증명(Proof-of-Concept)하는 단계입니다.

## 2. 주요 기능 (Features)

- **데이터 전처리:** `blockchair.com`에서 다운로드한 대용량 TSV 트랜잭션 데이터를 읽어, 10 BTC 이상의 '고래' 트랜잭션만 필터링하고 CSV 파일로 저장합니다.
- **RPC 통신 시뮬레이션:** 실제 Bitcoin Core 노드를 실행하지 않고도 프로젝트를 테스트할 수 있도록, RPC 통신을 모방하는 **시뮬레이션 모드**를 지원합니다.
- **기본 트랜잭션 분석:** 필터링된 트랜잭션의 상세 정보(총 출력 값, 출력 주소 및 금액 등)를 조회하고 간단한 분석 결과를 출력합니다.

## 3. 프로젝트 구조 (Project Structure)

```
bitcoin_project/
├── data/
│   ├── blockchair_bitcoin_transactions_20240101.tsv  # 샘플 데이터
│   ├── ...
│   └── output/
│       └── processed_transactions.csv              # 전처리된 결과
├── notebooks/
│   └── bitcoincore_original.ipynb                  # 초기 아이디어 스케치용 노트북
├── src/
│   ├── config.py             # 설정 변수 (경로, 시뮬레이션 모드 등)
│   ├── data_processing.py    # TSV 데이터 전처리 로직
│   ├── main.py               # 데이터 전처리 실행 스크립트
│   ├── rpc_client.py         # Bitcoin Core RPC 클라이언트 (시뮬레이션 기능 포함)
│   └── analysis.py           # 최종 분석 실행 스크립트
├── .gitignore                # Git 버전 관리 제외 파일 목록
├── requirements.txt          # 프로젝트 필요 라이브러리
└── README.md                 # 프로젝트 설명 파일
```

## 4. 설치 및 실행 방법 (Setup & How to Run)

### 4.1. 환경 설정 (Setup)

1.  **프로젝트 클론:**
    ```bash
    git clone <repository_url>
    cd bitcoin_project
    ```
2.  **필요 라이브러리 설치:**
    ```bash
    pip install -r requirements.txt
    ```

### 4.2. 실행 순서 (How to Run)

1.  **데이터 준비:** `blockchair.com` 등에서 트랜잭션 데이터(`.tsv`)를 다운로드하여 `data/` 폴더에 위치시킵니다. (샘플 데이터가 이미 포함되어 있습니다.)

2.  **데이터 전처리 실행:**
    아래 명령어를 실행하여 `data/` 폴더의 TSV 파일들을 전처리하고 `data/output/processed_transactions.csv` 파일을 생성합니다.
    ```bash
    python -m src.main
    ```

3.  **분석 스크립트 실행:**
    전처리된 데이터를 바탕으로 (시뮬레이션) RPC 통신을 통해 트랜잭션 분석을 시작합니다.
    ```bash
    python -m src.analysis
    ```

## 5. 시뮬레이션 모드 (Simulation Mode)

이 프로젝트는 실제 Bitcoin Core 노드 없이도 핵심 로직을 실행하고 테스트할 수 있도록 시뮬레이션 모드를 제공합니다.

-   **위치:** `src/config.py` 파일 내 `SIMULATION_MODE` 변수
-   `SIMULATION_MODE = True` (기본값): 실제 RPC 서버에 연결하지 않고, `src/rpc_client.py`에 미리 정의된 가상의 샘플 데이터를 반환합니다.
-   `SIMULATION_MODE = False`: 실제 Bitcoin Core 노드에 연결을 시도합니다. 이 경우, `config.py` 파일의 `RPC_HOST`, `RPC_PORT`, `RPC_USER`, `RPC_PASSWORD`를 실제 환경에 맞게 수정해야 합니다.

## 6. 향후 계획 (Future Work - v2.0)

- **Blockchair API 연동:** 수동으로 데이터를 다운로드하는 대신, GitHub 학생 개발자 팩으로 제공되는 Blockchair API를 활용하여 데이터를 실시간으로 가져오는 기능을 구현할 예정입니다.
- **고급 분석 기능:** 단순 정보 조회을 넘어, 트랜잭션 흐름 추적, 고래 지갑 유형 분류 등 더 심도 있는 분석 모델을 추가할 계획입니다.
