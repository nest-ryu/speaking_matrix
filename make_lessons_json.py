import json
import re
import pdfplumber
from config import SOURCE_PDF, LESSONS_JSON


# -------------------------------
# 📄 PDF 텍스트 추출 (pdfplumber 사용)
# -------------------------------
def extract_text(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)


# -------------------------------
# 🔹 Lesson 구분 (DAY 01–30)
# -------------------------------
def split_lessons(full_text):
    """
    PDF 내 'DAY 01 — 제목' 또는 'DAY 01 - 제목' 패턴으로 레슨 분리
    """
    pattern = r"DAY\s*(\d{1,2})\s*[—-]\s*(.+)"
    matches = list(re.finditer(pattern, full_text))
    lessons = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        lesson_num = int(m.group(1))
        title = m.group(2).strip()
        body = full_text[start:end].strip()
        lessons.append((lesson_num, title, body))
    return lessons


# -------------------------------
# 🔹 텍스트 정리 함수 (소제목 제거)
# -------------------------------
def clean_text(text):
    if not text:
        return ""
    # 불필요한 라벨 제거 (영문+한글)
    text = re.sub(r"^\s*[|.\-·]*\s*(English Sentences?|영어 문장).*", "", text, flags=re.I | re.M)
    text = re.sub(r"^\s*[|.\-·]*\s*(Korean Translation|한국어 번역).*", "", text, flags=re.I | re.M)
    text = re.sub(r"^\s*[|.\-·]*\s*(Grammar.*|문법.*|표현 포인트.*)", "", text, flags=re.I | re.M)
    text = re.sub(r"^\s*[|.\-·]*\s*(Speaking Practice|말하기 연습|연습).*", "", text, flags=re.I | re.M)
    # 깨끗하게 정리
    return text.strip(" \n\t|·")


def clean_list(lst):
    cleaned = []
    for item in lst:
        t = clean_text(item)
        if t:
            cleaned.append(t)
    return cleaned


# -------------------------------
# 🔹 각 Lesson 내 섹션 추출
# -------------------------------
def extract_sections(body_text):
    """
    본문에서 네 섹션을 분리:
    - 영어 문장
    - 한국어 번역
    - 문법·표현 포인트
    - 말하기 연습
    """
    labels = [
        r"🗣\s*영어 문장.*?|영어 문장.*?",
        r"🇰🇷\s*한국어 번역.*?|한국어 번역.*?",
        r"💡\s*문법.*?|문법.*?",
        r"📝\s*말하기.*?|말하기.*?"
    ]

    parts = re.split("(" + "|".join(labels) + ")", body_text)
    def get_content(label_text):
        try:
            idx = next(i for i, t in enumerate(parts) if re.match(label_text, t or "", flags=re.I))
            return parts[idx + 1].strip()
        except StopIteration:
            return ""

    english = clean_text(get_content(labels[0]))
    korean = clean_text(get_content(labels[1]))
    grammar_raw = get_content(labels[2])
    practice_raw = get_content(labels[3])

    grammar = clean_list(grammar_raw.splitlines())
    practice = clean_list(practice_raw.splitlines())

    return english, korean, grammar, practice


# -------------------------------
# 🔹 JSON 생성
# -------------------------------
def build_json(pdf_path, out_json):
    text = extract_text(pdf_path)
    blocks = split_lessons(text)
    lessons = []

    for num, title, body in blocks:
        english, korean, grammar, practice = extract_sections(body)
        lessons.append({
            "lesson": num,
            "title": title,
            "english": english,
            "korean": korean,
            "grammar": grammar,
            "practice": practice
        })

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)

    print(f"✅ lessons.json 생성 완료 ({len(lessons)}개 Lesson) → {out_json}")


# -------------------------------
# 🚀 실행 진입점
# -------------------------------
if __name__ == "__main__":
    print("📘 PDF → JSON 변환 시작 (소제목 자동 제거 버전)")
    build_json(SOURCE_PDF, LESSONS_JSON)
