
import streamlit as st
import pandas as pd


# ------------------------------
# 1. 파일 경로 및 설정
# ------------------------------

MENTOR_FILE = "mentors.txt"
MENTEE_FILE = "mentees.txt"

WEIGHTS = {
    "subject": 40,
    "day": 35,
    "level": 25
}


# ------------------------------
# 2. 파일에서 데이터 읽기
# ------------------------------

def read_people(filename):
    people = []

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 한 사람당 6줄
    for i in range(0, len(lines), 6):
        block = lines[i:i + 6]

        # 데이터가 불완전하면 건너뜀
        if len(block) < 6:
            continue

        person = {
            "name": block[0].strip(),
            "subjects": [
                x.strip() for x in block[1].strip().split(",")
                if x.strip()
            ],
            "days": [
                x.strip() for x in block[2].strip().split(",")
                if x.strip()
            ],
            "levels": [
                x.strip() for x in block[3].strip().split(",")
                if x.strip()
            ],
            "middle_score": int(block[4].strip())
        }

        if person["name"]:
            people.append(person)

    return people


def read_mentor():
    return read_people(MENTOR_FILE)


def read_mentee():
    return read_people(MENTEE_FILE)


# ------------------------------
# 3. 데이터를 파일에 저장
# ------------------------------

def write_people(filename, people):
    with open(filename, "w", encoding="utf-8") as f:
        for person in people:
            f.write(person["name"] + "\n")
            f.write(", ".join(person["subjects"]) + "\n")
            f.write(", ".join(person["days"]) + "\n")
            f.write(", ".join(person["levels"]) + "\n")
            f.write(str(person["middle_score"]) + "\n")
            f.write("----------\n")


def write_mentor(mentors):
    write_people(MENTOR_FILE, mentors)


def write_mentee(mentees):
    write_people(MENTEE_FILE, mentees)


# ------------------------------
# 4. 멘토 및 멘티 추가
# ------------------------------

def add_mentor(mentors, name, subjects, days, levels, score):
    mentor = {
        "name": name.strip(),
        "subjects": subjects,
        "days": days,
        "levels": levels,
        "middle_score": score
    }

    mentors.append(mentor)


def add_mentee(mentees, name, subjects, days, level, score):
    mentee = {
        "name": name.strip(),
        "subjects": subjects,
        "days": days,
        "levels": [level],
        "middle_score": score
    }

    # 같은 정보가 이미 저장되어 있는지 확인
    duplicate = False

    for person in mentees:
        if (
            person["name"] == mentee["name"]
            and person["subjects"] == mentee["subjects"]
            and person["days"] == mentee["days"]
            and person["levels"] == mentee["levels"]
            and person["middle_score"] == mentee["middle_score"]
        ):
            duplicate = True
            break

    if not duplicate:
        mentees.append(mentee)


# ------------------------------
# 5. 매칭 점수 계산
# ------------------------------

def calculate_score(mentor, mentee):
    score = 0
    reasons = []

    # 1. 멘토 자격 확인
    # 멘토의 점수가 멘티보다 낮으면 추천에서 제외
    if mentor["middle_score"] < mentee["middle_score"]:
        return 0, [
            "멘토의 중간고사 점수가 멘티보다 낮아 제외"
        ]

    # 2. 공통 과목 확인
    common_subjects = (
        set(mentee["subjects"]) & set(mentor["subjects"])
    )

    # 공통 과목이 없으면 추천하지 않음
    if not common_subjects:
        return 0, [
            "공통 과목이 없어 추천 대상에서 제외"
        ]

    subject_score = (
        len(common_subjects) / len(mentee["subjects"])
    ) * WEIGHTS["subject"]

    score += subject_score

    reasons.append(
        f"과목 {', '.join(sorted(common_subjects))} 일치: "
        f"+{subject_score:.1f}점"
    )

    # 3. 공통 요일 확인
    common_days = (
        set(mentee["days"]) & set(mentor["days"])
    )

    day_score = (
        len(common_days) / len(mentee["days"])
    ) * WEIGHTS["day"]

    score += day_score

    if common_days:
        reasons.append(
            f"가능 요일 {', '.join(sorted(common_days))} 일치: "
            f"+{day_score:.1f}점"
        )
    else:
        reasons.append("가능 요일 일치 없음: +0점")

    # 4. 학습 수준 확인
    if mentee["levels"][0] in mentor["levels"]:
        score += WEIGHTS["level"]

        reasons.append(
            f"학습 수준 지도 가능: +{WEIGHTS['level']}점"
        )
    else:
        reasons.append("학습 수준 불일치: +0점")

    return round(score, 1), reasons


# ------------------------------
# 6. 적합한 멘토 추천
# ------------------------------

def match_mentors(mentors, mentee, top_n=3):
    results = []

    for mentor in mentors:
        score, reasons = calculate_score(mentor, mentee)

        # 자격 미달 또는 점수가 0점이면 제외
        if score == 0:
            continue

        results.append({
            "name": mentor["name"],
            "score": score,
            "reasons": reasons,
            "subjects": mentor["subjects"],
            "days": mentor["days"],
            "levels": mentor["levels"]
        })

    # 점수가 높은 순서대로 정렬
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_n]


# ------------------------------
# 7. Streamlit 화면 설정
# ------------------------------

st.set_page_config(
    page_title="멘토-멘티 매칭",
    page_icon="🤝",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state.page = "main"


# ------------------------------
# 8. 메인 화면
# ------------------------------

if st.session_state.page == "main":

    st.title("🤝 멘토-멘티 매칭")

    st.write(
        "관심 과목, 가능한 요일, 학습 수준을 비교하여 "
        "적합한 멘토를 추천합니다."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 멘토", use_container_width=True):
            st.session_state.page = "mentor"
            st.rerun()

    with col2:
        if st.button("📚 멘티", use_container_width=True):
            st.session_state.page = "mentee"
            st.rerun()


# ------------------------------
# 9. 멘토 메뉴
# ------------------------------

elif st.session_state.page == "mentor":

    st.title("🎓 멘토 메뉴")

    if st.button("⬅ 메인으로"):
        st.session_state.page = "main"
        st.rerun()

    menu = st.radio(
        "메뉴 선택",
        ["멘토 등록", "등록된 멘토 확인"],
        horizontal=True
    )

    mentors = read_mentor()

    # 멘토 등록
    if menu == "멘토 등록":

        st.subheader("멘토 등록")

        with st.form("mentor_form"):

            name = st.text_input("멘토 이름")

            subjects = st.multiselect(
                "가르칠 수 있는 과목",
                ["국어", "영어", "수학", "사회", "과학", "역사", "도덕",
                "기술가정", "정보", "체육", "음악", "미술"]
            )

            days = st.multiselect(
                "가능 요일",
                ["월", "화", "수", "목", "금", "토", "일"]
            )

            levels = st.multiselect(
                "지도 가능한 수준",
                ["초급", "중급", "고급"]
            )

            score = st.number_input(
                "중간고사 점수",
                min_value=0,
                max_value=100,
                value=70,
                step=1
            )

            submitted = st.form_submit_button("등록하기")

        if submitted:

            if not name.strip():
                st.warning("이름을 입력하세요.")

            elif not subjects:
                st.warning("가르칠 과목을 선택하세요.")

            elif not days:
                st.warning("가능 요일을 선택하세요.")

            elif not levels:
                st.warning("지도 가능한 수준을 선택하세요.")

            elif any(
                m["name"] == name.strip()
                for m in mentors
            ):
                st.warning("이미 등록된 이름입니다.")

            else:
                add_mentor(
                    mentors,
                    name,
                    subjects,
                    days,
                    levels,
                    int(score)
                )

                write_mentor(mentors)

                st.success("멘토 등록 완료!")

    # 등록된 멘토 확인
    else:

        st.subheader("등록된 멘토")

        if mentors:

            display_data = []

            for mentor in mentors:
                display_data.append({
                    "이름": mentor["name"],
                    "과목": ", ".join(mentor["subjects"]),
                    "가능 요일": ", ".join(mentor["days"]),
                    "지도 수준": ", ".join(mentor["levels"]),
                    "중간고사 점수": mentor["middle_score"]
                })

            st.dataframe(
                pd.DataFrame(display_data),
                use_container_width=True
            )

        else:
            st.info("등록된 멘토가 없습니다.")


# ------------------------------
# 10. 멘티 메뉴
# ------------------------------

elif st.session_state.page == "mentee":

    st.title("📚 멘티 메뉴")

    if st.button("⬅ 메인으로"):
        st.session_state.page = "main"
        st.rerun()

    menu = st.radio(
        "메뉴 선택",
        ["멘토 찾기", "등록된 멘티 확인"],
        horizontal=True
    )

    mentors = read_mentor()
    mentees = read_mentee()

    # 멘티 정보 입력 및 매칭
    if menu == "멘토 찾기":

        st.subheader("멘티 정보 입력")

        with st.form("mentee_form"):

            name = st.text_input("멘티 이름")

            subjects = st.multiselect(
                "배우고 싶은 과목",
                ["국어", "영어", "수학", "사회", "과학", "역사", "도덕",
                "기술가정", "정보", "체육", "음악", "미술"]
            )

            days = st.multiselect(
                "가능한 요일",
                ["월", "화", "수", "목", "금", "토", "일"]
            )

            level = st.selectbox(
                "현재 학습 수준",
                ["초급", "중급", "고급"]
            )

            score = st.number_input(
                "중간고사 점수",
                min_value=0,
                max_value=100,
                value=70,
                step=1
            )

            submitted = st.form_submit_button("멘토 찾기")

        if submitted:

            if not name.strip():
                st.warning("이름을 입력하세요.")

            elif not subjects:
                st.warning("배우고 싶은 과목을 선택하세요.")

            elif not days:
                st.warning("가능한 요일을 선택하세요.")

            elif not mentors:
                st.warning("먼저 멘토를 등록하세요.")

            else:
                mentee = {
                    "name": name.strip(),
                    "subjects": subjects,
                    "days": days,
                    "levels": [level],
                    "middle_score": int(score)
                }

                # 멘티 정보 저장
                add_mentee(
                    mentees,
                    name,
                    subjects,
                    days,
                    level,
                    int(score)
                )

                write_mentee(mentees)

                # 멘토 추천
                results = match_mentors(mentors, mentee)

                if not results:

                    st.info(
                        "조건에 맞는 멘토가 없습니다. "
                        "과목과 점수 조건을 확인하세요."
                    )

                else:

                    st.subheader(f"{name}님의 추천 결과")

                    for rank, result in enumerate(results, start=1):

                        st.markdown(
                            f"### {rank}위 {result['name']} "
                            f"- {result['score']}점"
                        )

                        st.progress(
                            min(
                                100,
                                max(0, int(result["score"]))
                            )
                        )

                        st.write(
                            "과목:",
                            ", ".join(result["subjects"])
                        )

                        st.write(
                            "가능 요일:",
                            ", ".join(result["days"])
                        )

                        st.write(
                            "지도 수준:",
                            ", ".join(result["levels"])
                        )

                        st.write("추천 이유")

                        for reason in result["reasons"]:
                            st.write(f"- {reason}")

                        st.divider()

    # 등록된 멘티 확인
    else:

        st.subheader("등록된 멘티")

        if mentees:

            display_data = []

            for mentee in mentees:
                display_data.append({
                    "이름": mentee["name"],
                    "과목": ", ".join(mentee["subjects"]),
                    "가능 요일": ", ".join(mentee["days"]),
                    "학습 수준": ", ".join(mentee["levels"]),
                    "중간고사 점수": mentee["middle_score"]
                })

            st.dataframe(
                pd.DataFrame(display_data),
                use_container_width=True
            )

        else:
            st.info("등록된 멘티가 없습니다.")
