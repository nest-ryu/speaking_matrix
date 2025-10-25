import os
import json
import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from config import AUDIO_DIR, LESSONS_JSON


# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(page_title="1분 영어 말하기 | Speaking Matrix", page_icon="🗣", layout="wide")
st.title("🗣 1분 영어 말하기 | Speaking Matrix")
st.markdown("🔹 Lesson 번호를 입력하거나 ⏮⏭ 버튼으로 이동하세요.")


# ---------------------------
# 데이터 로드
# ---------------------------
def load_lessons():
    if os.path.exists(LESSONS_JSON):
        with open(LESSONS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    st.error("❌ lessons.json 파일을 찾을 수 없습니다.")
    return []

lessons = load_lessons()
if not lessons:
    st.stop()


# ---------------------------
# 세션 상태
# ---------------------------
if "lesson_index" not in st.session_state:
    st.session_state.lesson_index = 0
if "lesson_query" not in st.session_state:
    # 입력창 기본은 항상 공백
    st.session_state.lesson_query = ""


# ---------------------------
# 입력 콜백: Enter 시 이동 + 입력창 비우기
# ---------------------------
def _on_enter():
    raw = st.session_state.lesson_query.strip().upper().replace("LESSON", "").strip()
    if raw.isdigit():
        n = int(raw)
        if 1 <= n <= len(lessons):
            st.session_state.lesson_index = n - 1
    # 항상 비워서 공백 유지
    st.session_state.lesson_query = ""


# ---------------------------
# Lesson 번호 입력창 (항상 공백 시작, Enter로 이동)
# ---------------------------
st.text_input(
    "Lesson 번호 입력 (예: 5 또는 005)",
    key="lesson_query",
    placeholder="번호 입력 후 Enter",
    on_change=_on_enter,  # ← Enter/변경 시 처리
)


# ---------------------------
# 이전/다음 버튼 (좌측 촘촘)
# ---------------------------
c1, c2, csp = st.columns([0.14, 0.14, 0.72])
with c1:
    if st.button("⏮ 이전", use_container_width=True):
        if st.session_state.lesson_index > 0:
            st.session_state.lesson_index -= 1
            st.rerun()
with c2:
    if st.button("⏭ 다음", use_container_width=True):
        if st.session_state.lesson_index < len(lessons) - 1:
            st.session_state.lesson_index += 1
            st.rerun()
with csp:
    st.markdown(
        f"<div style='text-align:right;font-weight:700;'>현재 Lesson: {lessons[st.session_state.lesson_index]['lesson']:02d} / {len(lessons):02d}</div>",
        unsafe_allow_html=True,
    )


# ---------------------------
# 현재 선택된 Lesson
# ---------------------------
lesson = lessons[st.session_state.lesson_index]

# 제목 구성: "영문 | 한글"이 들어온 경우 분리
title_en, title_ko = lesson["title"], ""
if "|" in lesson["title"]:
    parts = lesson["title"].split("|", 1)
    title_en = parts[0].strip()
    title_ko = parts[1].strip()

# 버튼 바로 아래 제목 표시 (요청사항)
st.markdown(
    f"<h2 style='margin-top:8px;'>Lesson {lesson['lesson']:02d} — {title_en}"
    + (f" | {title_ko}" if title_ko else "")
    + "</h2>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ---------------------------
# 오디오 (제목 바로 아래로 이동)
# 파일명: "01. 한국제목.mp3"
# ---------------------------
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

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------
# 본문 섹션 (구간 사이 공백 1줄)
# ---------------------------
st.subheader("🗣 영어 문장 | English Sentences")
st.markdown("<br>".join(lesson["english"].split("\n")), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🇰🇷 한국어 번역 | Korean Translation")
st.markdown("<br>".join(lesson["korean"].split("\n")), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("💡 문법·표현 포인트 | Grammar & Expressions")
for g in lesson.get("grammar", []):
    st.markdown(f"- {g}")
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📝 말하기 연습 | Speaking Practice")
for s in lesson.get("practice", []):
    st.markdown(f"- {s}")


# ---------------------------
# PDF 생성·다운로드 (서버 저장 없이 바로)
# ---------------------------
def create_pdf_buffer(lesson_obj):
    pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))
    styles = getSampleStyleSheet()
    for n in styles.byName:
        styles[n].fontName = 'HYSMyeongJo-Medium'
    styles.add(ParagraphStyle(name="KTitle", fontName="HYSMyeongJo-Medium",
                              fontSize=16, leading=20, alignment=1))
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50)
    story = []

    def add(txt, style="BodyText", space=8):
        story.append(Paragraph(txt, styles[style])); story.append(Spacer(1, space))

    # 제목
    t_en, t_ko = lesson_obj["title"], ""
    if "|" in t_en:
        p = t_en.split("|", 1); t_en, t_ko = p[0].strip(), p[1].strip()
    full_title = f"Lesson {lesson_obj['lesson']:02d} — {t_en}" + (f" | {t_ko}" if t_ko else "")
    add(f"<b>{full_title}</b>", "KTitle", 14)

    add("<b>🗣 영어 문장 | English Sentences</b>")
    add(lesson_obj["english"].replace("\n", "<br/>"))

    add("<b>🇰🇷 한국어 번역 | Korean Translation</b>")
    add(f"<font color='gray'>{lesson_obj['korean'].replace('\n', '<br/>')}</font>")

    add("<b>💡 문법·표현 포인트 | Grammar & Expressions</b>")
    for g in lesson_obj.get("grammar", []): add(f"- {g}")

    add("<b>📝 말하기 연습 | Speaking Practice</b>")
    for s in lesson_obj.get("practice", []): add(f"- {s}")

    doc.build(story)
    buf.seek(0)
    return buf

pdf_buffer = create_pdf_buffer(lesson)
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    label="📄 학습지 PDF 다운로드",
    data=pdf_buffer,
    file_name=f"Lesson_{lesson['lesson']:02d}.pdf",
    mime="application/pdf"
)
