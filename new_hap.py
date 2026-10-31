
import streamlit as st # gui 창
import pandas as pd

MENTOR_FILE = "mentors.txt" #저장할 텍스트 파일
MENTEE_FILE = "mentees.txt" 

mentors = [ ] # 정보 들어갈 딕셔너리
mentees = [ ]


WEIGHTS = { # 가중치(점수 비율)
    "subject": 40,
    "day": 35,
    "level": 25,
}


def calculate_score(mentor, mentee): # 점수 계산
    score = 0 # 점수 초기화
    reasons = [] # 이유

    common_subjects = set(mentee["subjects"]) & set(mentor["subjects"]) # 멘토와 멘티 과목 교집합(겹치는부분)

    # 관심 분야는 무조건 하나 이상 일치해야함
    if not common_subjects: # 안일치하면
        return 0, ["과목이 일치하지 않아 추천 대상에서 제외"]

    subject_score = (
        len(common_subjects) / len(mentee["subjects"]) # 겹치는 과목 개수 / 멘티 과목 개수
    ) * WEIGHTS["subject"] 
    score += subject_score
    reasons.append( # 이유 작성(과목이 일치함)
        f"관심 분야 {', '.join(sorted(common_subjects))} 일치: "
        f"+{subject_score:.1f}점"
    )

    common_days = set(mentee["days"]) & set(mentor["days"])
    
    day_score = ( 
        len(common_days) / len(mentee["days"])
    ) * WEIGHTS["day"]
    score += day_score

    if common_days:
        reasons.append(
            f"가능 요일 {', '.join(sorted(common_days))} 일치: "
            f"+{day_score:.1f}점"
        )
    # 날짜도 무조건 하나 이상 일치해야함
    else: # 안일치하면
        reasons.append("가능 요일 일치 없음: +0점")

    if mentee["level"] in mentor["levels"]:
        score += WEIGHTS["level"]
        reasons.append(
            f"학습 수준 지도 가능: +{WEIGHTS['level']}점"
        )
    else:
        reasons.append("학습 수준 불일치: +0점")

    if mentee["method"] == mentor["method"]:
        score += WEIGHTS["method"]
        reasons.append(
            f"멘토링 방식 일치: +{WEIGHTS['method']}점"
        )
    else:
        reasons.append("멘토링 방식 불일치: +0점")

    return round(score, 1), reasons


# 멘토 비교
def match_mentors(mentors, mentee, top_n=3): # top_n=3이 뭐지
    results = []

    for mentor in mentors:
        score, reasons = calculate_score(mentor, mentee)

        if score == 0:
            continue

        results.append({
            "name": mentor["name"],
            "score": score,
            "reasons": reasons,
            "subjects": mentor["subjects"],
            "days": mentor["days"],
            "method": mentor["method"]
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_n]


# gui
st.set_page_config(
    page_title="멘토-멘티 매칭",
    page_icon="icon",
    layout="centered"
)

st.title("멘토-멘티 매칭") # 제목
st.write(
    "관심 분야, 가능한 요일, 현재 수준, 희망 방식을 비교하여 "
    "적합한 멘토를 추천합니다."
) # 설명글

st.subheader("등록된 멘토")

display_data = []
for mentor in mentors:
    display_data.append({
        "이름": mentor["name"],
        "분야": ", ".join(mentor["subjects"]),
        "가능 요일": ", ".join(mentor["days"]),
        "지도 수준": ", ".join(mentor["levels"]),
        "방식": mentor["method"]
    })

st.dataframe(pd.DataFrame(display_data)) # display_data에 있는거 출력(나중에 이거 바꾸기)

st.subheader("멘티 정보 입력")

mentee_name = st.text_input("이름")
subjects = st.multiselect(
    "배우고 싶은 분야",
    [ "국어",  "영어", "수학", "사회", "과학", "역사", "도덕",
    "기술가정", "정보", "체육", "음악", "미술"]
)
days = st.multiselect(
    "가능한 요일",
    ["월", "화", "수", "목", "금", "토", "일"]
)
level = st.selectbox(
    "현재 수준",
    ["초급", "중급", "고급"]
)


# ------------------------------
# 5. 추천 실행
# ------------------------------
if st.button("멘토 찾기"):
    if not mentee_name.strip():
        st.warning("이름을 입력하세요.")
    elif not subjects:
        st.warning("관심 분야를 하나 이상 선택하세요.")
    elif not days:
        st.warning("가능한 요일을 하나 이상 선택하세요.")
    else:
        mentee = {
            "name": mentee_name.strip(),
            "subjects": subjects,
            "days": days,
            "level": level,
        }

        results = match_mentors(mentors, mentee)

        if not results:
            st.info("관심 분야가 맞는 멘토가 없습니다.")
        else:
            st.subheader(f"{mentee['name']}님의 추천 결과")

            for rank, result in enumerate(results, start=1):
                st.markdown(
                    f"### {rank}위 {result['name']} - "
                    f"{result['score']}점"
                )

                st.progress(int(result["score"]))

                st.write("분야:", ", ".join(result["subjects"]))
                st.write("가능 요일:", ", ".join(result["days"]))
                st.write("방식:", result["method"])

                st.write("추천 이유")
                for reason in result["reasons"]:
                    st.write("-", reason)

                st.divider()
