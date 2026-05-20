import streamlit as st
from datetime import datetime

# 제목
st.title("📅 스케줄 관리 앱")

# 세션 저장소 생성
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# 입력 영역
task = st.text_input("할 일 입력")
task_date = st.date_input("날짜 선택")

# 추가 버튼
if st.button("일정 추가"):

    # 빈값 체크
    if task.strip() == "":
        st.warning("할 일을 입력하세요.")
    else:
        st.session_state.todo_list.append(
            {
                "task": task,
                "date": str(task_date)
            }
        )
        st.success("추가 완료")

# 구분선
st.write("---")

# 일정 목록
st.subheader("일정 목록")

# 일정 없을 때
if len(st.session_state.todo_list) == 0:
    st.info("등록된 일정이 없습니다.")

# 일정 출력
for idx, item in enumerate(st.session_state.todo_list):

    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(f"{item['date']} - {item['task']}")

    with col2:
        if st.button("삭제", key=f"delete_{idx}"):
            st.session_state.todo_list.pop(idx)
            st.experimental_rerun()
