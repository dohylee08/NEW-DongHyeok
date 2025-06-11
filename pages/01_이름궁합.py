import streamlit as st
import re

# 고정 이름 설정
FIXED_NAME = "이동혁"

st.set_page_config(page_title="이동혁 이름궁합 (획수 피라미드)", page_icon="❤️")

st.title("❤️ 이름 궁합 테스트 (획수 피라미드)")
st.write(f"한쪽 이름은 **{FIXED_NAME}**로 고정되어 있습니다.")
st.write("상대방 이름을 입력한 후 '궁합 계산하기' 버튼을 눌러 결과를 확인하세요.")

# 초성, 중성, 종성 리스트 및 획수 데이터
CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
CHO_STROKES =    [2,4,2,3,6,5,4,4,8,2,4,1,3,6,4,3,4,5,3]

JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JUN_STROKES =    [2,3,3,4,2,3,3,4,2,3,4,3,3,2,3,4,3,3,1,2,1]

# 종성은 단일 자모와 복합 자모 분리
JONGSUNG_LIST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
# 복합 종성 분해 맵
COMPOSITE_JONG = {
    'ㄳ': ('ㄱ', 'ㅅ'), 'ㄵ': ('ㄴ', 'ㅈ'), 'ㄶ': ('ㄴ', 'ㅎ'),
    'ㄺ': ('ㄹ', 'ㄱ'), 'ㄻ': ('ㄹ', 'ㅁ'), 'ㄼ': ('ㄹ', 'ㅂ'), 'ㄽ': ('ㄹ', 'ㅅ'),
    'ㄾ': ('ㄹ', 'ㅌ'), 'ㄿ': ('ㄹ', 'ㅍ'), 'ㅀ': ('ㄹ', 'ㅎ'), 'ㅄ': ('ㅂ', 'ㅅ')
}
# 종성 획수 사전 생성
JONG_STROKES = { '': 0 }
for jong in JONGSUNG_LIST[1:]:
    if jong in CHOSUNG_LIST:
        JONG_STROKES[jong] = CHO_STROKES[CHOSUNG_LIST.index(jong)]
    elif jong in COMPOSITE_JONG:
        c1, c2 = COMPOSITE_JONG[jong]
        strokes = CHO_STROKES[CHOSUNG_LIST.index(c1)] + CHO_STROKES[CHOSUNG_LIST.index(c2)]
        JONG_STROKES[jong] = strokes
    else:
        JONG_STROKES[jong] = 0

# 한 글자 획수 계산
def count_strokes(ch: str) -> int:
    if not re.match(r"[가-힣]", ch):
        return 0
    code = ord(ch) - ord('가')
    cho_idx = code // (21 * 28)
    jung_idx = (code % (21 * 28)) // 28
    jong_idx = code % 28

    return (
        CHO_STROKES[cho_idx] +
        JUN_STROKES[jung_idx] +
        JONG_STROKES[JONGSUNG_LIST[jong_idx]]
    )

# 두 이름 번갈아 섞기
def interleave(name1: str, name2: str) -> list:
    merged = []
    for i in range(max(len(name1), len(name2))):
        if i < len(name1): merged.append(name1[i])
        if i < len(name2): merged.append(name2[i])
    return merged

# 피라미드 합산
def pyramid_sum(nums: list) -> list:
    levels = [nums]
    while len(levels[-1]) > 2:
        curr = levels[-1]
        next_lvl = []
        for i in range(len(curr) - 1):
            s = curr[i] + curr[i+1]
            if s >= 10:
                next_lvl.extend([s // 10, s % 10])
            else:
                next_lvl.append(s)
        levels.append(next_lvl)
    return levels

# Streamlit UI
other_name = st.text_input("상대방 이름 입력:")
if st.button("궁합 계산하기"):
    if not other_name:
        st.warning("상대방 이름을 입력해주세요.")
    else:
        seq = interleave(FIXED_NAME, other_name)
        strokes = [count_strokes(c) for c in seq]
        levels = pyramid_sum(strokes)
        final = levels[-1]
        score = final[0] * 10 + final[1]

        st.subheader(f"🔮 {FIXED_NAME} ❤️ {other_name} 궁합 점수: {score}점")
        st.write("---")
        st.write("#### 📊 피라미드 단계별 수치:")
        for lvl in levels:
            st.write(lvl)

        if score >= 80:
            st.success("✨ 찰떡궁합입니다! 🎉")
            st.balloons()
        elif score >= 50:
            st.info("😊 좋은 시작이에요. 서로 맞춰보세요!")
        else:
            st.error("😅 좀 더 알아가며 이해가 필요해요.")

st.markdown("---")
st.caption("*참고: 오락용 결과입니다.*")



