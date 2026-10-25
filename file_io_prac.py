'''
만들어야하는거 :

예외처리(입력받을때 이상한거 넣을때)

함수 
1. 파일 정보 읽어서 mentors에 저장하는거 - 완성(read_mentor)
2. 사용자에게 정보받아서 mentors에 저장(append) 해주는거 - 완성(add_mentor)
3. mentors를 파일에 저장하는거 - 완성(open_mentor)

방식
1. 파일 "r"로 열기
2. 프로그램 mentors에 파일에 있는 정보 불러오기
3. 저장 하면 "a"로 추가하기
'''

MENTOR_FILE = "mentors.txt"
MENTEE_FILE = "mentees.txt"



#사용자 -> 딕셔너리
def add_people(peoples) :
   people = {
      "name" : input("이름 : ").strip(),
      "subjects" : input("과목(,로 구분) : ").split(),
      "days" : input("가능 요일(,로 구분) : ").split(),
      "levels" : input("수준(,로 구분) : ").split(),
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
         f.write(", ".join(people["subjects"]) + "\n") # 띄어쓰기로 나열하기 (국어 영어 수학)
         f.write(", ".join(people["days"]) + "\n")
         f.write(", ".join(people["levels"]) + "\n")
         f.write(str(people["middle_score"]) + "\n")
         f.write("----------\n") # 구분하는거
      f.close()

def write_mentors() :
   write_people(MENTOR_FILE, mentors)

def write_mentees() :
   write_people(MENTEE_FILE, mentees)



# 파일 -> 딕셔너리
def read_people(filename, peoples) : # 파일에서부터 정보 꺼내서 딕셔너리에 저장
   f = open(filename, "r", encoding="utf-8")
   for i, data in enumerate(f) :  # enumerate(f)는 파일의 줄과 그 줄의 정보 출력, i = 0, data = "홍길동"
      index = i // 6 # 몫 구하기
      data = data.strip() # 앞뒤 공백, 줄바꿈 제거
      match i % 6 : # switch case 문 비슷한거, default는 _로
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
            data = data.split(", ")
            peoples[index]["levels"] = data
         case 4 : 
            peoples[index]["middle_score"] = int(data) # 중간 점수는 정수로 받기
         case _ : # 나머지 저거 -----일때 무시
            continue

def read_mentors() :
   return read_people(MENTOR_FILE, mentors)

def read_mentees() :
   return read_people(MENTEE_FILE, mentees)






mentors = [ ] # 빈 딕셔너리
mentees = [ ]

#실행 코드
# | | |
# V V V


question = input("멘토 or 멘티 : ")

if question == "멘토" :
   read_mentors()
   print("멘토 등록\n--------------------------\n")
   add_mentor()
   write_mentors()

elif question == "멘티" :
   read_mentees()
   print("멘티 등록\n--------------------------\n")
   add_mentee()
   write_mentees()

else :
   print("잘못된 입력입니다")
   