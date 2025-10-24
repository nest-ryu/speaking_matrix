import os
import json
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from config import AUDIO_DIR, PDF_OUTPUT_DIR, LESSONS_JSON

# ----------------------------------------------------
# 기본 설정
# ----------------------------------------------------
st.set_page_config(page_title="1분 영어 말하기", page_icon="🗣", layout="wide")
st.title("🗣 1분 영어 말하기 | Speaking Matrix")


# ----------------------------------------------------
# 데이터 불러오기
# ----------------------------------------------------
def load_lessons():
    if os.path.exists(LESSONS_JSON):
        with open(LESSONS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error("❌ lessons.json 파일을 찾을 수 없습니다.")
        return []


lessons = load_lessons()
if not lessons:
    st.stop()


# ----------------------------------------------------
# 사이드바
# ----------------------------------------------------
lesson_list = [f"{l['lesson']:02d}. {l['title']}" for l in lessons]
selected = st.sidebar.selectbox("레슨 선택", lesson_list)
lesson = lessons[lesson_list.index(selected)]


# ----------------------------------------------------
# 본문 표시 (줄바꿈 포함)
# ----------------------------------------------------
st.header(f"Lesson {lesson['lesson']:02d} — {lesson['title']}")

# 🗣 영어 문장
st.subheader("🗣 영어 문장 | English Sentences")
english_lines = lesson["english"].split("\n")
st.markdown("<br>".join(english_lines), unsafe_allow_html=True)

# 🇰🇷 한국어 번역
st.subheader("🇰🇷 한국어 번역 | Korean Translation")
korean_lines = lesson["korean"].split("\n")
st.markdown("<br>".join(korean_lines), unsafe_allow_html=True)

# 💡 문법·표현 포인트
st.subheader("💡 문법·표현 포인트 | Grammar & Expressions")
for g in lesson.get("grammar", []):
    st.markdown(f"- {g}")

# 📝 말하기 연습
st.subheader("📝 말하기 연습 | Speaking Practice")
for s in lesson.get("practice", []):
    st.markdown(f"- {s}")


# ----------------------------------------------------
# 오디오 파일
# ----------------------------------------------------
# 파일명 형식: "01. 조깅.mp3"
num_str = str(lesson["lesson"]).zfill(2)
try:
    korean_title = lesson["title"].split("|")[1].strip()
except IndexError:
    korean_title = lesson["title"].strip()

audio_filename = f"{num_str}. {korean_title}.mp3"
audio_path = os.path.join(AUDIO_DIR, audio_filename)

if os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.warning(f"🎧 오디오 파일을 찾을 수 없습니다: {audio_filename}")


# ----------------------------------------------------
# PDF 생성 함수 (한글 폰트 적용)
# ----------------------------------------------------
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import ParagraphStyle

def create_pdf(lesson):
    # ✅ 한글 폰트 등록
    pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))

    # ✅ 스타일 세트업 (모든 텍스트에 한글 폰트 적용)
    styles = getSampleStyleSheet()
    for style_name in styles.byName:
        styles[style_name].fontName = 'HYSMyeongJo-Medium'

    # 커스텀 스타일 정의
    styles.add(ParagraphStyle(name='KTitle',
                              fontName='HYSMyeongJo-Medium',
                              fontSize=16,
                              leading=20,
                              alignment=1))  # 중앙정렬

    pdf_path = os.path.join(PDF_OUTPUT_DIR, f"Lesson_{lesson['lesson']:02d}.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50)

    story = []

    def add_text(text, style="BodyText", space=8):
        p = Paragraph(text, styles[style])
        story.append(p)
        story.append(Spacer(1, space))

    # 제목
    add_text(f"<b>Lesson {lesson['lesson']:02d} — {lesson['title']}</b>", "KTitle", 14)

    # 영어 문장
    add_text("<b>🗣 영어 문장 | English Sentences</b>")
    add_text(lesson["english"].replace("\n", "<br/>"))

    # 한국어 번역
    add_text("<b>🇰🇷 한국어 번역 | Korean Translation</b>")
    add_text(f"<font color='gray'>{lesson['korean'].replace('\n', '<br/>')}</font>")

    # 문법·표현 포인트
    add_text("<b>💡 문법·표현 포인트 | Grammar & Expressions</b>")
    for g in lesson.get("grammar", []):
        add_text(f"- {g}")

    # 말하기 연습
    add_text("<b>📝 말하기 연습 | Speaking Practice</b>")
    for s in lesson.get("practice", []):
        add_text(f"- {s}")

    doc.build(story)
    return pdf_path



# ----------------------------------------------------
# PDF 생성 및 다운로드
# ----------------------------------------------------
if st.button("📄 학습지 PDF 생성 및 다운로드"):
    pdf_file = create_pdf(lesson)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥 PDF 다운로드",
            data=f,
            file_name=os.path.basename(pdf_file),
            mime="application/pdf"
        )
