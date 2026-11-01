"""
v 0.0.1
- 중간고사 점수 추가

v 0.0.2
- 홈화면, 돌아가기 추가
- 파일입출력 추가
- 중간고사 점수 추가 완료


**오늘 도서관가서 코드만짠다**

"""


import streamlit as st # gui 창
import pandas as pd

MENTOR_FILE = "mentors.txt" #저장할 텍스트 파일
MENTEE_FILE = "mentees.txt" 

with open(MENTOR_FILE, "a", encoding="utf-8") : # 파일이 없으면 새로 생성
    pass
with open(MENTEE_FILE, "a", encoding="utf-8") : 
    pass

mentors = [ # 임시멘토
    {
        "name": "김민수",
        "subjects": ["수학", "영어"],
        "days": ["월", "수", "금"],
        "level": "초급",
        "method": "온라인",
        "middle_score": 85
    },
    {
        "name": "이서연",
        "subjects": ["국어", "수학"],
        "days": ["화", "목", "토"],
        "level": "중급",
        "method": "오프라인",
        "middle_score": 95
    },
    {
        "name": "홍길동",
        "subjects": ["국어", "수학", "영어", "과학", "사회"],
        "days": ["월", "화", "수", "목", "토"],
        "level": "고급",
        "method": "오프라인",
        "middle_score": 100
    }
] # 정보 들어갈 딕셔너리
mentees = [ ]


WEIGHTS = { # 가중치(점수 비율)
    "subject": 40,
    "day": 30,
    "level": 20,
    "method": 10
}


def calculate_score(mentor, mentee): # 점수 계산
    score = 0 # 점수 초기화
    reasons = [] # 이유

    common_subjects = set(mentee["subjects"]) & set(mentor["subjects"]) # 멘토와 멘티 과목 교집합(겹치는부분)

    # 관심 분야는 무조건 하나 이상 일치해야함
    if not common_subjects: # 안일치하면
        return 0, ["과목이 일치하지 않아 추천 대상에서 제외"]

    # 겹치는 과목 개수 / 멘티 과목 개수
    subject_score = (len(common_subjects) / len(mentee["subjects"])) * WEIGHTS["subject"] 
    score += subject_score

    # 이유 작성(과목이 일치함)
    reasons.append(f"관심 분야 {', '.join(sorted(common_subjects))} 일치: +{subject_score:.1f}점")

    common_days = set(mentee["days"]) & set(mentor["days"])
    
    day_score = (len(common_days) / len(mentee["days"])) * WEIGHTS["day"] # 겹치는 비율 X 가중치
    score += day_score


    # 날짜도 무조건 하나 이상 일치해야함
    if common_days:
        reasons.append(f"가능 요일 {', '.join(sorted(common_days))} 일치: +{day_score:.1f}점")
    else: # 안일치하면
        return 0, ["날짜가 일치하지 않아 추천 대상에서 제외"]

    if mentee["level"] == mentor["level"]:
        score += WEIGHTS["level"]
        reasons.append(f"학습 수준 지도 가능: +{WEIGHTS['level']}점")
    else:
        reasons.append("학습 수준 불일치: +0점")

    if mentee["method"] == mentor["method"]:
        score += WEIGHTS["method"]
        reasons.append(f"멘토링 방식 일치: +{WEIGHTS['method']}점")
    else:
        reasons.append("멘토링 방식 불일치: +0점")

    if mentee["middle_score"] > mentor["middle_score"] :
        score = 0; # 멘토의 중간고사 점수가 더 낮으면 0점
        reasons.append("멘토의 중간고사 점수가 더 낮음, 0점")
    else :
        score += 0

    return round(score, 1), reasons


# 멘토 비교
def match_mentors(mentors, mentee, top_n=3): # top_n=3
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
    ) # 멘토(item) 딕셔너리를 점수 순으로 내림차순

    return results[:top_n]

#file_io_prac.py
#사용자 -> 딕셔너리
def add_people(peoples) :
    people = {
        "name" : input("이름 : ").strip(),
        "subjects" : input("과목(,로 구분) : ").split(),
        "days" : input("가능 요일(,로 구분) : ").split(),
        "level" : input("수준(,로 구분) : ").strip(),
        "middle_score" : int(input("중간고사 점수 : "))
    }
    peoples.append(people)

def add_mentor() :
    return add_people(mentors)

def add_mentee() :
    return add_people(mentees)


#딕셔너리 -> 파일
def write_people(filename, peoples) : # write_mentor(mentors) 하면 mentors 딕셔너리 전체가 파일에 저장
    with open(filename, "w", encoding="utf-8") as f :
        for people in peoples :
            f.write(people["name"] + "\n")
            f.write(", ".join(people["subjects"]) + "\n") # 쉼표로 나열하기 (국어, 영어, 수학)
            f.write(", ".join(people["days"]) + "\n")
            f.write(people["level"] + "\n")
            f.write(people["method"] + "\n")
            f.write(str(people["middle_score"]) + "\n")
            f.write("----------\n") # 구분하는거

def write_mentors() :
    write_people(MENTOR_FILE, mentors)

def write_mentees() :
    write_people(MENTEE_FILE, mentees)


# 파일 -> 딕셔너리
def read_people(filename, peoples) : # 파일에서부터 정보 꺼내서 딕셔너리에 저장
    peoples.clear()
    with open(filename, "r", encoding="utf-8") as f :
        for i, data in enumerate(f) :  # enumerate(f)는 파일의 줄과 그 줄의 정보 출력, i = 0, data = "홍길동"
            index = i // 7 # 몫 구하기
            data = data.strip() # 앞뒤 공백, 줄바꿈 제거
            match i % 7 : # switch case 문 비슷한거, default는 _로
                        #이름 ~ 구분기호 총 6줄, i%6 해서 구별
                case 0 :
                    peoples.append({})
                    peoples[index]["name"] = data
                case 1 : 
                    data = data.split(", ") # 과목, 요일, 수준은 배열로 받기
                    peoples[index]["subjects"] = data
                case 2 : 
                    data = data.split(", ")
                    peoples[index]["days"] = data
                case 3 : 
                    peoples[index]["level"] = data
                case 4 : 
                    peoples[index]["method"] = data
                case 5 :
                    peoples[index]["middle_score"] = int(data) # 중간 점수는 정수로 받기
                case _ : # 나머지 -----일때 무시
                    continue

def read_mentors() :
   mentors.clear()
   return read_people(MENTOR_FILE, mentors)

def read_mentees() :
   mentees.clear()
   return read_people(MENTEE_FILE, mentees)


















# gui
st.set_page_config( # 설정
    page_title="멘토-멘티 매칭",
    page_icon="icon",
    layout="centered"
)
if "page" not in st.session_state: # 처음 앱을 열었을때 세션스테이트 홈으로 정하기
    st.session_state.page = "home"

if st.session_state.page == "home" :
    st.title("멘토-멘티 매칭 프로그램")
    st.write("원하는 역할을 선택해주세요")
    if st.button("멘토로 참여하기") :
        st.session_state.page = "Mentor" # 멘토 페이지로 이동
        st.rerun() # 화면 초기화
    elif st.button("멘티로 참여하기") :
        st.session_state.page = "Mentee" # 멘티 페이지로 이동
        st.rerun() # 화면 초기화
    elif st.button("멘토, 멘티 확인") :
        st.session_state.page = "Check_MM" #멘토멘티 확인 페이지로 이동
        st.rerun() # 화면 초기화

if st.session_state.page == "Mentor" : # 멘토로 참여하기
    st.title("멘토로 참여하기")
    st.write("나의 경험과 지식을 필요로 하는 멘티를 매칭해 드립니다!") # 멘토 설명글
    if st.button("돌아가기") :
        st.session_state.page = "home" # 홍으로 돌아가기
        st.rerun() # 화면 초기화

elif st.session_state.page == "Mentee" : # 멘티로 참여하기
    st.title("멘티로 참여하기") # 제목
    st.write("나의 성향과 일정에 꼭 맞는 최적의 멘토를 매칭해 드립니다!") # 멘티 설명글

    st.subheader("등록된 멘토")

    read_mentors()

#    display_data = [] # 모든 멘토 정보 저장 배열
 #   for mentor in mentors:
  #      display_data.append({
   #         "이름": mentor["name"],
    #        "분야": ", ".join(mentor["subjects"]),
     #       "가능 요일": ", ".join(mentor["days"]),
      #      "지도 수준": ", ".join(mentor["level"]),
       #     "방식": mentor["method"],
        #    "중간고사 점수": mentor["middle_score"]
        #})

    st.dataframe(pd.DataFrame(mentors)) # display_data에 있는거 출력
                                            # 그냥 file_io_prac에 있는 함수 쓰면 될듯?

    st.subheader("멘티 정보 입력")

    mentee_name = st.text_input("이름")
    subjects = st.multiselect( # 과목 다중선택
        "배우고 싶은 분야",
        [ "국어",  "영어", "수학", "사회", "과학", "역사", "도덕",
        "기술가정", "정보", "체육", "음악", "미술"]
    )
    days = st.multiselect( # 요일 다중선택
        "가능한 요일",
        ["월", "화", "수", "목", "금", "토", "일"]
    )
    level = st.selectbox( # 현재 수준 선택
        "현재 수준",
        ["초급", "중급", "고급"]
    )
    method = st.selectbox( # 온/오프라인 여부 선택
        "수업 방법",
        ["온라인", "오프라인"]
    )
    middle_score = st.number_input( # 중간고사 점수 입력
        "중간고사 점수",
        min_value=0,
        max_value=100
    )
    

    if st.button("나와 맞는 멘토 찾기"): # 멘토찾기 버튼 눌렀을때
        if not mentee_name.strip(): # 이름없음
            st.warning("이름을 입력하세요.")
        elif not subjects: # 과목 선택 안함
            st.warning("배우고 싶은 과목을 하나 이상 선택하세요.")
        elif not days: # 요일 선택 안함
            st.warning("가능한 요일을 하나 이상 선택하세요.")
        else:
            mentee = {
                "name": mentee_name.strip(),
                "subjects": subjects,
                "days": days,
                "level": level,
                "method": method,
                "middle_score": middle_score
            }

            read_mentees()  # 기존 멘티 정보 불러오기

            mentees.append(mentee)  # 새로운 멘티 정보 추가

            write_mentees()  # 기존 정보 + 새로운 정보 저장

            results = match_mentors(mentors, mentee)

            if not results:
                st.info("관심 분야가 맞는 멘토가 없습니다.")
            else:
                st.subheader(f"{mentee['name']}님의 추천 결과")

                for rank, result in enumerate(results, start=1):
                    st.markdown(f"### {rank}위 {result['name']} - {result['score']}점") # 1위 홍길동 - 100점

                    st.progress(int(result["score"]))

                    st.write("분야:", ", ".join(result["subjects"]))
                    st.write("가능 요일:", ", ".join(result["days"]))
                    st.write("방식:", result["method"])

                    st.write("추천 이유")
                    for reason in result["reasons"]:
                        st.write("-", reason)

                    st.divider()
    if st.button("돌아가기") :
            st.session_state.page = "home" # 홍으로 돌아가기
            st.rerun() # 화면 초기화

elif st.session_state.page == "Check_MM" :
    st.title("멘토, 멘티 확인")
    st.write("멘토")
    #멘토 표 보여주기
    st.write("멘티")
    #멘티 표 보여주기
    if st.button("돌아가기") :
        st.session_state.page = "home" # 홍으로 돌아가기
        st.rerun() # 화면 초기화



empty = ''' #주석 출력 방지용
내용 질문
- 왜만들음? 공부를 하고 싶은데 학원비가 부담되거나 성적이 낮은 친구들이 부담되지 않게 성적을 향상시켜주려고
- 성적 왜 올려줌??? 그러게 나라발전? 공평한 기회 제공?

프로그램 질문
국어는 잘하는데 수학을 못하면 어떡함?
시간도 안맞을수도 있지 않음?
-> 각 항목마다 값이 다를때
   어떻게하지
중간고사 점수만으로 잘함 못함이 판별 가능할까? 
찍어서 90점맞고 밀려서 80점맞으면 어떻게함? 정확도가 떨어짐, 초~고 기준이라서 모의고사도 못쓰네

사람들이 정직하게 점수를 쓸것인가? <- 이건 배제해야할듯

'''
