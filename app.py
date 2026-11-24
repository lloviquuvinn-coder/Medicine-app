import datetime  # 표준 라이브러리 활용
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="개인맞춤 약 복용 가이드", page_icon="💊", layout="centered"
)

st.title("💊 증상-질병 상호작용 및 개인맞춤 약 복용 가이드")
st.caption(f"보건 진로 연계 프로젝트 | 조회 기준일: {datetime.date.today()}")
st.write("나이와 겪고 있는 증상 번호를 선택하면 맞춤 복용 약을 안내해 드립니다.")

# 1. 리스트(List) 정의: 약 종류 및 증상 목록
medicines = [
    "탁센",
    "타이레놀",
    "활명수",
    "항생제",
    "어린이용 타이레놀",
    "이지엔",
]
symptoms = ["감기", "생리통", "두통", "체함", "몸살"]

# 증상별 추천 약 매핑 (리스트 활용)
symptom_meds = {
    "감기": ["탁센", "의사에게 처방받은 항생제"],
    "생리통": ["이지엔", "탁센"],
    "두통": ["탁센", "타이레놀"],
    "체함": ["활명수"],
    "몸살": ["타이레놀"],
}


# 2. 함수(Function) 정의: def check_disease(med_name, age)
def check_disease(med_name, age):
  """
    선택된 증상(med_name)과 나이(age)를 바탕으로
    추천 약 안내 문구와 복용 주의사항을 반환하는 함수
    """
  # 3. 조건문(if / elif / else)으로 나이 및 증상별 약 추천 로직 처리
  if age <= 13:
    # 13세 이하인 경우 어린이용 타이레놀 우선 추천 안내
    base_guide = f"{age}세이므로 **어린이용 타이레놀** 복용을 우선적으로 고려해 보세요."
    if med_name in symptom_meds:
      ref_list = symptom_meds[med_name]
      ref_text = "이나 ".join(ref_list) if len(ref_list) == 2 else ref_list[0]
      detail_note = (
          f" (참고: 성인/청소년 기준 {med_name} 증상에는 {ref_text} 등이"
          " 언급되나, 13세 이하는 연령에 맞는 용량·제형 확인이 꼭"
          " 필요합니다.)"
      )
    else:
      detail_note = ""
    return f"{base_guide}{detail_note}"

  # 14세 이상 ~ 100세 이하인 경우 증상별 문구 반환
  if med_name == "두통":
    return "두통증상을 겪는다면 탁센이나 타이레놀을 추천합니다"
  elif med_name == "감기":
    return "감기증상을 겪는다면 탁센이나 의사에게 처방받은 항생제를 추천합니다"
  elif med_name == "생리통":
    return "생리통증상을 겪는다면 이지엔이나 탁센을 추천합니다"
  elif med_name == "몸살":
    return "몸살증상을 겪는다면 타이레놀을 추천합니다"
  elif med_name == "체함":
    return "체함증상을 겪는다면 활명수를 추천합니다"
  else:
    return "선택한 증상에 대한 안내 정보가 없습니다."


st.divider()

# 사용자 입력 영역
age = st.slider(
    "나이를 선택하세요 (1세 ~ 100세)", min_value=1, max_value=100, value=17
)

# 4. 반복문(for)을 사용해 번호가 붙은 증상 선택지 생성
numbered_options = []
for idx, symptom in enumerate(symptoms, start=1):
  numbered_options.append(f"{idx}. {symptom}")

selected_option = st.selectbox(
    "증상 번호를 고른 뒤 선택하세요",
    options=numbered_options,
    index=2,  # 기본값: 3. 두통
)

# 선택한 번호를 기준으로 실제 증상명 추출 (반복문 활용)
selected_symptom = ""
for idx, symptom in enumerate(symptoms, start=1):
  if selected_option.startswith(f"{idx}. "):
    selected_symptom = symptom
    break

# 결과 출력 버튼 및 화면 표시
if st.button("맞춤 약 확인하기", type="primary"):
  result_message = check_disease(selected_symptom, age)
  st.subheader("📋 맞춤 약 복용 안내 결과")
  st.success(result_message)

  # 보건 연계 복용 주의사항 안내
  st.info(
      "**보건 복용 주의사항**\n"
      "- 항생제는 세균 감염 시 **의사의 처방**에 따라 정해진 기간만큼 복용해야 합니다.\n"
      "- 진통제(탁센, 타이레놀, 이지엔 등)는 성분 중복 및 위장 장애를 피하기 위해 약사·의사와 상담 후 복용하세요.\n"
      "- 증상이 심해지거나 고열·복통 등이 지속되면 반드시 병원을 방문하세요."
  )

with st.expander("등록된 증상 번호 및 약 목록 보기"):
  st.write("**증상 번호 목록**")
  for idx, s in enumerate(symptoms, start=1):
    st.write(f"- {idx}번: {s}")

  st.write("**등록된 약 종류**")
  for m in medicines:
    st.write(f"- {m}")
