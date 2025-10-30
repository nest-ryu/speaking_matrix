import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from config import PDF_OUTPUT_DIR

# 한글 폰트 등록
pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))

# PDF 파일 경로
output_path = os.path.join(PDF_OUTPUT_DIR, "Day28_29_30.pdf")

# 스타일 정의
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Unified',
                          fontName='HYSMyeongJo-Medium',
                          fontSize=12,
                          leading=22,
                          spaceAfter=14))
styles.add(ParagraphStyle(name='HeadingUnified',
                          fontName='HYSMyeongJo-Medium',
                          fontSize=14,
                          leading=26,
                          spaceAfter=20))

# 내용 구성
content = []

# DAY 28
content.append(Paragraph("DAY 28 - Spending Time with Friends | 친구들과의 시간", styles['HeadingUnified']))

content.append(Paragraph("영어 문장 | English Sentences", styles['HeadingUnified']))
content.append(Paragraph("""These days, there isn't enough time to hang out with my friends.<br/>
Everyone's schedule is tight, so we meet up once during the week or on weekends.<br/>
We normally go to a coffee shop or have a drink.<br/>
I don't love talking, but I am a good listener.<br/>
However, it depends on the person.<br/>
I don't want to listen to a person who only talks about themselves.""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("한국어 번역 | Korean Translation", styles['HeadingUnified']))
content.append(Paragraph("""요즘에는 친구들과 어울려 다닐 시간이 별로 없습니다.<br/>
다들 스케줄이 빡빡해서 주중이나 주말에 한 번 만나요.<br/>
우리는 보통 커피숍에 가거나 술을 마십니다.<br/>
저는 말하는 것을 좋아하지 않지만 남의 이야기는 잘 들어줍니다.<br/>
하지만 그건 사람에 따라 달라요.<br/>
자기 이야기만 하는 사람의 말은 듣고 싶지 않아요.""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("문법&middot;표현 포인트 | Grammar &amp; Expressions", styles['HeadingUnified']))
content.append(Paragraph("""• hang out with friends → 친구들과 어울리다<br/>
• be tight (schedule) → 일정이 빡빡하다<br/>
• it depends on → ~에 따라 다르다<br/>
• talk about oneself → 자기 이야기를 하다<br/>
• be a good listener → 잘 들어주는 사람이다""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("말하기 연습 | Speaking Practice", styles['HeadingUnified']))
content.append(Paragraph("""• 저는 친구들과 어울릴 시간이 별로 없어요. → I don’t have much time to hang out with my friends.<br/>
• 주중이나 주말에 한 번 만나요. → We meet once during the week or on weekends.<br/>
• 자기 이야기만 하는 사람은 싫어요. → I don’t like people who only talk about themselves.""", styles['Unified']))

# 새 페이지
content.append(PageBreak())

# DAY 29
content.append(Paragraph("DAY 29 - My Friend’s Birthday | 친구의 생일", styles['HeadingUnified']))

content.append(Paragraph("영어 문장 | English Sentences", styles['HeadingUnified']))
content.append(Paragraph("""It was Kim’s birthday yesterday.<br/>
We had a birthday party at a restaurant in the neighborhood.<br/>
The restaurant is a 10-minute walk from my house.<br/>
I gave Kim a scented candle for her birthday present.<br/>
She was satisfied with the present, and I was satisfied with my choice.<br/>
We spent about three hours at the restaurant.<br/>
We had a great time.""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("한국어 번역 | Korean Translation", styles['HeadingUnified']))
content.append(Paragraph("""어제는 Kim의 생일이었어요.<br/>
우리는 동네 식당에서 생일 파티를 했어요.<br/>
그 식당은 우리 집에서 걸어서 10분 거리입니다.<br/>
저는 Kim에게 생일 선물로 향초를 줬어요.<br/>
Kim은 선물에 만족했고 저도 제 선택에 만족했어요.<br/>
우리는 세 시간 정도 식당에 있었고 즐거운 시간을 보냈어요.""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("문법&middot;표현 포인트 | Grammar &amp; Expressions", styles['HeadingUnified']))
content.append(Paragraph("""• birthday present → 생일 선물<br/>
• be satisfied with → ~에 만족하다<br/>
• a 10-minute walk → 도보로 10분 거리<br/>
• spend time → 시간을 보내다<br/>
• have a great time → 즐거운 시간을 보내다""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("말하기 연습 | Speaking Practice", styles['HeadingUnified']))
content.append(Paragraph("""• 어제는 Kim의 생일이었어요. → It was Kim’s birthday yesterday.<br/>
• 향초를 선물했어요. → I gave her a scented candle.<br/>
• 우리는 즐거운 시간을 보냈어요. → We had a great time.""", styles['Unified']))

# 새 페이지
content.append(PageBreak())

# DAY 30
content.append(Paragraph("DAY 30 - A Conversation with a Friend | 친구와의 대화", styles['HeadingUnified']))

content.append(Paragraph("영어 문장 | English Sentences", styles['HeadingUnified']))
content.append(Paragraph("""On the way back home, Kim and I went to the park behind her house.<br/>
We sat on a bench and had a talk.<br/>
I was a bit tired, but I listened to Kim.<br/>
She talked about some issues with her boss.<br/>
I told her that it is complicated to solve these problems, but it wouldn’t take too much time.<br/>
When I got home, it was 11:30 p.m.<br/>
I got ready for bed and went to sleep at midnight.""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("한국어 번역 | Korean Translation", styles['HeadingUnified']))
content.append(Paragraph("""집에 오는 길에 Kim과 저는 Kim의 집 뒤 공원에 갔습니다.<br/>
우리는 벤치에 앉아 대화를 나눴습니다.<br/>
저는 조금 피곤했지만 Kim의 이야기를 들어줬습니다.<br/>
Kim은 직장 상사와의 문제에 대해 이야기했어요.<br/>
저는 그런 문제는 복잡하지만 오래 걸리지는 않을 거라고 말했습니다.<br/>
집에 도착했을 때는 밤 11시 30분이었어요.<br/>
잘 준비를 하고 자정에 잠이 들었습니다.""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("문법&middot;표현 포인트 | Grammar &amp; Expressions", styles['HeadingUnified']))
content.append(Paragraph("""• on the way back home → 집에 오는 길에<br/>
• have a talk → 대화를 나누다<br/>
• talk about → ~에 대해 이야기하다<br/>
• get ready for bed → 잠잘 준비를 하다<br/>
• go to sleep → 잠이 들다""", styles['Unified']))
content.append(Spacer(1, 16))

content.append(Paragraph("말하기 연습 | Speaking Practice", styles['HeadingUnified']))
content.append(Paragraph("""• 우리는 공원 벤치에 앉아 이야기했어요. → We sat on a bench and had a talk.<br/>
• Kim은 상사 문제에 대해 얘기했어요. → Kim talked about issues with her boss.<br/>
• 저는 자정에 잠이 들었어요. → I went to sleep at midnight.""", styles['Unified']))

# PDF 생성
doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)
doc.build(content)

print(f"PDF 파일 생성 완료: {output_path}")
