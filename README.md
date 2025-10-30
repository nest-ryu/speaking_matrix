

# 🗣 1분 영어 말하기 (Speaking Matrix)

**1분 영어 말하기** 프로젝트는 30개의 짧은 영어 회화 레슨을
텍스트·오디오·PDF 학습지 형태로 제공하는 간단한 Streamlit 앱입니다.  
로컬 PC나 Pydroid3에서 바로 실행할 수 있습니다.

https://speakingmatrix-1minute.streamlit.app/


## 📁 폴더 구조

speaking_matrix/
│
├── make_lessons_json.py # PDF → lessons.json 자동 변환 스크립트
├── speaking_matrix.py # Streamlit 메인 앱
├── config.py # 경로 설정
├── requirements.txt # 필요한 패키지 목록
│
└── audio/ # 오디오 파일 폴더 (예: 1. Jogging.mp3 … 30. Reflection.mp3)



## ⚙️ 주요 기능

| 📄 **make_lessons_json.py** | `1분영어_01-30.pdf` → `lessons.json` 자동 생성 |
| 🗣 **speaking_matrix.py** | JSON 기반 문장·번역·문법·연습·오디오 표시 |
| 📘 **PDF 생성**  | 각 Lesson 학습지 PDF를 즉시 생성하여 다운로드 가능 |
| 🎧 **오디오 지원** | `audio/` 폴더의 `N. 제목.mp3` 형식 파일 자동 인식 |


## 🚀 실행 방법

### 1) 사전 준비
- Python 3.9+
- 프로젝트 폴더 `speaking_matrix/` 생성
- `1분영어_01-30.pdf` 를 같은 폴더에 복사
- 오디오 30개 파일을 `audio/` 폴더에 넣기 (`1. 제목.mp3` … `30. 제목.mp3`)


### 2) 패키지 설치
pip install -r requirements.txt

3) PDF → JSON 변환
python make_lessons_json.py
➡ lessons.json 파일이 자동 생성됩니다.

4) Streamlit 앱 실행
streamlit run speaking_matrix.py
➡ 브라우저에서 Lesson 1 ~ 30을 텍스트·오디오·PDF로 학습할 수 있습니다.


🧩 추가 정보

PDF 생성 시 reportlab을 사용하며, 한글 폰트 깨짐 방지를 위해 기본 폰트는 HYSMyeongJo-Medium을 권장합니다.
audio/ 폴더 안에 오디오 파일이 없을 경우, 앱에서 자동으로 경고 메시지를 표시합니다.
make_lessons_json.py 실행 후 생성된 lessons.json은 speaking_matrix.py에서 자동으로 불러옵니다.



