import os

# 🔹 프로젝트 기본 경로 (현재 파일 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔹 오디오 파일 경로 (예: audio/01. 조깅.mp3)
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

# 🔹 PDF 생성 경로
PDF_OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pdfs")

# 🔹 JSON 데이터 파일
LESSONS_JSON = os.path.join(BASE_DIR, "lessons.json")

# 🔹 원본 PDF (옵션: make_lessons_json.py에서 사용)
SOURCE_PDF = os.path.join(BASE_DIR, "1분영어_01-30.pdf")

# 폴더 자동 생성 (없으면 만들어줌)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)

# 🔹 기본 상태 로그
if __name__ == "__main__":
    print("✅ config.py 로드 완료")
    print(f"BASE_DIR       : {BASE_DIR}")
    print(f"AUDIO_DIR      : {AUDIO_DIR}")
    print(f"PDF_OUTPUT_DIR : {PDF_OUTPUT_DIR}")
    print(f"LESSONS_JSON   : {LESSONS_JSON}")
