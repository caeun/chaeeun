import streamlit as st
import google.generativeai as genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# -----------------------------
# API 키 불러오기
# -----------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)

except Exception:
    st.error("API 키를 불러올 수 없습니다. secrets 설정을 확인하세요.")
    st.stop()

# -----------------------------
# 모델 생성
# -----------------------------
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction="""
        너는 따뜻하고 공감 능력이 뛰어난 연애상담 전문가야.
        사용자의 감정을 존중하고 현실적인 조언을 제공해.
        너무 공격적이거나 단정적인 표현은 피하고,
        친근한 말투로 답변해.
        """
    )

except Exception as e:
    st.error(f"모델 생성 오류: {e}")
    st.stop()

# -----------------------------
# 채팅 기록 저장
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        try:
            with st.spinner("생각 중..."):

                # 대화 기록 구성
                history = []

                for msg in st.session_state.messages[:-1]:

                    role = "user" if msg["role"] == "user" else "model"

                    history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })

                # 채팅 시작
                chat = model.start_chat(history=history)

                response = chat.send_message(user_input)

                bot_reply = response.text

                st.markdown(bot_reply)

                # 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_reply
                })

        except Exception as e:
            error_msg = f"오류가 발생했습니다: {e}"

            st.error(error_msg)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
