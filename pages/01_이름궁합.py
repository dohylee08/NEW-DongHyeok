import streamlit as st
import re

# 설정: 이동혁 이름 고정
FIXED_NAME = "이동혁"

st.set_page_config(page_title="이름궁합 (획수 피라미드) - 이동혁 고정", page_icon="❤️")

st.title("❤️ 이름 궁합 (획수 피라미드) 테스트")
st.write(f"두 사람 중 한 명은 **{FIXED_NAME}**로 고정되어 있습니다!\n다른 한 분의 이름을 입력하고 궁합을 확인해보세요.")

# 획수 데이터
CHO = {'ㄱ':2,'ㄲ':4,'ㄴ':2,'ㄷ':3,'ㄸ':6,'ㄹ':5,'ㅁ':4,'ㅂ':4,'ㅃ':8,
       'ㅅ':2,'ㅆ':4,'ㅇ':1,'ㅈ':3,'ㅉ':6,'ㅊ':4,'ㅋ':3,'ㅌ':4,'ㅍ':5,'ㅎ':3}
JUN = {'ㅏ':2,'ㅐ':3,'ㅑ':3,'ㅒ':4,'ㅓ':2,'ㅔ':3,'ㅕ':3,'ㅖ':4,'ㅗ':2,'ㅘ':3,
       'ㅙ':4,'ㅚ':3,'ㅛ':3,'ㅜ':2,'ㅝ':3,'ㅞ':4,'ㅟ':3,'ㅠ':3,'ㅡ':1,'ㅢ':2,'ㅣ':1}
JONG = ["", "ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
JONG_STROKES = {ch: CHO[ch] if ch in CHO else (CHO[ch[0]] + JUN[ch[1]] if len(ch)==2 else 0) for ch in JONG if ch}

# 한 글자 획수 계산 함수
def decompose_and_count(ch):
    if not re.match(r"[가-힣]", ch):
        return 0
    code = ord(ch) - ord('가')
    cho = code // (21 * 28)
    jung = (code % (21 * 28)) // 28
    jong = code % 28

    # 초
    cho_char = list(CHO.keys())[cho]
    # 중
    jung_char = list(JUN.keys())[jung]
    # 종
    jong_char = JONG[jong]
    
    strokes = CHO.get(cho_char, 0) + JUN.get(jung_char, 0) + JONG_STROKES.get(jong_char, 0)
    return strokes

# 두 이름 섞기
def interleave(name1, name2):
    arr = []
    l1, l2 = len(name1), len(name2)
    for i in range(max(l1, l2)):
        if i < l1: arr.append(name1[i])
        if i < l2: arr.append(name2[i])
    return arr

# 피라미드 합산
def pyramid(strokes):
    levels = [strokes]
    while len(levels[-1]) > 2:
        cur = levels[-1]
        nxt = []
        for i in range(len(cur) - 1):
            s = cur[i] + cur[i+1]
            if s >= 10:
                nxt.extend([s // 10, s % 10])
            else:
                nxt.append(s)
        levels.append(nxt)
    return levels

# 입력받기
other_name = st.text_input("상대방 이름 입력")

if st.button("궁합 계산하기"):
    if not other_name:
        st.warning("상대방의 이름을 입력해주세요.")
    else:
        seq = interleave(FIXED_NAME, other_name)
        strokes = [decompose_and_count(ch) for ch in seq]
        levels = pyramid(strokes)
        final = levels[-1]
        score = final[0] * 10 + final[1]

        st.subheader(f"💌 {FIXED_NAME} ❤️ {other_name} 궁합 점수: **{score}점**")
        st.write("### 📊 피라미드 과정")
        for lvl in levels:
            st.write(lvl)

        if score >= 80:
            st.success("✨ 아주 찰떡궁합입니다! ✨")
            st.balloons()
        elif score >= 50:
            st.info("😊 괜찮은 궁합이에요! 서로 노력해 보세요.")
        else:
            st.error("😅 조금 더 서로 이해가 필요할 수도 있어요.")

st.markdown("---")
st.caption("※ 이 결과는 오락용입니다. 과학적 근거가 없어요 😉")

