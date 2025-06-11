import streamlit as st
import random

# 음식점 데이터 (예시)
restaurant_data = {
    "서울": {
        "한식": ["한남동 맛집", "명동 설렁탕", "강남 곰탕"],
        "일식": ["스시 오마카세", "신주쿠 우동", "도쿄 라멘"],
        "중식": ["북경반점", "마라탕 전문점", "홍콩 딤섬"],
        "양식": ["이태리 파스타", "스테이크 하우스", "브런치 카페"]
    },
    "부산": {
        "한식": ["광안리 회센터", "부산 돼지국밥", "해운대 갈비"],
        "일식": ["해운대 스시", "일본 라멘 거리", "사카에 초밥"],
        "중식": ["부산 마라샹궈", "중국집 대박", "부산 딤섬 거리"],
        "양식": ["남포동 피자", "서면 스테이크", "해운대 브런치"]
    },
    "제주": {
        "한식": ["제주 흑돼지", "성산 전복 뚝배기", "우도 땅콩 아이스크림"],
        "일식": ["스시 제주", "라멘 거리", "사시미 전문점"],
        "중식": ["제주 마라탕", "홍콩 딤섬 제주점", "중식 뷔페"],
        "양식": ["제주 피자집", "오션 뷰 레스토랑", "제주 브런치"]
    }
}

st.set_page_config(page_title="음식점 추천기", page_icon="🍽️")

st.title("🍽️ 음식점 추천 서비스")
st.write("원하는 지역과 음식 종류를 선택하면 음식점을 추천해 드립니다!")

# 지역 선택
region = st.selectbox("📍 지역 선택", list(restaurant_data.keys()))

# 음식 종류 선택
food_type = st.radio("🍱 음식 종류 선택", list(restaurant_data[region].keys()))

# 추천 버튼
if st.button("추천 받기"):
    recommendation = random.choice(restaurant_data[region][food_type])
    st.success(f"👉 추천 음식점: **{recommendation}**")
else:
    st.info("원하는 지역과 음식 종류를 선택한 뒤 버튼을 눌러보세요!")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
