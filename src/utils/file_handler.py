import os

def load_tsv_files_from_folder(folder_path):
    """
    주어진 폴더 경로에서 .tsv 확장자를 가진 모든 파일의 리스트를 반환합니다.
    """
    if not os.path.isdir(folder_path):
        print(f"오류: 폴더를 찾을 수 없습니다 - {folder_path}")
        return []
    
    tsv_files = [f for f in os.listdir(folder_path) if f.endswith('.tsv')]
    return tsv_files