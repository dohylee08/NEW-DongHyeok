import streamlit as st
import pandas as pd
import random

# 음식점 데이터 (위도, 경도 포함)
restaurant_data = {
    "서울": {
        "한식": [
            {"name": "한남동 맛집", "lat": 37.535, "lon": 127.005},
            {"name": "명동 설렁탕", "lat": 37.563, "lon": 126.982},
            {"name": "강남 곰탕", "lat": 37.497, "lon": 127.028},
        ],
        "일식": [
            {"name": "스시 오마카세", "lat": 37.519, "lon": 127.022},
            {"name": "신주쿠 우동", "lat": 37.566, "lon": 126.978},
            {"name": "도쿄 라멘", "lat": 37.511, "lon": 127.059},
        ],
        "중식": [
            {"name": "북경반점", "lat": 37.561, "lon": 126.994},
            {"name": "마라탕 전문점", "lat": 37.545, "lon": 127.039},
            {"name": "홍콩 딤섬", "lat": 37.556, "lon": 126.937},
        ],
        "양식": [
            {"name": "이태리 파스타", "lat": 37.523, "lon": 127.021},
            {"name": "스테이크 하우스", "lat": 37.504, "lon": 127.002},
            {"name": "브런치 카페", "lat": 37.547, "lon": 127.047},
        ],
    },
    # 더 추가 가능: 부산, 제주 등
}

st.set_page_config(page_title="음식점 추천 지도", page_icon="🍽️", layout="wide")

st.title("🍽️ 음식점 추천 & 지도 표시 서비스")
st.write("**지역과 음식 종류를 선택하면 음식점을 추천하고 위치를 지도에 표시합니다!**")

region = st.selectbox("📍 지역 선택", list(restaurant_data.keys()))
food_type = st.radio("🍱 음식 종류 선택", list(restaurant_data[region].keys()))

if st.button("추천 받기"):
    choice = random.choice(restaurant_data[region][food_type])
    st.success(f"👉 추천 음식점: **{choice['name']}**")

    # 지도 표시용 데이터프레임 생성
    df = pd.DataFrame({
        'lat': [choice['lat']],
        'lon': [choice['lon']],
        'name': [choice['name']],
    })

    st.map(df, zoom=12)

    with st.expander("📌 음식점 상세 위치 정보"):
        st.write(f"**이름**: {choice['name']}")
        st.write(f"**위도**: {choice['lat']}")
        st.write(f"**경도**: {choice['lon']}")
else:
    st.info("추천 버튼을 눌러주세요!")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")

