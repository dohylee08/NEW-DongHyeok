import streamlit as st
import folium
from streamlit_folium import st_folium

# 여행지 데이터 (예시)
travel_destinations = {
    "뉴욕 (New York City)": {
        "coords": (40.7128, -74.0060),
        "description": "미국 최대 도시 뉴욕! 타임스퀘어, 센트럴파크, 자유의 여신상 등 다양한 명소가 있습니다."
    },
    "샌프란시스코 (San Francisco)": {
        "coords": (37.7749, -122.4194),
        "description": "금문교(Golden Gate Bridge), 알카트라즈 섬, 트램 등으로 유명한 도시입니다."
    },
    "라스베이거스 (Las Vegas)": {
        "coords": (36.1699, -115.1398),
        "description": "카지노와 화려한 쇼로 유명한 세계적인 엔터테인먼트 도시입니다."
    },
    "그랜드 캐니언 (Grand Canyon)": {
        "coords": (36.1069, -112.1129),
        "description": "세계적인 자연경관! 거대한 협곡과 붉은 바위의 장엄한 풍경을 감상할 수 있습니다."
    },
    "올랜도 (Orlando)": {
        "coords": (28.5383, -81.3792),
        "description": "디즈니월드와 유니버설 스튜디오가 있는 미국 최고의 테마파크 도시입니다."
    }
}

# Streamlit 페이지 설정
st.set_page_config(page_title="미국 여행 가이드", layout="wide")

st.title("🇺🇸 미국 여행지 가이드")
st.write("미국의 주요 여행지를 지도와 함께 소개합니다!")

# 여행지 선택
selected_place = st.selectbox("방문하고 싶은 여행지를 선택하세요:", list(travel_destinations.keys()))

# 선택한 여행지 정보
info = travel_destinations[selected_place]
st.subheader(selected_place)
st.write(info["description"])

# 지도 생성
m = folium.Map(location=info["coords"], zoom_start=5)

# 마커 추가
for place, data in travel_destinations.items():
    folium.Marker(
        location=data["coords"],
        popup=f"<b>{place}</b><br>{data['description']}",
        tooltip=place,
        icon=folium.Icon(color="blue" if place != selected_place else "red")
    ).add_to(m)

# 선택된 장소로 지도 중심 이동 및 확대
folium.Marker(
    location=info["coords"],
    popup=f"<b>{selected_place}</b><br>{info['description']}",
    tooltip=selected_place,
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# 지도 출력
st_data = st_folium(m, width=800, height=500)

