# bitcoin_project/src/main.py

import os
from . import config
from . import data_processing

def main():
    """
    데이터 처리 프로세스를 실행하는 메인 함수입니다.
    1. 설정 파일에서 데이터 경로를 가져옵니다.
    2. 입력 폴더에 있는 모든 TSV 파일을 찾습니다.
    3. 각 TSV 파일을 순차적으로 처리하여 하나의 CSV 파일로 합칩니다.
    """
    print("="*50)
    print("TSV 데이터 처리 프로세스를 시작합니다.")
    print(f"입력 폴더: {config.INPUT_DATA_PATH}")
    print(f"출력 폴더: {config.OUTPUT_DATA_PATH}")
    print("="*50)

    # 최종 결과를 저장할 CSV 파일의 전체 경로를 설정합니다.
    output_csv_full_path = os.path.join(config.OUTPUT_DATA_PATH, config.PROCESSED_DATA_FILENAME)

    # 기존에 생성된 결과 파일이 있다면 삭제하여 매번 새로 생성하도록 합니다.
    if os.path.exists(output_csv_full_path):
        os.remove(output_csv_full_path)
        print(f"기존 결과 파일 ('{config.PROCESSED_DATA_FILENAME}')을 삭제했습니다.")

    # 입력 폴더에서 처리할 TSV 파일 목록을 가져옵니다.
    tsv_files_to_process = data_processing.find_tsv_files(config.INPUT_DATA_PATH)

    if not tsv_files_to_process:
        print("처리할 TSV 파일이 없습니다. 프로세스를 종료합니다.")
        return

    # 각 TSV 파일을 순회하며 처리하고 결과를 하나의 CSV 파일에 추가합니다.
    for tsv_file in tsv_files_to_process:
        data_processing.process_and_append_tsv(tsv_file, output_csv_full_path)

    print("="*50)
    print("모든 TSV 파일 처리가 완료되었습니다.")
    print(f"결과가 다음 파일에 저장되었습니다: {output_csv_full_path}")
    print("="*50)

if __name__ == "__main__":
    main()